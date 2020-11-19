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
from typing import List

import numpy as np
import pyLDAvis
from nautilus_nlp.topic_modeling.nmf_model import NMF
from nautilus_nlp.topic_modeling.seanmf_model import SeaNMF


def prepare_data(
    docs: List[str], vocab_min_count: int = 1, vocab_max_size: int = 10000
):
    """
    Parameters
    ----------
    docs : list
        list of sentences on which the topic modeling will be performed
    vocab_min_count : int
        minimum number of occurrences of a word to be considered in the vocabulary
    vocab_max_size : int
        maximum number of word in the vocabulary

    Returns
    -------
    list
        list of encoded sentences using vocab IDs
    list
        list of vocabulary
    Array
        array with vocab frequency counts
    """
    vocab = {}

    # Tokens_list is a list of sub-lists where each sub-list contains a sentences' tokens.
    tokens_list = []
    for sentence in docs:
        sentence = re.split(r"\s", sentence)
        tokens_list.append(sentence)
    vocab = dict(Counter(x for xs in tokens_list for x in xs))

    # Create Vocab array ( list of sorted vocab + counts )
    vocab_arr = [[wd, vocab[wd]] for wd in vocab if vocab[wd] > vocab_min_count]
    vocab_arr = sorted(vocab_arr, key=lambda k: k[1])[::-1]
    vocab_arr = vocab_arr[:vocab_max_size]
    vocab_arr = sorted(vocab_arr)

    vocab_list = list(map(lambda x: x[0], vocab_arr))
    # Create Vocab to ID dictionnary
    vocab2id = {itm[1][0]: itm[0] for itm in enumerate(vocab_arr)}

    # Create ID representation of text (ie: each sentence is a list of vocabId )
    encoded_text_id = []
    for sentence in docs:
        sentence = re.split(r"\s", sentence)
        sentence = [int(vocab2id[wd]) for wd in sentence if wd in vocab2id]
        encoded_text_id.append(sentence)

    return encoded_text_id, vocab_list, vocab_arr


def train_shorttext_model(
    model_name: str,
    encoded_text_id: list,
    vocab_list: list,
    n_topics: int = 20,
    max_iter: int = 20,
    max_err: float = 0.1,
    alpha: float = 0,
    beta: float = 0,
):
    """
    Parameters
    ----------
    model_name : str {'nmf','seanmf'}
    encoded_text_id : list
        list of encoded sentences
    vocab_list : list
        list of vocabulary
    n_topics : int
        number of topics
    max_iter : int
        maximum number of iterations while training
    max_err : float
        training error
    alpha : float
        regularization param for the NMF model
    beta : float
        regularization param for the NMF model

    Returns
    -------
    Trained NMF model

    Raises
    ------
    ValueError
        If model_name is not valid
    """

    n_docs = len(encoded_text_id)
    n_terms = len(vocab_list)

    if model_name == "nmf":
        dt_mat = __build_doc_term_matrix(n_terms, n_docs, encoded_text_id)
        return NMF(
            dt_mat,
            mat_iw=[],
            mat_ih=[],
            n_topic=n_topics,
            max_iter=max_iter,
            max_err=max_err,
        )

    if model_name == "seanmf":
        # Calculate co-occurence matrix
        cooc_mat = __build_cooccurence_matrix(n_terms, encoded_text_id)
        # Calculate PPMI
        mat_ss = __calculate_ppmi(cooc_mat, n_terms)
        # Build doc-term matrix
        dt_mat = __build_doc_term_matrix(n_terms, n_docs, encoded_text_id)
        return SeaNMF(
            dt_mat,
            mat_ss,
            mat_iw=[],
            mat_iwc=[],
            mat_ih=[],
            alpha=alpha,
            beta=beta,
            n_topic=n_topics,
            max_iter=max_iter,
            max_err=max_err,
            fix_seed=1024,
        )
    raise ValueError("Invalid model name: Use nmf or seanmf")


def show_dominant_topic(
    model, encoded_text_id: list, vocab_list: list, n_top_keyword: int = 10
):
    """
    Computes the PMi score for each topic and the topKeywords describing each of them.

    Parameters
    ----------
    - model
        trained NMF model
    - encoded_text_id : list
        list of encoded sentences
    - vocab_list : list
        list of vocabulary
    - n_top_keyword : list
        the number of keywords to be returned

    Returns
    -------
    dict
        A dictionnary with the topic number and its top keywords
    dict
        A ictionnary with the topic number and its PMI score
    """
    dt_mat = __build_cooccurence_matrix(
        n_terms=len(vocab_list), encoded_text_id=encoded_text_id
    )
    np.fill_diagonal(dt_mat, 0)
    mat_w, _ = model.get_decomposition_matrix()
    n_topic = mat_w.shape[1]
    pmi_arr = []
    for k in range(n_topic):
        top_keywords_index = mat_w[:, k].argsort()[::-1][:n_top_keyword]
        pmi_arr.append(__calculate_pmi(dt_mat, top_keywords_index))

    index = np.argsort(pmi_arr)
    topics = {}
    pmi_score = {}
    for k in index:
        words = []
        for w in np.argsort(mat_w[:, k])[::-1][:n_top_keyword]:
            words.append(vocab_list[w])
        # Complete the topic and the score dicts. Format {Topic_number: words or score}
        topics[k] = words
        pmi_score[k] = pmi_arr[k]

    return topics, pmi_score


