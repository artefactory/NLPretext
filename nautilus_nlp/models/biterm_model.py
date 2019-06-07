import numpy as np
from biterm.btm import oBTM
from biterm.utility import vec_to_biterms, topic_summuary
from sklearn.feature_extraction.text import CountVectorizer


class biterm_model:

    def __init__(self, data, nb_topics, nb_iteration, lang='english'):
        self.data = data
        self.nb_topics = nb_topics
        self.nb_iteration = nb_iteration
        self.lang = lang
        self.btm = None
        self.topics = None
        self.vocab = None
        self.X = None

    def train_biterm_model(self):
        vec = CountVectorizer(stop_words=self.lang)
        self.X = vec.fit_transform(self.data).toarray()

        self.vocab = np.array(vec.get_feature_names())
        biterms = vec_to_biterms(self.X)
        self.btm = oBTM(num_topics=self.nb_topics, V=self.vocab)
        self.topics = self.btm.fit_transform(biterms, iterations=self.nb_iteration)

    def get_cluster_biterm(self, nb_word_per_cluster):
        results = topic_summuary(self.btm.phi_wz.T, self.X, self.vocab, nb_word_per_cluster, verbose=False)

        return results

    def get_text_topic(self, indice):
        return self.topics[indice].argmax()


text = """Cola 1.5L Carrefour,Pepsi Cola Light 1.5L,Pepsi Cola Twist Light
,Cola 1.5L CRF DISC,Coca-Cola Light 1.5L,Coca-Cola Light 4x0.5L,Coca-Cola Light 6x0.3L
,Panzani 200g x 4 bio,Rustichella 150g bio,De Cecco - Fusilli bio,Gerblé sans Gluten50g
,Penne de riz 100g sans gluten,Spaghetti de maïs 50g sans Glute"""
text = text.split(",")

nb_topics = 5
nb_word_per_cluster = 5
nb_iteration = 100
language = 'english'

BitermModel = biterm_model(data=text
                           , nb_topics=nb_topics
                           , nb_iteration=nb_iteration
                           , lang='english')

BitermModel.train_biterm_model()

clusters = BitermModel.get_cluster_biterm(nb_word_per_cluster=nb_word_per_cluster)
print(clusters)

indice = 0
print("cluster indice", BitermModel.get_text_topic(indice))
