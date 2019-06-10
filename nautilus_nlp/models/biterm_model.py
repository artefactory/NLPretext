import numpy as np
from biterm.btm import oBTM
from biterm.utility import vec_to_biterms, topic_summuary
from sklearn.feature_extraction.text import CountVectorizer
import pyLDAvis


class BitermModel:

    def __init__(self, data, nb_topics, nb_iteration, lang):
        """
        Model for topic modelling
        Particularly useful for short texts
        :param data: a list of string, each string can be a document
        :param nb_topics: positive int
        :param nb_iteration: positive int
        :param lang: str, _language to remove the stop words, can be setup to None
        """

        self.is_int_positive(nb_topics)
        self.is_int_positive(nb_iteration)
        self.is_list_of_string(data)

        self.data = data
        self.nb_topics = nb_topics
        self.nb_iteration = nb_iteration
        self.lang = lang
        self._topics = None
        self._btm = None
        self._X = None
        self._vocab = None

    @staticmethod
    def is_int_positive(number):
        """
        Function to check if the input parameter is a integer and positive otherwise raise an error
        :param number:
        :return:
        """
        if not isinstance(number, int):
            raise ValueError("Parameter {} has to be an integer".format(number))
        if number < 1:
            raise ValueError("Parameter {} has to be positive".format(number))

    @staticmethod
    def is_list_of_string(data):
        """
        Function to check if the input parameter is a list of strings otherwise raise an error
        :param data:
        :return:
        """
        if not isinstance(data, list):
            raise ValueError("{} has to be a list".format(data))
        if len(data) == 0:
            raise ValueError("{} is empty".format(data))
        for document in data:
            if not isinstance(document, str):
                raise ValueError("All elements of {} have to be a string, problem with {}".format(data, document))

    def compute_topics(self, nb_word_per_cluster):
        vec = CountVectorizer(stop_words=self.lang)
        self._X = vec.fit_transform(self.data).toarray()
        self._vocab = np.array(vec.get_feature_names())

        biterms = vec_to_biterms(self._X)
        self._btm = oBTM(num_topics=self.nb_topics, V=self._vocab)
        self._topics = self._btm.fit_transform(biterms, iterations=self.nb_iteration)

        results = topic_summuary(self._btm.phi_wz.T, self._X, self._vocab, nb_word_per_cluster, verbose=False)

        return results

    def get_document_topic(self, index):
        if self._topics is None:
            raise ValueError("Model needs to be trained first")

        return self._topics[index].argmax()

    def save_pyLDAvis_plot(self, path_to_output='./biterm_pyLDAavis_plot.html'):
        if self._topics is None or self._btm is None or self._X is None or self._vocab is None:
            raise ValueError("Model needs to be trained first")

        vis = pyLDAvis.prepare(self._btm.phi_wz.T, self._topics, np.count_nonzero(self._X, axis=1), self._vocab,
                               np.sum(self._X, axis=0))
        pyLDAvis.save_html(vis, path_to_output)
