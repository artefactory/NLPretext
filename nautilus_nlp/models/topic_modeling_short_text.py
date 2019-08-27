import re
from nmf_seanmf_models import *
import numpy as np

def data_preparation(text, vocab_min_count=1, vocab_max_size=10000):
    """
    This function expects a list of documents (sentences) and returns the needed data to
    make topic modeling for short text using NMF model.
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


def train_model(model, encoded_text_id, vocab_list, n_topics= 20, max_iter= 20, max_err=0.1, alpha = 0, beta=0):
    """
    :param model:
    :param docs:
    :param n_topics:
    :param max_iter:
    :param max_err:
    :param alpha:
    :param beta:
    :return:
    """

    n_docs = len(encoded_text_id)
    n_terms = len(vocab_list)

    if model == 'nmf':
        dt_mat = np.zeros([n_terms, n_docs])
        for k in range(n_docs):
            for j in encoded_text_id[k]:
                dt_mat[j, k] += 1.0
        model = NMF(
            dt_mat,
            n_topic=n_topics,
            max_iter=max_iter,
            max_err=max_err)

    return model


def show_dominant_topic(model, encoded_text_id, vocab_list, n_topKeyword =10):
    """
    Computes the PMi score for each topic and the topKeywords describing each of them.
    :param model:
    :param encoded_text_id:
    :param vocab_list:
    :return: topics = dictionnary with the topic number and its topkeywords
             pmi_score = dictionnary with the topic number and its PMI score
    """

    dt_mat = __build_cooccurence_matrix(n_terms=len(vocab_list), encoded_text_id=encoded_text_id)
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
    :param model: trained model
    :return topics_list: list having the same length as the training text containing topics assigned to each sentence.
    """
    _, H = model.get_decomposition_matrix()
    H_probs = H / H.sum(axis=1, keepdims=True)
    topics_list = list(np.argmax(H_probs, axis=1) + 1)
    return topics_list


def __build_cooccurence_matrix(n_terms, encoded_text_id):
    dt_mat = np.zeros([n_terms, n_terms])
    for itm in encoded_text_id:
        for kk in itm:
            for jj in itm:
                if kk != jj:
                    dt_mat[int(kk), int(jj)] += 1.0
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

## TEST

text = ['abs souscription ird abs collaborateur message bloquant finaliser merci selectionner un personne physique comme assurer principal',
'ref contrat af752001033 date heure creation avener non technique abs abs souscription ird collaborateur souhaiter repasser contrat mensuel selectionner bon rib car rib present sur contrat être errone celer cause impaye sur contrat',
'demande refair devis faire depuis im non traduire dans ab avec declanchement visa correction un message erreur',
'abs souscription ird souscription un affaire nouveau abs collab arriver pas finaliser son contrat']
encoded_text_id, vocab_list, vocab_arr = data_preparation(text)

#print(encoded_text_id)
#print(vocab_arr)

x = train_model('nmf', encoded_text_id, vocab_list, n_topics= 3)
topics, pmi_score = show_dominant_topic(x, encoded_text_id, vocab_list, n_topKeyword =10)

print(topics)

print(pmi_score)

list_of_topics= get_assigned_topics(x)
print(list_of_topics)
