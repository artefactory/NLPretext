import gensim
import logging
import os
import pyLDAvis
import pyLDAvis.gensim 

from IPython.display import HTML

logging.getLogger("gensim").setLevel(logging.WARNING)


def create_dictionary(data):
    
    """ Create a dictionary(id2word) containing the number of times a word appears 
    in the dataset set: one of the two main inputs to the LDA topic model with the corpus
    
    Parameters
    ----------
    data : list of list of tokens
       
    Returns
    -------
    list of list of tuples
    """
    return gensim.corpora.Dictionary(data)

def filter_extremes(dictionary, no_below=15, no_above=0.3 , **kwargs) :
    """ Remove very rare and very common words

    Parameters
    ----------
    dictionary: dictionary containing the number of times a word appears in the dataset set
    no_below : int, optional
    Keep tokens which are contained in at least `no_below` documents.
    no_above : float, optional
    Keep tokens which are contained in no more than `no_above` documents
    (fraction of total corpus size, not an absolute number).

    (Add to docstring) + other func
    """
    return dictionary.filter_extremes(no_below=no_below, no_above=no_above, **kwargs)


def create_bow_corpus(data, dictionary):
    
    """ Create the corpus: one of the two main inputs to the LDA topic model with the dictionary (id2word)
        The produced corpus is a mapping of (word_id, word_frequency).
    Parameters
    ----------
    data : list of list of tokens
       
    Returns
    -------
    list of list of tuples
    """
    texts = data
    corpus = [dictionary.doc2bow(text) for text in texts]
    return corpus

### Gensim LdaModel

def train_lda_model(bow_corpus, dictionary, num_topics, **kwargs):
    """ Train the model on the corpus
      
    Parameters
    ----------
    corpus : iterable of list of tokens. Stream of document vectors or sparse matrix of shape (num_terms, num_documents).$
    dictionary: corpora.Dictionary. Mapping from word IDs to words
    num_topics: int
    
    Returns
    -------
    gensim.ldamodel
    """
    model = gensim.models.ldamodel.LdaModel(corpus=bow_corpus, id2word=dictionary, num_topics=num_topics, passes=10, minimum_probability=0.001, random_state=0)
    return model


def save_model(model, MODELNAME):
    """ Save the model that has been trained
        
        Parameters
        ----------
        model: ldamodel
        MODELNAME: str
    """
    return model.save(MODELNAME)


def load_model(model_path,model_name):
    '''
    model_path: path where the model has been saved
    model_name: name of the saved model
    '''
    ldamodel = gensim.models.LdaModel.load(os.path.join(model_path,model_name))
    return ldamodel

def fit_data(model, bow):
    """Test the model on new, unseen documents"""
    return model[bow]

### Gensim LdaMallet

def load_mallet_model(model_path, model_name, model_prefix=None):
    '''
    model_prefix: prefix used while saving the model
    model_name: name of the saved model
    '''
    ldamodel = LdaMallet.load(os.path.join(model_path,model_name))
    if model_prefix is not None:
        ldamodel.prefix = model_path+'/'+ model_prefix
    return ldamodel

def train_mallet_model(mallet_path, bow_corpus, dictionary, num_topics, **kwargs):
    """ Train the model on the corpus
      
    Parameters
    ----------
    mallet_path: path to mallet files
    bow_corpus : iterable of list of tokens. Stream of document vectors or sparse matrix of shape (num_terms, num_documents).$
    dictionary: corpora.Dictionary. Mapping from word IDs to words
    num_topics: int
    
    Returns
    -------
    gensim.ldamodel
    """
    model = gensim.models.wrappers.LdaMallet(mallet_path, corpus=bow_corpus, id2word=dictionary, num_topics=num_topics, prefix='nautil')
    return model


# Visualization


def visualize_topics(model, bow_corpus, dictionary):
    """ Visualize the topics-keywords with the pyLDAvis interactive chart.
        (Work well in notebook)
    """
    return pyLDAvis.gensim.prepare(model, bow_corpus, dictionary)


def save_pyldavis(pyldavis, vis_path, vis_name):
    """ Save the pyldavis interactive chart
    pyldavis: pyLDAvis._prepare.PreparedData
    vis_path: str
    vis_path: str
    """ 
    return pyLDAvis.save_html(pyldavis, os.path.join(vis_path, vis_name, '.html'))


def show_pyldavis(vis_path, vis_name):
    return HTML(filename=os.path.join(vis_path, vis_name, '.html'))

