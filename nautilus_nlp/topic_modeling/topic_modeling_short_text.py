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
import re
from collections import Counter
from itertools import product
from nautilus_nlp.topic_modeling.nmf_model import *
from nautilus_nlp.topic_modeling.seanmf_model import *
import numpy as np
import pyLDAvis


def prepare_data(text, vocab_min_count=1, vocab_max_size=10000):
    """
    :param text: list of str on which the topic modeling will be performed
    :param vocab_min_count: minimum number of occurrences of a word to be considered in the vocabulary
    :param vocab_max_size: maximum number of word in the vocabulary
    :return:  encoded_text_id: list of encoded sentences using vocab IDs
              vocab_list: list of vocabulary
              vocab_arr: array with vocab frequency counts
    """
    vocab = {}

    # Tokens_list is a list of sub-lists where each sub-list contains a sentences' tokens.
    tokens_list=[]
    for sentence in text:
        sentence = re.split('\s', sentence)
        tokens_list.append(sentence)
    vocab = dict(Counter(x for xs in tokens_list for x in xs))

    # Create Vocab array ( list of sorted vocab + counts )
    vocab_arr = [[wd, vocab[wd]] for wd in vocab if vocab[wd] > vocab_min_count]
    vocab_arr = sorted(vocab_arr, key=lambda k: k[1])[::-1]
    vocab_arr = vocab_arr[:vocab_max_size]
    vocab_arr = sorted(vocab_arr)

    vocab_list = list(map(lambda x:x[0], vocab_arr))
    # Create Vocab to ID dictionnary
    vocab2id = {itm[1][0]: itm[0] for itm in enumerate(vocab_arr)}

    # Create ID representation of text (ie: each sentence is a list of vocabId )
    encoded_text_id = []
    for sentence in text:
        sentence = re.split('\s', sentence)
        sentence = [int(vocab2id[wd]) for wd in sentence if wd in vocab2id]
        encoded_text_id.append(sentence)

    return encoded_text_id, vocab_list, vocab_arr


def train_shorttext_model(model_name, encoded_text_id, vocab_list, n_topics=20, max_iter=20, max_err=0.1, alpha=0, beta=0):
    """
    :param model_name: string = 'nmf' or 'seanmf'
    :param encoded_text_id: list of encoded sentences
    :param vocab_list: list of vocabulary
    :param n_topics: number of topics
    :param max_iter: maximum number of iterations while training
    :param max_err: training error
    :param alpha: regularization param for the NMF model
    :param beta: regularization param for the NMF model
    :return: Trained NMF model
    """

    n_docs = len(encoded_text_id)
    n_terms = len(vocab_list)

    if model_name == 'nmf':
        dt_mat = __build_doc_term_matrix(n_terms, n_docs, encoded_text_id)
        model = NMF(
            dt_mat,
            n_topic=n_topics,
            max_iter=max_iter,
            max_err=max_err)

    elif model_name == 'seanmf':
        # Calculate co-occurence matrix
        cm = __build_cooccurence_matrix(n_terms, encoded_text_id)
        # Calculate PPMI
        SS = __calulate_PPMI(cm, n_terms)
        # Build doc-term matrix
        dt_mat = __build_doc_term_matrix(n_terms, n_docs, encoded_text_id)
        model = SeaNMF(
            dt_mat, SS,
            alpha=alpha,
            beta=beta,
            n_topic=n_topics,
            max_iter=max_iter,
            max_err=max_err,
            fix_seed=1024)

    else:
        model = None
        print('Invalid model name: Use nmf or seanmf')

    return model


def __build_doc_term_matrix(n_terms, n_docs, encoded_text_id):
    dt_mat = np.zeros([n_terms, n_docs])
    for k in range(n_docs):
        for j in encoded_text_id[k]:
            dt_mat[j, k] += 1.0
    return dt_mat


def show_dominant_topic(model, encoded_text_id, vocab_list, n_topKeyword =10):
    """
    Computes the PMi score for each topic and the topKeywords describing each of them.
    :param model: trained NMF model
    :param encoded_text_id: list of encoded sentences
    :param vocab_list: list of vocabulary
    :return: topics = dictionnary with the topic number and its topkeywords
             pmi_score = dictionnary with the topic number and its PMI score
    """

    dt_mat = __build_cooccurence_matrix(n_terms=len(vocab_list), encoded_text_id=encoded_text_id)
    np.fill_diagonal(dt_mat, 0)
    W,_ = model.get_decomposition_matrix()
    n_topic = W.shape[1]
    PMI_arr = []
    for k in range(n_topic):
        top_keywords_index = W[:, k].argsort()[::-1][:n_topKeyword]
        PMI_arr.append(__calculate_PMI(dt_mat, top_keywords_index))

    index = np.argsort(PMI_arr)
    topics = {}
    pmi_score = {}
    for k in index:
        words = []
        for w in np.argsort(W[:, k])[::-1][:n_topKeyword]:
            words.append(vocab_list[w])
        # Complete the topic and the score dicts. Format {Topic_number: words or score}
        topics[k] = words
        pmi_score[k] = PMI_arr[k]

    return topics, pmi_score


