import time
import numpy as np
from numpy.linalg import norm
from tqdm import tqdm

'''
Topic Modeling via NMF
'''

class NMF(object):
    def __init__(
            self,
            A, IW=[], IH=[],
            n_topic=10, max_iter=100, max_err=1e-3,
            rand_init=True):
        """
        The objective of the NMF model is to approximate the term-document matrix A by two lower-rank matrices W and H.
        The process is iterative and we denote IW and IH the the matrix W and H that are updated at each step.

        :param A: The term-document matrix
        :param IW: topics Matrix, each column vector W(:,k) represents the k-th topic in terms of M keywords
        and its elements are the weights of the corresponding keywords.
        :param IH: The row vector H(j,:) is the latent representation for document j in terms of K topics
        :param n_topic: Number of selected topics
        :param max_iter: Maximum number of iterations to update W and H
        :param max_err: maximum error under which we consider that the loop converged
        :param rand_init: random init boolean
        """
        self.A = A
        self.n_row = A.shape[0]
        self.n_col = A.shape[1]

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
            self.W = np.random.random((self.n_row, self.n_topic))
            self.H = np.random.random((self.n_col, self.n_topic))
        else:
            self.W = IW
            self.H = IH
        for k in range(self.n_topic):
            self.W[:, k] /= norm(self.W[:, k])

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

        HtH = self.H.T.dot(self.H)
        AH = self.A.dot(self.H)
        for k in range(self.n_topic):
            tmpW = self.W[:, k] * HtH[k, k] + AH[:, k] - np.dot(self.W, HtH[:, k])
            self.W[:, k] = np.maximum(tmpW, epss)
            self.W[:, k] /= norm(self.W[:, k]) + epss

        WtW = self.W.T.dot(self.W)
        AtW = self.A.T.dot(self.W)
        for k in range(self.n_topic):
            self.H[:, k] = self.H[:, k] * WtW[k, k] + AtW[:, k] - np.dot(self.H, WtW[:, k])
            self.H[:, k] = np.maximum(self.H[:, k], epss)

    def nmf_loss(self):
        loss = norm(self.A - np.dot(self.W, np.transpose(self.H)), 'fro') ** 2 / 2.0
        return loss

    def get_loss(self):
        return np.array(self.loss_hist)

    def get_decomposition_matrix(self):
        return self.W, self.H
