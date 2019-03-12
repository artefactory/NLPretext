from sklearn.base import BaseEstimator, ClassifierMixin
import fastText


class Fasttext_clf(BaseEstimator, ClassifierMixin):
    def __init__(self, path=None):
        try:
            self.model = fastText.load_model(path)
        except Exception as e:
            print(e)
            self.model = None

    def fit(self, X, y):
        return self

    def predict(self, X):
        r = self.model.predict(X)
        return r

    def predict_proba(self, X):
        result_predict = self.model.predict(X)
        if result_predict and len(result_predict) >= 2:
            probas = result_predict[1]
            if probas:
                return probas[0]
        return False

    def score(self, X, y=None):
        return sum(self.predict(X))
