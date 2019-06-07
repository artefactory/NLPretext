from nautilus_nlp.models.biterm_model import BitermModel
import pandas as pd
import pytest


class UnitTestBiterm:

    def __init__(self):
        self.text = ['Cola 1.5L Carrefour',
                     'Pepsi Cola Light 1.5L',
                     'Pepsi Cola Twist Light',
                     'Cola 1.5L CRF DISC',
                     'Coca-Cola Light 1.5L',
                     'Coca-Cola Light 4x0.5L',
                     'Coca-Cola Light 6x0.3L',
                     'Panzani 200g x 4 bio',
                     'Rustichella 150g bio',
                     'De Cecco - Fusilli bio',
                     'Gerblé sans Gluten50g',
                     'Penne de riz 100g sans gluten',
                     'Spaghetti de maïs 50g sans Glute']

        self.nb_topics = 5
        self.nb_word_per_cluster = 5
        self.nb_iteration = 100
        self.language = 'english'

    def run_tests(self):
        self.test_number_topic_correct()
        for element in ["de", [], 4.5, (23, 24)]:
            self.test_number_iteration_non_int(element)
            self.test_number_topic_non_int(element)
            self.test_data_input(element)

        self.test_number_iteration_negative(-5)
        self.test_number_topic_negative(-5)
        self.test_data_input(["def", 3])
        self.test_data_input(3)
        self.test_no_initialisation()

    def test_number_topic_correct(self):
        biterm_model = BitermModel(data=self.text
                                   , nb_topics=self.nb_topics
                                   , nb_iteration=self.nb_iteration
                                   , lang=self.language)
        clusters = biterm_model.get_clusters(nb_word_per_cluster=self.nb_word_per_cluster)
        assert len(pd.DataFrame(clusters)) == 5

    def test_number_topic_negative(self, nb_topics):
        with pytest.raises(ValueError):
            BitermModel(data=self.text, nb_topics=nb_topics, nb_iteration=self.nb_iteration, lang=self.language)

    def test_number_topic_non_int(self, nb_topics):
        with pytest.raises(ValueError):
            BitermModel(data=self.text, nb_topics=nb_topics, nb_iteration=self.nb_iteration, lang=self.language)

    def test_number_iteration_negative(self, nb_iteration):
        with pytest.raises(ValueError):
            BitermModel(data=self.text, nb_topics=self.nb_topics, nb_iteration=nb_iteration, lang=self.language)

    def test_number_iteration_non_int(self, nb_iteration):
        with pytest.raises(ValueError):
            BitermModel(data=self.text, nb_topics=self.nb_topics, nb_iteration=nb_iteration, lang=self.language)

    def test_data_input(self, data):
        with pytest.raises(ValueError):
            BitermModel(data=data, nb_topics=self.nb_topics, nb_iteration=self.nb_iteration, lang=self.language)

    def test_no_initialisation(self):
        with pytest.raises(ValueError):
            biter_model = BitermModel(data=self.text, nb_topics=self.nb_topics, nb_iteration=self.nb_iteration,
                                      lang=self.language)
            biter_model.get_document_topic(2)


unit_test = UnitTestBiterm()
unit_test.run_tests()
