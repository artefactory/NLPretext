
import time
import numpy as np
from numpy.linalg import norm
from tqdm import tqdm


class SeaNMF(object):
    def __init__(
            self,
            A, S,
            IW=[], IWc=[], IH=[],
            alpha=1.0, beta=0.1, n_topic=10, max_iter=100, max_err=1e-3,
            rand_init=True, fix_seed=False):
        """
        Seanmf is a topic modeling algorithm, paper:  http://dmkd.cs.vt.edu/papers/WWW18.pdf.
        It finds an approximation to the term-document matrix A by two lower-rank matrices W and H,
        at each iteration a context matrix Wc are computed and used to update W.
        :param A: document term matrix
        :param S: Word-context (semantic) correlation matrix
        :param IW: topics Matrix, each column vector W(:,k) represents the k-th topic in terms of M keywords
        and its elements are the weights of the corresponding keywords.
        :param IWc: Latent factor matrix of contexts.
        :param IH: The row vector H(j,:) is the latent representation for document j in terms of K topics
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

        self.A = A
        self.S = S

        self.n_row = A.shape[0]
        self.n_col = A.shape[1]

        self.n_topic = n_topic
        self.max_iter = max_iter
        self.alpha = alpha
        self.beta = beta
        self.B = np.ones([self.n_topic, 1])
        self.max_err = max_err
        self.snmf_mat_init(rand_init, IW,  IWc, IH)
        self.snmf_iter()

    def snmf_mat_init(self, rand_init, IW=[], IWc=[], IH=[]):
        """
        Init Matrices W,Wc and H initially either randomly or using existing IW,IWc IH matrices taken when iterating.
        :param rand_init: Boolean indicating initial random init
        """
        if rand_init:
            self.W = np.random.random((self.n_row, self.n_topic))
            self.Wc = np.random.random((self.n_row, self.n_topic))
            self.H = np.random.random((self.n_col, self.n_topic))
        else:
            self.W = IW
            self.Wc = IWc
            self.H = IH
        for k in range(self.n_topic):
            self.W[:, k] /= norm(self.W[:, k])
            self.Wc[:, k] /= norm(self.Wc[:, k])

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
        Alogorithm 1: Equations to update W, wc, H are described in the paper
        http://dmkd.cs.vt.edu/papers/WWW18.pdf
        '''

        epss = 1e-20
        # Update W
        AH = np.dot(self.A, self.H)
        SWc = np.dot(self.S, self.Wc)
        HtH = np.dot(self.H.T, self.H)
        WctWc = np.dot(self.Wc.T, self.Wc)
        W1 = self.W.dot(self.B)

        for k in range(self.n_topic):
            num0 = HtH[k, k] * self.W[:, k] + self.alpha * WctWc[k, k] * self.W[:, k]
            num1 = AH[:, k] + self.alpha * SWc[:, k]
            num2 = np.dot(self.W, HtH[:, k]) + self.alpha * np.dot(self.W, WctWc[:, k]) + self.beta * W1[0]
            self.W[:, k] = num0 + num1 - num2
            self.W[:, k] = np.maximum(self.W[:, k], epss)  # project > 0
            self.W[:, k] /= norm(self.W[:, k]) + epss  # normalize
        # Update Wc
        WtW = self.W.T.dot(self.W)
        StW = np.dot(self.S, self.W)
        for k in range(self.n_topic):
            self.Wc[:, k] = self.Wc[:, k] + StW[:, k] - np.dot(self.Wc, WtW[:, k])
            self.Wc[:, k] = np.maximum(self.Wc[:, k], epss)
        # Update H
        AtW = np.dot(self.A.T, self.W)
        for k in range(self.n_topic):
            self.H[:, k] = self.H[:, k] + AtW[:, k] - np.dot(self.H, WtW[:, k])
            self.H[:, k] = np.maximum(self.H[:, k], epss)

    def snmf_loss(self):
        loss = norm(self.A - np.dot(self.W, np.transpose(self.H)), 'fro') ** 2 / 2.0
        if self.alpha > 0:
            loss += self.alpha * norm(np.dot(self.W, np.transpose(self.Wc)) - self.S, 'fro') ** 2 / 2.0
        if self.beta > 0:
            loss += self.beta * norm(self.W, 1) ** 2 / 2.0

        return loss

    def get_decomposition_matrix(self):
        # Wc was not considered to keep same structure as NMF
        return self.W, self.H


