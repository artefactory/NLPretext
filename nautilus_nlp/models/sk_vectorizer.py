from sklearn.feature_extraction.text import CountVectorizer
from sklearn.base import BaseEstimator, ClassifierMixin


class sk_vectorizer(BaseEstimator, ClassifierMixin):
    def __init__(self):
        self.model = CountVectorizer()

    def fit(self, train_data):
        self.model.fit(train_data)

    def fit_transform(self, train_data):
        self.model.fit_transform(train_data)
        return train_data

    def transform(self, data):
        return self.model.transform(data)
