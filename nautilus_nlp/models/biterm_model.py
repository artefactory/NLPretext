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
        self._vectorize_text = None
        self._vocabulary = None

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
        """
        Main function computing the topic modeling, topics
        :param nb_word_per_cluster: positive integer
        :return: a dictionary containing the the different topics with the top words and coherence associated
        """
        vec = CountVectorizer(stop_words=self.lang)
        self._vectorize_text = vec.fit_transform(self.data).toarray()
        self._vocabulary = np.array(vec.get_feature_names())

        biterms = vec_to_biterms(self._vectorize_text)
        self._btm = oBTM(num_topics=self.nb_topics, V=self._vocabulary)
        self._topics = self._btm.fit_transform(biterms, iterations=self.nb_iteration)

        results = topic_summuary(self._btm.phi_wz.T, self._vectorize_text, self._vocabulary, nb_word_per_cluster, verbose=False)

        return results

    def get_document_topic(self, index):
        """
        Get the cluster associated to the specified document
        :param index: the document index, positive integer
        :return: the cluster index
        """
        if self._topics is None:
            raise ValueError("Model needs to be trained first")

        return self._topics[index].argmax()

    def save_pyLDAvis_plot_as_html(self, path_to_output='./biterm_pyLDAavis_plot.html'):
        """
        Function saving the pyLDAvis plot associated with the compute_topics function
        :param path_to_output: path to save the plut, must be a html file
        :return:
        """
        if self._topics is None or self._btm is None or self._vectorize_text is None or self._vocabulary is None:
            raise ValueError("Model needs to be trained first")

        vis = pyLDAvis.prepare(self._btm.phi_wz.T, self._topics, np.count_nonzero(self._vectorize_text, axis=1), self._vocabulary,
                               np.sum(self._vectorize_text, axis=0))
        pyLDAvis.save_html(vis, path_to_output)
