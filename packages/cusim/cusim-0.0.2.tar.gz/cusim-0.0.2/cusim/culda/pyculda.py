# Copyright (c) 2021 Jisang Yoon
# All rights reserved.
#
# This source code is licensed under the Apache 2.0 license found in the
# LICENSE file in the root directory of this source tree.

# pylint: disable=no-name-in-module,too-few-public-methods,no-member
import os
from os.path import join as pjoin

import json
import atexit
import shutil
import tempfile

import h5py
import numpy as np
from scipy.special import polygamma as pg

from cusim import aux, IoUtils
from cusim.culda.culda_bind import CuLDABind
from cusim.config_pb2 import CuLDAConfigProto
from cusim.constants import EPS, WARP_SIZE


class CuLDA:
  def __init__(self, opt=None):
    self.opt = aux.get_opt_as_proto(opt or {}, CuLDAConfigProto)
    self.logger = aux.get_logger("culda", level=self.opt.py_log_level)

    assert self.opt.block_dim <= WARP_SIZE ** 2 and \
      self.opt.block_dim % WARP_SIZE == 0, \
      f"invalid block dim ({self.opt.block_dim}, warp size: {WARP_SIZE})"

    tmp = tempfile.NamedTemporaryFile(mode='w', delete=False)
    opt_content = json.dumps(aux.proto_to_dict(self.opt), indent=2)
    tmp.write(opt_content)
    tmp.close()

    self.logger.info("opt: %s", opt_content)
    self.obj = CuLDABind()
    assert self.obj.init(bytes(tmp.name, "utf8")), f"failed to load {tmp.name}"
    os.remove(tmp.name)

    self.words, self.num_words, self.num_docs = None, None, None
    self.alpha, self.beta, self.grad_alpha, self.new_beta = \
      None, None, None, None

    self.tmp_dirs = []
    atexit.register(self.remove_tmp)

  def preprocess_data(self):
    if self.opt.skip_preprocess:
      return
    iou = IoUtils(aux.proto_to_dict(self.opt.io))
    if not self.opt.processed_data_path:
      data_dir = tempfile.TemporaryDirectory().name
      self.tmp_dirs.append(data_dir)
      self.opt.processed_data_path = pjoin(data_dir, "token.h5")
    iou.convert_bow_to_h5(self.opt.data_path, self.opt.processed_data_path)

  def init_model(self):
    # count number of docs and load voca
    assert os.path.exists(self.opt.processed_data_path)
    assert os.path.exists(self.opt.keys_path)
    h5f = h5py.File(self.opt.processed_data_path, "r")
    self.num_docs = h5f["indptr"].shape[0] - 1
    h5f.close()
    with open(self.opt.keys_path, "rb") as fin:
      self.words = [line.strip().decode("utf8") for line in fin]
    self.num_words = len(self.words)

    self.logger.info("number of words: %d, docs: %d",
                     self.num_words, self.num_docs)

    # random initialize alpha and beta
    np.random.seed(self.opt.seed)
    self.alpha = np.random.uniform( \
      size=(self.opt.num_topics,)).astype(np.float32)
    self.beta = np.random.uniform( \
      size=(self.num_words, self.opt.num_topics)).astype(np.float32)
    self.beta /= np.sum(self.beta, axis=0)[None, :]
    self.logger.info("alpha %s, beta %s initialized",
                     self.alpha.shape, self.beta.shape)

    # zero initialize grad alpha and new beta
    block_cnt = self.obj.get_block_cnt()
    self.grad_alpha = np.zeros(shape=(block_cnt, self.opt.num_topics),
                               dtype=np.float32)
    self.new_beta = np.zeros(shape=self.beta.shape, dtype=np.float32)
    self.logger.info("grad alpha %s, new beta %s initialized",
                     self.grad_alpha.shape, self.new_beta.shape)

    # set h5 file path to backup gamma
    if not self.opt.gamma_path:
      data_dir = tempfile.TemporaryDirectory().name
      self.tmp_dirs.append(data_dir)
      self.opt.gamma_path = pjoin(data_dir, "gamma.h5")
    self.logger.info("backup gamma to %s", self.opt.gamma_path)
    os.makedirs(os.path.dirname(self.opt.gamma_path), exist_ok=True)
    h5f = h5py.File(self.opt.gamma_path, "w")
    h5f.create_dataset("gamma", shape=(self.num_docs, self.opt.num_topics),
                       dtype=np.float32)
    h5f.close()

    # push it to gpu
    self.obj.load_model(self.alpha, self.beta, self.grad_alpha, self.new_beta)

  def train_model(self):
    self.preprocess_data()
    self.init_model()
    h5f = h5py.File(self.opt.processed_data_path, "r")
    for epoch in range(1, self.opt.epochs + 1):
      gamma_h5f = h5py.File(self.opt.gamma_path, "r+")
      self.logger.info("Epoch %d / %d", epoch, self.opt.epochs)
      self._train_e_step(h5f, gamma_h5f["gamma"], epoch)
      self._train_m_step()
      gamma_h5f.close()
    h5f.close()

  def _train_e_step(self, h5f, gamma_h5f, epoch):
    offset, size = 0, h5f["cols"].shape[0]
    pbar = aux.Progbar(size, stateful_metrics=["train_loss", "vali_loss"])
    train_loss_nume, train_loss_deno = 0, 0
    vali_loss_nume, vali_loss_deno = 0, 0
    while True:
      target = h5f["indptr"][offset] + self.opt.batch_size
      if target < size:
        next_offset = h5f["rows"][target]
      else:
        next_offset = h5f["indptr"].shape[0] - 1
      indptr = h5f["indptr"][offset:next_offset + 1]
      beg, end = indptr[0], indptr[-1]
      indptr -= beg
      cols = h5f["cols"][beg:end]
      counts = h5f["counts"][beg:end]
      vali = (h5f["vali"][beg:end] < self.opt.vali_p).astype(np.bool)
      gamma = gamma_h5f[offset:next_offset, :]

      # call cuda kernel
      train_loss, vali_loss = \
        self.obj.feed_data(cols, indptr.astype(np.int32),
                           vali, counts, gamma,
                           epoch == 1 or self.opt.reuse_gamma,
                           self.opt.num_iters_in_e_step)

      gamma_h5f[offset:next_offset, :] = gamma
      # accumulate loss
      train_loss_nume -= train_loss
      vali_loss_nume -= vali_loss
      train_loss_deno += np.sum(counts[~vali])
      vali_loss_deno += np.sum(counts[vali])
      train_loss = train_loss_nume / (train_loss_deno + EPS)
      vali_loss = vali_loss_nume / (vali_loss_deno + EPS)

      # update progress bar
      pbar.update(end, values=[("train_loss", train_loss),
                               ("vali_loss", vali_loss)])
      offset = next_offset

      if end == size:
        break

  def _train_m_step(self):
    self.obj.pull()

    # update beta
    self.new_beta[:, :] = np.maximum(self.new_beta, EPS)
    self.beta[:, :] = self.new_beta / np.sum(self.new_beta, axis=0)[None, :]
    self.new_beta[:, :] = 0

    # update alpha
    alpha_sum = np.sum(self.alpha)
    gvec = np.sum(self.grad_alpha, axis=0)
    gvec += self.num_docs * (pg(0, alpha_sum) - pg(0, self.alpha))
    hvec = self.num_docs * pg(1, self.alpha)
    z_0 = pg(1, alpha_sum)
    c_nume = np.sum(gvec / hvec)
    c_deno = 1 / z_0 + np.sum(1 / hvec)
    c_0 = c_nume / c_deno
    delta = (gvec - c_0) / hvec
    self.alpha -= delta
    self.alpha[:] = np.maximum(self.alpha, EPS)
    self.grad_alpha[:,:] = 0

    self.obj.push()

  def save_h5_model(self, filepath, chunk_size=10000):
    self.logger.info("save h5 format model path to %s", filepath)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    h5f = h5py.File(filepath, "w")
    h5f.create_dataset("alpha", data=self.alpha)
    h5f.create_dataset("beta", data=self.beta)
    h5f.create_dataset("keys", data=np.array([word.encode("utf")
                                              for word in self.words]))
    gamma = h5f.create_dataset("gamma", dtype=np.float32,
                               shape=(self.num_docs, self.opt.num_topics))
    h5f_gamma = h5py.File(self.opt.gamma_path, "r")
    for offset in range(0, self.num_docs, chunk_size):
      next_offset = min(self.num_docs, offset + chunk_size)
      gamma[offset:next_offset, :] = h5f_gamma["gamma"][offset:next_offset, :]
    h5f_gamma.close()
    h5f.close()

  def remove_tmp(self):
    if not self.opt.remove_tmp:
      return
    for tmp_dir in self.tmp_dirs:
      if os.path.exists(tmp_dir):
        self.logger.info("remove %s", tmp_dir)
        shutil.rmtree(tmp_dir)
