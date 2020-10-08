# GNU Lesser General Public License v3.0 only
# Copyright (C) 2020 Artefact
# licence-information@artefact.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import time
import numpy as np
from numpy.linalg import norm
from tqdm import tqdm


class SeaNMF:

    # pylint: disable=too-many-instance-attributes

    def __init__(
            self, mat_a, mat_s, mat_iw, mat_iwc, mat_ih, alpha=1.0, beta=0.1, n_topic=10,
            max_iter=100, max_err=1e-3, rand_init=True, fix_seed=False):
        """
        Seanmf is a topic modeling algorithm, paper:  http://dmkd.cs.vt.edu/papers/WWW18.pdf.
        It finds an approximation to the term-document matrix A by two lower-rank matrices W and H,
        at each iteration a context matrix Wc are computed and used to update W.
        :param mat_a: document term matrix
        :param mat_s: Word-context (semantic) correlation matrix
        :param mat_iw: topics Matrix, each column vector W(:,k) represents the k-th topic in terms of M keywords
        and its elements are the weights of the corresponding keywords.
        :param mat_iwc: Latent factor matrix of contexts.
        :param mat_ih: The row vector H(j,:) is the latent representation for document j in terms of K topics
        :param alpha: Seanmf algorithm parameter
        :param beta: Seanmf algorithm parameter
        :param n_topic: Number of selected topics
        :param max_iter: Maximum number of iterations to update W and H
        :param max_err: maximum error under which we consider that the loop converged
        :param rand_init: random init boolean
        :param fix_seed: int number to fix random seed.
        """
        if fix_seed:
            np.random.seed(0)

        self.mat_a = mat_a
        self.mat_s = mat_s

        self.n_row = mat_a.shape[0]
        self.n_col = mat_a.shape[1]

        self.n_topic = n_topic
        self.max_iter = max_iter
        self.alpha = alpha
        self.beta = beta
        self.mat_b = np.ones([self.n_topic, 1])
        self.max_err = max_err
        self.snmf_mat_init(rand_init, mat_iw, mat_iwc, mat_ih)
        self.snmf_iter()

    def snmf_mat_init(self, rand_init, mat_iw, mat_iwc, mat_ih):
        """
        Init Matrices W,Wc and H initially either randomly or using existing IW,IWc IH matrices taken when iterating.
        :param rand_init: Boolean indicating initial random init
        """
        if rand_init:
            self.mat_w = np.random.random((self.n_row, self.n_topic))
            self.mat_wc = np.random.random((self.n_row, self.n_topic))
            self.mat_h = np.random.random((self.n_col, self.n_topic))
        else:
            self.mat_w = mat_iw
            self.mat_wc = mat_iwc
            self.mat_h = mat_ih
        for k in range(self.n_topic):
            self.mat_w[:, k] /= norm(self.mat_w[:, k])
            self.mat_wc[:, k] /= norm(self.mat_wc[:, k])

    def snmf_iter(self):
        """
        Main iterative loop for matrix decomposition
        """
        loss_old = 1e20
        start_time = time.time()
        for i in tqdm(range(self.max_iter)):
            self.snmf_solver()
            loss = self.snmf_loss()
            if loss_old - loss < self.max_err:
                print('Matrix decomposition loop converged!')
                break
            loss_old = loss
            end_time = time.time()
            print('Step={}, Loss={}, Time={}s'.format(i, loss, end_time - start_time))

    def snmf_solver(self):
        '''
        using BCD framework
        Alogorithm 1: Equations to update W, wc, H matrices are described in the paper
        http://dmkd.cs.vt.edu/papers/WWW18.pdf
        '''

        epss = 1e-20
        # Update W
        mat_ah = np.dot(self.mat_a, self.mat_h)
        mat_swc = np.dot(self.mat_s, self.mat_wc)
        mat_hth = np.dot(self.mat_h.T, self.mat_h)
        mat_wctwc = np.dot(self.mat_wc.T, self.mat_wc)
        mat_w1 = self.mat_w.dot(self.mat_b)

        for k in range(self.n_topic):
            num0 = mat_hth[k, k] * self.mat_w[:, k] + self.alpha * mat_wctwc[k, k] * self.mat_w[:, k]
            num1 = mat_ah[:, k] + self.alpha * mat_swc[:, k]
            num2 = np.dot(self.mat_w, mat_hth[:, k]) + self.alpha * np.dot(
                self.mat_w, mat_wctwc[:, k]) + self.beta * mat_w1[0]
            self.mat_w[:, k] = num0 + num1 - num2
            self.mat_w[:, k] = np.maximum(self.mat_w[:, k], epss)  # project > 0
            self.mat_w[:, k] /= norm(self.mat_w[:, k]) + epss  # normalize
        # Update Wc
        mat_wtw = self.mat_w.T.dot(self.mat_w)
        mat_stw = np.dot(self.mat_s, self.mat_w)
        for k in range(self.n_topic):
            self.mat_wc[:, k] = self.mat_wc[:, k] + mat_stw[:, k] - np.dot(self.mat_wc, mat_wtw[:, k])
            self.mat_wc[:, k] = np.maximum(self.mat_wc[:, k], epss)
        # Update H
        mat_atw = np.dot(self.mat_a.T, self.mat_w)
        for k in range(self.n_topic):
            self.mat_h[:, k] = self.mat_h[:, k] + mat_atw[:, k] - np.dot(self.mat_h, mat_wtw[:, k])
            self.mat_h[:, k] = np.maximum(self.mat_h[:, k], epss)

    def snmf_loss(self):
        loss = norm(self.mat_a - np.dot(self.mat_w, np.transpose(self.mat_h)), 'fro') ** 2 / 2.0
        if self.alpha > 0:
            loss += self.alpha * norm(np.dot(self.mat_w, np.transpose(self.mat_wc)) - self.mat_s, 'fro') ** 2 / 2.0
        if self.beta > 0:
            loss += self.beta * norm(self.mat_w, 1) ** 2 / 2.0

        return loss

    def get_decomposition_matrix(self):
        # Wc was not considered to keep same structure as NMF
        return self.mat_w, self.mat_h
