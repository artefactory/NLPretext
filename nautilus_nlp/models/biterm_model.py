import numpy as np
from biterm.btm import oBTM
from biterm.utility import vec_to_biterms, topic_summuary
from sklearn.feature_extraction.text import CountVectorizer


class BitermModel:

    @staticmethod
    def is_int_positive(number):
        if type(number) != int:
            raise ValueError("Parameter {} has to be an integer".format(number))
        if number < 1:
            raise ValueError("Parameter {} has to be positive".format(number))

    @staticmethod
    def is_list_of_string(data):
        if type(data) != list:
            raise ValueError("{} has to be a list".format(data))
        if len(data) == 0:
            raise ValueError("{} is empty".format(data))
        for document in data:
            if type(document) != str:
                raise ValueError("All elements of {} have to be a string, problem with {}".format(data, document))

    def __init__(self, data, nb_topics, nb_iteration, lang='english'):
        """
        Model for topic modelling
        Particularly useful for short texts
        :param data: a list of string, each string can be a document
        :param nb_topics: positive int
        :param nb_iteration: positive int
        :param lang: str, language to remove the stop words
        """

        self.is_int_positive(nb_topics)
        self.is_int_positive(nb_iteration)
        self.is_list_of_string(data)

        self.data = data
        self.nb_topics = nb_topics
        self.nb_iteration = nb_iteration
        self.lang = lang
        self.topics = None

    def get_clusters(self, nb_word_per_cluster):
        vec = CountVectorizer(stop_words=self.lang)
        X = vec.fit_transform(self.data).toarray()
        vocab = np.array(vec.get_feature_names())

        biterms = vec_to_biterms(X)
        btm = oBTM(num_topics=self.nb_topics, V=vocab)
        self.topics = btm.fit_transform(biterms, iterations=self.nb_iteration)

        results = topic_summuary(btm.phi_wz.T, X, vocab, nb_word_per_cluster, verbose=False)

        return results

    def get_document_topic(self, index):
        if self.topics is None:
            raise ValueError("Model needs to be trained first")

        return self.topics[index].argmax()