def get_assigned_topics(model):
    """
    Assign the topic number to the sentences used when training the model
    :param model: trained model for short text
    :return topics_list: list having the same length as the training text containing topics assigned to each sentence.
    """

    _, H = model.get_decomposition_matrix()
    # The weights of the H matrix are converted into probabilities
    H_probs = H / H.sum(axis=1, keepdims=True)
    topics_list = list(np.argmax(H_probs, axis=1))

    return topics_list


def show_pyldavis(model, encoded_text_id, vocab_arr):
    """
    :param model: trained model
    :param encoded_text_id: encoded_text_id: list of encoded sentences
    :param vocab_arr: array of vocabulary frequency
    :return: pyldavis topics plot
    """

    data = prepare_data_pyldavis(model, encoded_text_id, vocab_arr)
    vis_data = pyLDAvis.prepare(**data)

    return pyLDAvis.display(vis_data)


def prepare_data_pyldavis(model, encoded_text_id, vocab_arr):
    """
    Transform the model decomposed matrix to create topic term and document topics matrices
    and prepare data to feed pyldavis.
    link : http://jeriwieringa.com/2018/07/17/pyLDAviz-and-Mallet/
    :return dict of data needed by pyldavis
    """

    # 1 List of documents lengths
    doc_length_values=[]
    for doc in encoded_text_id:
        doc_length_values.append(len(doc))
    # 2 List of vocab
    list_vocab = list(map(lambda x: x[0], vocab_arr))
    # 3 List of vocab. Frequency
    freq_vocab = list(map(lambda x: x[1], vocab_arr))
    W, H = model.get_decomposition_matrix()
    # Normlize the decomposition to get probabilities
    W_probs = W / W.sum(axis=1, keepdims=True)
    # 4 topic term matrix phi
    phi = W_probs.T
    # 5 document term matrix theta
    theta = H / H.sum(axis=1, keepdims=True)

    data = {'topic_term_dists': phi,
            'doc_topic_dists': theta,
            'doc_lengths': doc_length_values,
            'vocab': list_vocab,
            'term_frequency': freq_vocab
            }

    return data


def __build_cooccurence_matrix(n_terms, encoded_text_id):
    """
    The cooccurence matrix represents the number of times each word
    appeared in the same context as another word from the vocabulary.
    The matrix has n_terms x n_terms size, columns and rows denote the vocab.
    Cell values represent the number of times words occured together in the same sentence.
    :param :encoded_text_id : list of encoded sentences
    :return: res: the co-occurence matrix

    """
    res = np.zeros([n_terms, n_terms])
    for row in encoded_text_id:
        counts = Counter(row)
        for key_from, key_to in product(counts, repeat=2):
            res[key_from, key_to] += counts[key_from] * counts[key_to]
    return res


def __calulate_PPMI(cm, n_terms):
    D1 = np.sum(cm)
    print('D1= ', D1)
    SS = D1 * cm
    print('SS= ',SS)
    for k in range(n_terms):
        SS[k] /= np.sum(cm[k])
    for k in range(n_terms):
        SS[:, k] /= np.sum(cm[:, k])
    print('SS = ', SS )
    cm = []  # release memory
    SS[SS == 0] = 1.0
    SS = np.log(SS)
    SS[SS < 0.0] = 0.0
    return SS


def __build_doc_term_matrix(n_terms, n_docs, encoded_text_id):
    dt_mat = np.zeros([n_terms, n_docs])
    for k in range(n_docs):
        for j in encoded_text_id[k]:
            dt_mat[j, k] += 1.0
    return dt_mat


def __calculate_PMI(AA, topKeywordsIndex):
    '''
    Method to compute PMi score
    Reference:
    Short and Sparse Text Topic Modeling via Self-Aggregation
    '''

    D1 = np.sum(AA)
    n_tp = len(topKeywordsIndex)
    PMI = []
    for index1 in topKeywordsIndex:
        for index2 in topKeywordsIndex:
            if index2 < index1:
                if AA[index1, index2] == 0:
                    PMI.append(0.0)
                else:
                    C1 = np.sum(AA[index1])
                    C2 = np.sum(AA[index2])
                    PMI.append(np.log(AA[index1,index2]*D1/C1/C2))
    avg_PMI = 2.0*np.sum(PMI)/float(n_tp)/(float(n_tp)-1.0)

    return avg_PMI
