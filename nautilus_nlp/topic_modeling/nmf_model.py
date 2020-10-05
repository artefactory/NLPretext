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


class NMF:

    # pylint: disable=too-many-instance-attributes

    def __init__(
            self, mat_a, mat_iw, mat_ih, n_topic=10,
            max_iter=100, max_err=1e-3, rand_init=True):
        """
        The objective of the NMF model is to approximate the term-document matrix A by two lower-rank matrices W and H.
        The process is iterative and we denote IW and IH the the matrix W and H that are updated at each step.

        :param a: The term-document matrix
        :param IW: topics Matrix, each column vector W(:,k) represents the k-th topic in terms of M keywords
        and its elements are the weights of the corresponding keywords.
        :param IH: The row vector H(j,:) is the latent representation for document j in terms of K topics
        :param n_topic: Number of selected topics
        :param max_iter: Maximum number of iterations to update W and H
        :param max_err: maximum error under which we consider that the loop converged
        :param rand_init: random init boolean
        """
        self.mat_a = mat_a
        self.mat_iw = mat_iw
        self.mat_ih = mat_ih
        self.n_row = mat_a.shape[0]
        self.n_col = mat_a.shape[1]

        self.n_topic = n_topic
        self.max_iter = max_iter
        self.max_err = max_err

        self.loss_hist = []
        self.nmf_mat_init(rand_init)
        self.nmf_iter()

    def nmf_mat_init(self, rand_init):
        """
        Init Matrices W and H initially either randomly or using existing IW, IH matrices taken when iterating.
        :param rand_init: Boolean indicating initial random init
        """
        if rand_init:
            self.mat_w = np.random.random((self.n_row, self.n_topic))
            self.mat_h = np.random.random((self.n_col, self.n_topic))
        else:
            self.mat_w = self.mat_iw
            self.mat_h = self.mat_ih
        for k in range(self.n_topic):
            self.mat_w[:, k] /= norm(self.mat_w[:, k])

    def nmf_iter(self):
        """
        Main iterative loop for matrix decomposition
        """
        loss_old = 1e20
        start_time = time.time()
        for i in tqdm(range(self.max_iter)):
            self.nmf_solver()
            loss = self.nmf_loss()
            self.loss_hist.append(loss)

            if loss_old - loss < self.max_err:
                print('Matrix decomposition loop converged!')
                break
            loss_old = loss
            end_time = time.time()
            print('Step={}, Loss={}, Time={}s'.format(i, loss, end_time - start_time))

    def nmf_solver(self):
        '''
        regular NMF without constraint.
        Block Coordinate Decent
        '''
        epss = 1e-20

        mat_hth = self.mat_h.T.dot(self.mat_h)
        mat_ah = self.mat_a.dot(self.mat_h)
        for k in range(self.n_topic):
            tmp_w = self.mat_w[:, k] * mat_hth[k, k] + mat_ah[:, k] - np.dot(self.mat_w, mat_hth[:, k])
            self.mat_w[:, k] = np.maximum(tmp_w, epss)
            self.mat_w[:, k] /= norm(self.mat_w[:, k]) + epss

        mat_wtw = self.mat_w.T.dot(self.mat_w)
        mat_atw = self.mat_a.T.dot(self.mat_w)
        for k in range(self.n_topic):
            self.mat_h[:, k] = self.mat_h[:, k] * mat_wtw[k, k] + mat_atw[:, k] - np.dot(self.mat_h, mat_wtw[:, k])
            self.mat_h[:, k] = np.maximum(self.mat_h[:, k], epss)

    def nmf_loss(self):
        loss = norm(self.mat_a - np.dot(self.mat_w, np.transpose(self.mat_h)), 'fro') ** 2 / 2.0
        return loss

    def get_loss(self):
        return np.array(self.loss_hist)

    def get_decomposition_matrix(self):
        return self.mat_w, self.mat_h