def get_assigned_topics(model):
    """
    Assign the topic number to the sentences used when training the model

    Parameters
    ----------    
    model
        trained model for short text
    
    Returns
    -------
    list
        list of topics. Having the same length as the training text containing topics assigned \
        to each sentence.
    """
    _, mat_h = model.get_decomposition_matrix()
    # The weights of the H matrix are converted into probabilities
    h_probs = mat_h / mat_h.sum(axis=1, keepdims=True)
    topics_list = list(np.argmax(h_probs, axis=1))

    return topics_list


def show_pyldavis(model, encoded_text_id, vocab_arr):
    """
    Parameters
    ----------
    model
        trained model
    encoded_text_id
        encoded_text_id: list of encoded sentences
    vocab_arr
        array of vocabulary frequency

    Returns
    -------
    pyldavis topics plot
    """

    data = prepare_data_pyldavis(model, encoded_text_id, vocab_arr)
    vis_data = pyLDAvis.prepare(**data)

    return pyLDAvis.display(vis_data)


def prepare_data_pyldavis(model, encoded_text_id, vocab_arr) -> dict:
    """
    Transform the model decomposed matrix to create topic term and document topics matrices
    and prepare data to feed pyldavis.
    link : http://jeriwieringa.com/2018/07/17/pyLDAviz-and-Mallet/

    Returns
    -------
    dict
        dict of data needed by pyldavis
    """
    doc_length_values = [len(doc) for doc in encoded_text_id]
    list_vocab = list(map(lambda x: x[0], vocab_arr))
    freq_vocab = list(map(lambda x: x[1], vocab_arr))
    mat_w, mat_h = model.get_decomposition_matrix()
    # Normlize the decomposition to get probabilities
    w_probs = mat_w / mat_w.sum(axis=1, keepdims=True)
    # Topic-term matrix phi
    phi = w_probs.T
    # Document-term matrix theta
    theta = mat_h / mat_h.sum(axis=1, keepdims=True)
    return {
        "topic_term_dists": phi,
        "doc_topic_dists": theta,
        "doc_lengths": doc_length_values,
        "vocab": list_vocab,
        "term_frequency": freq_vocab,
    }


def __build_cooccurence_matrix(n_terms: int, encoded_text_id: list):
    """
    The cooccurence matrix represents the number of times each word
    appeared in the same context as another word from the vocabulary.
    The matrix has n_terms x n_terms size, columns and rows denote the vocab.
    Cell values represent the number of times words occured together in the same sentence.

    Parameters
    ----------
    n_terms : int
    encoded_text_id : list
        list of encoded sentences

    Returns
    -------
    co-occurence matrix
    """
    res = np.zeros([n_terms, n_terms])
    for row in encoded_text_id:
        counts = Counter(row)
        for key_from, key_to in product(counts, repeat=2):
            res[key_from, key_to] += counts[key_from] * counts[key_to]
    return res


def __calculate_ppmi(cooc_mat, n_terms):
    mat_d1 = np.sum(cooc_mat)
    print("D1= ", mat_d1)
    mat_ss = mat_d1 * cooc_mat
    print("SS= ", mat_ss)
    for k in range(n_terms):
        mat_ss[k] /= np.sum(cooc_mat[k])
    for k in range(n_terms):
        mat_ss[:, k] /= np.sum(cooc_mat[:, k])
    print("SS = ", mat_ss)
    cooc_mat = []  # release memory
    mat_ss[mat_ss == 0] = 1.0
    mat_ss = np.log(mat_ss)
    mat_ss[mat_ss < 0.0] = 0.0
    return mat_ss


def __build_doc_term_matrix(n_terms, n_docs, encoded_text_id):
    dt_mat = np.zeros([n_terms, n_docs])
    for k in range(n_docs):
        for j in encoded_text_id[k]:
            dt_mat[j, k] += 1.0
    return dt_mat


def __calculate_pmi(mat_aa, top_keywords_index):
    """
    Method to compute PMi score
    Reference: Short and Sparse Text Topic Modeling via Self-Aggregation
    """
    mat_d1 = np.sum(mat_aa)
    n_tp = len(top_keywords_index)
    mat_pmi = []
    for index1 in top_keywords_index:
        for index2 in top_keywords_index:
            if index2 < index1:
                if mat_aa[index1, index2] == 0:
                    mat_pmi.append(0.0)
                else:
                    mat_c1 = np.sum(mat_aa[index1])
                    mat_c2 = np.sum(mat_aa[index2])
                    mat_pmi.append(
                        np.log(mat_aa[index1, index2] * mat_d1 / mat_c1 / mat_c2)
                    )
    avg_pmi = 2.0 * np.sum(mat_pmi) / float(n_tp) / (float(n_tp) - 1.0)
    return avg_pmi
