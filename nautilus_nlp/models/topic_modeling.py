import gensim
import logging
import os
import pyLDAvis
import pyLDAvis.gensim 
from gensim.models import CoherenceModel
from gensim.models.wrappers import LdaMallet
import matplotlib.pyplot as plt

from IPython.display import HTML

logging.getLogger("gensim").setLevel(logging.WARNING)


def create_dictionary(data):
    
    """ Create a Dictionary encapsulates the mapping between normalized words and their integer ids.
    
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
        The produced corpus is a mapping of (token_id, token_count).
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

### Find Number of topics

def compute_coherence_values(dictionary, bow_corpus, texts, limit=25, start=2, step=4):
    """
    Compute c_v coherence for various number of topics

    /!\ It takes a really long time.

    Parameters:
    ----------
    dictionary : Gensim dictionary
    bow_corpus : Gensim bow corpus
    texts : List of input texts
    limit : Max num of topics

    Returns:
    -------
    model_list : List of LDA topic models
    coherence_values : Coherence values corresponding to the LDA model with respective number of topics
    """
    coherence_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        model = gensim.models.ldamodel.LdaModel(corpus=bow_corpus,
                                           id2word=dictionary,
                                          num_topics=num_topics, 
                                          random_state=0,
                                          update_every=5,
                                          chunksize=1000,
                                          passes=10)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())

    return model_list, coherence_values

def plot_optimal_topic_number(coherence_values, start=2, limit=25, step=4):
    """
    Plot the coherence scores per number of topics

    Parameters:
    ----------
    coherence_values : list of coherence scores for various number of topics
    start : int. Min num of topics
    limit : int. Max num of topics
    step: int

    Output:
    -------
    Lineplot
    """
    x = range(start, limit, step)
    plt.plot(x, coherence_values)
    plt.xlabel("Num Topics")
    plt.ylabel("Coherence score")
    plt.legend(("coherence_values"), loc='best')
    return plt.show()

def print_coherence_scores(coherence_values, start=2, limit=25, step=4):
    """
    Print the coherences scores for the ldamodels that had been tested with different number of topics
    """
    x = range(start, limit, step)
    for m, cv in zip(x, coherence_values):
        print("Num Topics =", m, " has Coherence Value of", round(cv, 4))


### LdaModel: Gensim & Mallet

def train_lda_model(bow_corpus, dictionary, num_topics, model='gensim', mallet_path=None, **kwargs):
    """ Train the lda model on the corpus
      
    Parameters
    ----------
    bow_corpus : iterable of list of tokens. Stream of document vectors or sparse matrix of shape (num_terms, num_documents).
    dictionary: corpora.Dictionary. Mapping from word IDs to words
    num_topics: int
    model : str. Precise the topic modeling model wanted, must be "gensim" or "mallet"
    mallet_path: str, optionnal if model='gensim', required if model='mallet'. Path to the mallet-2.0.8 file 
    
    Returns
    -------
    gensim.ldamodel
    """
    if model == 'gensim':
        model = train_lda_gensim(bow_corpus, dictionary, num_topics, **kwargs)
    elif model == 'mallet':
        if mallet_path is None:
            raise ValueError('You must precise the path to the mallet-2.0.8 file that has been downloaded before')
        else:
            model = train_lda_mallet(bow_corpus, dictionary, num_topics, mallet_path, **kwargs)
    else:
        raise ValueError('Please enter a valid model name: gensim or mallet')
    return model

def train_lda_gensim(bow_corpus, dictionary, num_topics, **kwargs):

    model = gensim.models.ldamodel.LdaModel(corpus=bow_corpus, id2word=dictionary, num_topics=num_topics, passes=10, minimum_probability=0.001, random_state=0, **kwargs)
    return model

def train_lda_mallet(bow_corpus, dictionary, num_topics, mallet_path, **kwargs):
    
    os.environ['MALLET_PATH'] = mallet_path
    mallet = '$MALLET_PATH/mallet-2.0.8/bin/mallet'
    model = gensim.models.wrappers.LdaMallet(mallet, corpus=bow_corpus, id2word=dictionary, num_topics=num_topics, prefix='composant', random_seed=0, **kwargs)
    return model


def save_model(model, model_name):
    """ Save the model that has been trained. The model will be saved on your current emplacement.
        
        Parameters
        ----------
        model: ldamodel
        model_name: str. Name the model that will be saved
    """
    return model.save(os.path.join(model_name))


def load_model(model_path,model_name, model='gensim', model_prefix='composant'):
    '''
    model : str. Precise the topic modeling model wanted, must be "gensim" or "mallet"
    model_path: str. path where the model has been saved
    model_name: str. name of the saved model
    model_prefix: str. By default, 'composant' default prefix used while saving the mallet model with train_lda_model function. 
    '''
    if model =='gensim':
        ldamodel = gensim.models.LdaModel.load(os.path.join(model_path,model_name))
    elif model =='mallet':
        ldamodel = LdaMallet.load(os.path.join(model_path,model_name))
        if model_prefix is not None:
            ldamodel.prefix = model_path+'/'+ model_prefix
    else:
        raise ValueError('Please enter a valid model name: gensim or mallet')
    return ldamodel

def fit_data(model, bow):
    """Test the model on new, unseen documents"""
    return model[bow]


# Visualization (only for gensim implementation for now)


def visualize_topics(model, bow_corpus, dictionary, model_type=None):
    """ Visualize the topics-keywords with the pyLDAvis interactive chart.
        (Work well in notebook)
        
    Parameters
    ----------
    model: LDA model: gensim or mallet
    bow_corpus : iterable of list of tokens. 
    dictionary: corpora.Dictionary. Dictionary encapsulates the mapping between normalized words and their integer ids.
    model : str. Precise the topic modeling model used, must be "gensim" or "mallet"
    
    Returns:
    ----------
    3D interactive chart
    
    """
    if model_type == 'mallet':
        model_vis = gensim.models.wrappers.ldamallet.malletmodel2ldamodel(model)
    elif model_type == 'gensim':
        model_vis = model
    elif model_type is None:
        raise ValueError('You forgot to precise your model type, it must be: gensim or mallet')
    else:
        raise ValueError('Please enter a valid model name: gensim or mallet') 
    return pyLDAvis.gensim.prepare(model_vis, bow_corpus, dictionary)

def save_pyldavis(pyldavis, vis_path, vis_name):
    """ Save the pyldavis interactive chart
    pyldavis: pyLDAvis._prepare.PreparedData
    vis_path: str
    vis_path: str
    """ 
    return pyLDAvis.save_html(pyldavis, os.path.join(vis_path, vis_name + '{}'.format('.html')))


def show_pyldavis(vis_path, vis_name):
    """ Display the HTML of the saved pyldavis interactive chart
    vis_path: str
    vis_path: str
    """
    return HTML(filename=os.path.join(vis_path, vis_name + '{}'.format('.html')))

def show_dominant_topic(model, bow_corpus, topic_number=1, topn=5):
    """ Print the dominant topics in the document, its score and the topics' top keywords.
    
    Quick way to interpret the topics

    Parameters
    ----------

    gensim.ldamodel
    model: ldamodel
    bow_corpus: iterable of list of tokens.
    topic_number: int. Pick the number of topics displayed
    topn: int. Number of topics' top keyword displayed

    """
    i = 0
    for index, score in sorted(model[bow_corpus], key=lambda tup: -1*tup[1]): 
        weight = model.show_topic(index, topn=topn)
        keywords = [i[0] for i in weight]
        print("Score: {}\t Topic: {}".format(score, keywords))
        i +=1
        if i == topic_number:
            break