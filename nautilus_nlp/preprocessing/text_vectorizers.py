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
import spacy
from gensim.corpora import Dictionary
from gensim.models.tfidfmodel import TfidfModel
from gensim import corpora, models, similarities
from gensim.matutils import sparse2full
import numpy as np
import math

from sklearn.feature_extraction.text import TfidfVectorizer as _TfidfVectorizer


class TfidfTextVectorizer(object):
    """
    Convert a collection of raw documents to a matrix of TF-IDF features.

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
    """
    
    def __init__(self, **kwargs):
        self.tfidf_vectorizer = _TfidfVectorizer(**kwargs)


    def _get_features_name(self):
        '''
        Array mapping from feature integer indices to feature name
        '''
        self.feature_names = self.tfidf_vectorizer.get_feature_names()
        return self.feature_names


    def compute_tfidf(self, raw_documents):
        '''
        Learn vocabulary and idf, return term-document matrix.

        Input a list of documents (string)
        Output the wordcount vector matrix.

        params
        ------
        raw_documents : iterable
            an iterable which yields either str, unicode or file objects

        returns
        -------
        X : sparse matrix, [n_samples, n_features]
            Tf-idf-weighted document-term matrix.
        '''
        self.word_count_vector = self.tfidf_vectorizer.fit_transform(raw_documents)
        self._get_features_name()
        return self.word_count_vector    


    def apply_tfidf_to_documents(self, raw_document):
        '''
        Apply the tf-idf weights to a document or a list of documents.
        Equivalent to .transform() method in sci-kit learn.
        
        Uses the vocabulary and document frequencies (df) learned by fit 
        (or fit_transform), and convert documents to document-term matrix.

        parameters
        ---------
        raw_documents : iterable or document
            an iterable which yields either str, unicode or file objects, or 
        a string.

        Returns
        -------
        X : sparse matrix, [n_samples, n_features]
            Tf-idf-weighted document-term matrix.
        '''
        if type(raw_document) == str:
            raw_document = [raw_document]
        return self.tfidf_vectorizer.transform(raw_document)
    
    
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


    def get_top_tfidf_per_doc(self, text:str, n:int=10)->list:
        '''
        compute TF-IDF for a given doc, and returns a list of the top N weighted words

        parameters
        ---------
        text : sparse matrix, [n_samples, n_features]
            If specified, will return the top weighted words for the given matrix,
            otherwise will give the result of the tf-idf matrix
        a string.

        n : number of terms to display

        Returns
        -------
        top-n weighted terms : dict
            List of top terms for the given document
        '''
        tf_idf_vector= self.apply_tfidf_to_documents([text])
        sorted_items=self._sort_coo(tf_idf_vector.tocoo())
        return list(self._extract_topn_from_vector(self.feature_names, sorted_items, n).keys())
    

    def get_top_tfidf(self, tfidf_matrix=None, n:int=10)->list:
        '''
        Input a tf-idf matrix, and returns a dict of the top N weighted words,
        with their weight.

        parameters
        ---------
        tfidf_matrix : sparse matrix, [n_samples, n_features]
            If specified, will return the top weighted words for the given matrix,
            otherwise will give the result of the tf-idf matrix
        a string.

        Returns
        -------
        top-n weighted terms : dict
            Dict of top terms and their associated weighted.
        '''
        if tfidf_matrix is None:
            tfidf_matrix = self.word_count_vector
        return self._extract_topn_from_vector(self.feature_names, self._sort_coo(tfidf_matrix.tocoo()), topn=n)


class GensimTextVectorizer(object):
    '''
    Gensim's implementation of TF-IDF, BOW models etc. 
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


    def _get_tfidf(self, docs, docs_dict):
        '''
        Gensim can again be used to create a bag-of-words representation of each document,
        Build the TF-IDF model, and compute the TF-IDF vector for each document.
        '''
        docs_corpus = [docs_dict.doc2bow(doc) for doc in docs]
        model_tfidf = TfidfModel(docs_corpus, id2word=docs_dict)
        docs_tfidf = model_tfidf[docs_corpus]
        docs_vecs = np.vstack([sparse2full(c, len(docs_dict)) for c in docs_tfidf])
        return docs_vecs

    def _document_vector(self, doc, docs_dict, nlp):
        """
        Get avg w2v for one document. Remove out-of-vocabulary words.
        """
        
        doc_vector = [nlp(word).vector for word in doc if word in docs_dict.token2id]
        return np.mean(doc_vector, axis=0)


    def avg_wv(self):
        '''
        Get average vector for document list
        '''
        docs_vecs = np.vstack(
            [self._document_vector(doc, self.docs_dict, self.nlp) for doc in self.docs]
        )
        return docs_vecs


    def get_tfidf(self):
        '''
        Get TF-IDF vector for document list
        '''
        docs_corpus = [self.docs_dict.doc2bow(doc) for doc in self.docs]
        model_tfidf = TfidfModel(docs_corpus, id2word=self.docs_dict)
        docs_tfidf = model_tfidf[docs_corpus]
        docs_vecs = np.vstack([sparse2full(c, len(self.docs_dict)) for c in docs_tfidf])
        return docs_vecs

    
    def get_lsi(self, num_topics=300):
        '''
        Get Latent Semantic Indexing(LSI) vector for document list
        '''
        docs_corpus = [self.docs_dict.doc2bow(doc) for doc in self.docs]
        model_lsi = models.LsiModel(docs_corpus, num_topics, id2word=self.docs_dict)
        docs_lsi = model_lsi[docs_corpus]
        docs_vecs = np.vstack([sparse2full(c, len(self.docs_dict)) for c in docs_lsi])
        return docs_vecs

    
    def get_rp(self):
        '''
        Get Random Projections(RP) vector for document list
        '''
        docs_corpus = [self.docs_dict.doc2bow(doc) for doc in self.docs]
        model_rp = models.RpModel(docs_corpus, id2word=self.docs_dict)
        docs_rp = model_rp[docs_corpus]
        docs_vecs = np.vstack([sparse2full(c, len(self.docs_dict)) for c in docs_rp])
        return docs_vecs

    def get_lda(self, num_topics=100):
        '''
        Get Latent Dirichlet Allocation(LDA) vector for document list
        '''
        docs_corpus = [self.docs_dict.doc2bow(doc) for doc in self.docs]
        model_lda = models.LdaModel(docs_corpus, num_topics, id2word=self.docs_dict)
        docs_lda = model_lda[docs_corpus]
        docs_vecs = np.vstack([sparse2full(c, len(self.docs_dict)) for c in docs_lda])
        return docs_vecs

    def get_hdp(self):
        '''
        Get Hierarchical Dirichlet Process(HDP) vector for document list
        '''
        docs_corpus = [self.docs_dict.doc2bow(doc) for doc in self.docs]
        model_hdp = models.HdpModel(docs_corpus, id2word=self.docs_dict)
        docs_hdp = model_hdp[docs_corpus]
        docs_vecs = np.vstack([sparse2full(c, len(self.docs_dict)) for c in docs_hdp])
        return docs_vecs
