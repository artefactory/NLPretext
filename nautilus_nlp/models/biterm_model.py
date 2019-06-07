import numpy as np
from biterm.btm import oBTM
from biterm.utility import vec_to_biterms, topic_summuary
from sklearn.feature_extraction.text import CountVectorizer


class BitermModel:

    def __init__(self, data, nb_topics, nb_iteration, lang='english'):
        """
        Model for topic modelling
        Particularly useful for short texts
        :param data: a list of string, each string can be a document
        :param nb_topics: positive int
        :param nb_iteration: positive int
        :param lang: str, language to remove the stop words
        """
        self.data = data
        self.nb_topics = nb_topics
        self.nb_iteration = nb_iteration
        self.lang = lang
        self.btm = None
        self.topics = None
        self.vocab = None
        self.X = None

    def pre_processing(self, data):
        vec = CountVectorizer(stop_words=self.lang)
        X = vec.fit_transform(data).toarray()
        vocab = np.array(vec.get_feature_names())

        return X, vocab

    def train_biterm_model(self):
        X, vocab = self.pre_processing(self.data)

        biterms = vec_to_biterms(X)
        self.btm = oBTM(num_topics=self.nb_topics, V=vocab)
        self.topics = self.btm.fit_transform(biterms, iterations=self.nb_iteration)

    def get_cluster_biterm(self, data, nb_word_per_cluster):
        X, vocab = self.pre_processing(data)
        results = topic_summuary(self.btm.phi_wz.T, X, vocab, nb_word_per_cluster, verbose=False)

        return results

    def get_text_topic(self, index):
        return self.topics[index].argmax()
