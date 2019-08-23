import re
from nmf_seanmf_models import *
import numpy as np

def data_preparation(text, vocab_min_count=1, vocab_max_size=10000):
    """
    This function expects a list of documents (sentences) and returns the needed data to
    make topic modeling for short text using NMF.
    :return:

    """

    vocab = {}
    for sentence in text:
        sentence = re.split('\s', sentence)
        for wd in sentence:
                try:
                    vocab[wd] += 1
                except:
                    vocab[wd] = 1
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


def train_model(model,n_docs, n_terms, docs, n_topics= 20, max_iter= 20, max_err=0.1, alpha = 0, beta=0):
    """
    :param model:
    :param n_docs:
    :param n_terms:
    :param docs:
    :param n_topics:
    :param max_iter:
    :param max_err:
    :param alpha:
    :param beta:
    :return:
    """
    if model == 'nmf':
        dt_mat = np.zeros([n_terms, n_docs])
        for k in range(n_docs):
            for j in docs[k]:
                dt_mat[j, k] += 1.0
        model = NMF(
            dt_mat,
            n_topic=n_topics,
            max_iter=max_iter,
            max_err=max_err)

    return model

## TEST

text = ['abs souscription ird abs collaborateur message bloquant finaliser merci selectionner un personne physique comme assurer principal',
'ref contrat af752001033 date heure creation avener non technique abs abs souscription ird collaborateur souhaiter repasser contrat mensuel selectionner bon rib car rib present sur contrat être errone celer cause impaye sur contrat',
'demande refair devis faire depuis im non traduire dans ab avec declanchement visa correction un message erreur',
'abs souscription ird souscription un affaire nouveau abs collab arriver pas finaliser son contrat']
encoded_text_id, vocab_list, vocab_arr = data_preparation(text)

print(encoded_text_id)

print(vocab_arr)

n_docs = len(encoded_text_id)
n_terms = len(vocab_list)
docs = encoded_text_id
vocab = vocab_list

x = train_model('nmf', n_docs, n_terms, docs)
W, H = x.get_decomposition_matrix()
