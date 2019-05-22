import spacy
from gensim.corpora import Dictionary
from gensim.models.tfidfmodel import TfidfModel
from gensim import corpora, models, similarities
from gensim.matutils import sparse2full
import numpy as np
import math

from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer


class Tfidf(object):
    """
    Inputs a list of string. 
    and the list of feature name.
    Wrapper of https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html

    Parameters
    ----------
    input=’content’, encoding=’utf-8’, decode_error=’strict’, strip_accents=None,
    lowercase=True, preprocessor=None, tokenizer=None, analyzer=’word’,
    stop_words=None, token_pattern=’(?u)\b\w\w+\b’, ngram_range=(1, 1),
    max_df=1.0, min_df=1, max_features=None, vocabulary=None, binary=False,
    dtype=<class ‘numpy.float64’>, norm=’l2’, use_idf=True, smooth_idf=True, sublinear_tf=False

    Returns
    -------
    list
        Outputs a tuple with the wordcount vector matrix
    """
    
    def __init__(self, **kwargs):
        self.tfidf_vectorizer = TfidfVectorizer(**kwargs)
    
    def _compute_wordcount_vector(self, documents):
        '''
        Input a list of documents (string)
        Output the wordcount vector matrix 
        '''
        self.word_count_vector = self.tfidf_vectorizer.fit_transform(documents)
        return self.word_count_vector
    

    def _get_features_name(self):
        self.feature_names = self.tfidf_vectorizer.get_feature_names()
        return self.feature_names

    
    def _compute_idf(self):
        self.tfidf_transformer=TfidfTransformer(smooth_idf=True, use_idf=True)
        self.tfidf_transformer.fit(self.word_count_vector)
        return self.word_count_vector

    
    def compute_tfidf(self, documents):
        self._compute_wordcount_vector(documents)
        self._get_features_name()
        self._compute_idf()
        return self.word_count_vector


    def transform_doc(self, document):
        '''
        Transform documents to document-term matrix.

        Returns
        -------
        Tf-idf-weighted document-term matrix.
        '''
        return self.tfidf_transformer.transform(document)

    def _apply_tfidf_to_doc(self, text):
        '''generate tf-idf for the given document'''
        return self.tfidf_transformer.transform(self.tfidf_vectorizer.transform([text]))
    
    
    def _sort_coo(self, coo_matrix):
        '''sort the tf-idf vectors by descending order of scores'''
        tuples = zip(coo_matrix.col, coo_matrix.data)
        return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)
    
    
    def _extract_topn_from_vector(self, feature_names, sorted_items, topn=10):
        """get the feature names and tf-idf score of top n items"""

        #use only topn items from vector
        sorted_items = sorted_items[:topn]

        score_vals = []
        feature_vals = []

        # word index and corresponding tf-idf score
        for idx, score in sorted_items:

            #keep track of feature name and its corresponding score
            score_vals.append(round(score, 3))
            feature_vals.append(feature_names[idx])

        #create a tuples of feature,score
        #results = zip(feature_vals,score_vals)
        results= {}
        for idx in range(len(feature_vals)):
            results[feature_vals[idx]]=score_vals[idx]

        return results

    
    def get_top_tfidf_per_doc(self, text, n=10):
        '''compute TF-IDF for a given doc, and returns a list of the top N weighted words'''
        tf_idf_vector= self._apply_tfidf_to_doc(text)
        sorted_items=self._sort_coo(tf_idf_vector.tocoo())
        return list(self._extract_topn_from_vector(self.feature_names, sorted_items, n).keys())
    
    def get_top_tfidf(self, n=10):
        '''returns a dict of the top N weighted words, with their weight'''
        return self._extract_topn_from_vector(self.feature_names, self._sort_coo(self.word_count_vector.tocoo()), topn=n)


class Text_Vectorizer(object):
    '''
    TODO: DOCSTRING
    '''
    def __init__(self, doc_list):
        # Initialize
        self.doc_list = doc_list
        self.nlp, self.docs, self.docs_dict = self._preprocess(self.doc_list)

    # Functions to lemmatise docs
    def _keep_token(self, t):
        return t.is_alpha and not (t.is_space or t.is_punct or t.is_stop or t.like_num)

    def _lemmatize_doc(self, doc):
        return [t.lemma_ for t in doc if self._keep_token(t)]

    # Gensim to create a dictionary and filter out stop and infrequent words (lemmas).
    def _get_docs_dict(self, docs):
        docs_dict = Dictionary(docs)
        # CAREFUL: For small corpus please carefully modify the parameters for filter_extremes, or simply comment it out.
        docs_dict.filter_extremes(no_below=5, no_above=0.2)
        docs_dict.compactify()
        return docs_dict

    # Preprocess docs
    def _preprocess(self, doc_list):
        # Load spacy model
        nlp = spacy.load("en")
        # lemmatise docs
        docs = [self._lemmatize_doc(nlp(doc)) for doc in doc_list]
        # Get docs dictionary
        docs_dict = self._get_docs_dict(docs)
        return nlp, docs, docs_dict

    # Gensim can again be used to create a bag-of-words representation of each document,
    # build the TF-IDF model,
    # and compute the TF-IDF vector for each document.
    def _get_tfidf(self, docs, docs_dict):
        docs_corpus = [docs_dict.doc2bow(doc) for doc in docs]
        model_tfidf = TfidfModel(docs_corpus, id2word=docs_dict)
        docs_tfidf = model_tfidf[docs_corpus]
        docs_vecs = np.vstack([sparse2full(c, len(docs_dict)) for c in docs_tfidf])
        return docs_vecs

    # Get avg w2v for one document
    def _document_vector(self, doc, docs_dict, nlp):
        # remove out-of-vocabulary words
        doc_vector = [nlp(word).vector for word in doc if word in docs_dict.token2id]
        return np.mean(doc_vector, axis=0)


    # Get average vector for document list
    def avg_wv(self):
        docs_vecs = np.vstack(
            [self._document_vector(doc, self.docs_dict, self.nlp) for doc in self.docs]
        )
        return docs_vecs

    # Get TF-IDF vector for document list
    def get_tfidf(self):
        docs_corpus = [self.docs_dict.doc2bow(doc) for doc in self.docs]
        model_tfidf = TfidfModel(docs_corpus, id2word=self.docs_dict)
        docs_tfidf = model_tfidf[docs_corpus]
        docs_vecs = np.vstack([sparse2full(c, len(self.docs_dict)) for c in docs_tfidf])
        return docs_vecs

    # Get Latent Semantic Indexing(LSI) vector for document list
    def get_lsi(self, num_topics=300):
        docs_corpus = [self.docs_dict.doc2bow(doc) for doc in self.docs]
        model_lsi = models.LsiModel(docs_corpus, num_topics, id2word=self.docs_dict)
        docs_lsi = model_lsi[docs_corpus]
        docs_vecs = np.vstack([sparse2full(c, len(self.docs_dict)) for c in docs_lsi])
        return docs_vecs

    # Get Random Projections(RP) vector for document list
    def get_rp(self):
        docs_corpus = [self.docs_dict.doc2bow(doc) for doc in self.docs]
        model_rp = models.RpModel(docs_corpus, id2word=self.docs_dict)
        docs_rp = model_rp[docs_corpus]
        docs_vecs = np.vstack([sparse2full(c, len(self.docs_dict)) for c in docs_rp])
        return docs_vecs

    # Get Latent Dirichlet Allocation(LDA) vector for document list
    def get_lda(self, num_topics=100):
        docs_corpus = [self.docs_dict.doc2bow(doc) for doc in self.docs]
        model_lda = models.LdaModel(docs_corpus, num_topics, id2word=self.docs_dict)
        docs_lda = model_lda[docs_corpus]
        docs_vecs = np.vstack([sparse2full(c, len(self.docs_dict)) for c in docs_lda])
        return docs_vecs

    # Get Hierarchical Dirichlet Process(HDP) vector for document list
    def get_hdp(self):
        docs_corpus = [self.docs_dict.doc2bow(doc) for doc in self.docs]
        model_hdp = models.HdpModel(docs_corpus, id2word=self.docs_dict)
        docs_hdp = model_hdp[docs_corpus]
        docs_vecs = np.vstack([sparse2full(c, len(self.docs_dict)) for c in docs_hdp])
        return docs_vecs
