from sklearn.base import BaseEstimator, ClassifierMixin
import fastText
import multiprocessing


class Fasttext_clf(BaseEstimator, ClassifierMixin):
    def __init__(self, path=None):
        try:
            self.model = fastText.load_model(path)
        except Exception as e:
            print(e)
            self.model = None

    def fit(self, X, y):
        # Todo Build SKlearn compatible API for training
        return self

    def train(
        self,
        train_data,
        lr=0.1,
        dim=100,
        ws=5,
        epoch=5,
        minCount=1,
        minCountLabel=0,
        minn=0,
        maxn=0,
        neg=5,
        wordNgrams=1,
        loss="softmax",
        bucket=2000000,
        thread=multiprocessing.cpu_count() - 1,
        lrUpdateRate=100,
        t=1e-4,
        label="__label__",
        verbose=2,
        pretrainedVectors="",
    ):
        """
    Train a supervised model and return a model object.
    input must be a filepath. The input text does not need to be tokenized
    as per the tokenize function, but it must be preprocessed and encoded
    as UTF-8. You might want to consult standard preprocessing scripts such
    as tokenizer.perl mentioned here: http://www.statmt.org/wmt07/baseline.html
    The input file must must contain at least one label per line. For an
    example consult the example datasets which are part of the fastText
    repository such as the dataset pulled by classification-example.sh.
    """
        self.model = fastText.train_supervised(
            input=train_data,
            lr=lr,
            dim=dim,
            ws=ws,
            epoch=epoch,
            minCount=minCount,
            minCountLabel=minCountLabel,
            minn=minn,
            maxn=maxn,
            neg=neg,
            wordNgrams=wordNgrams,
            loss=loss,
            bucket=bucket,
            thread=thread,
            lrUpdateRate=lrUpdateRate,
            t=t,
            label=label,
            verbose=verbose,
            pretrainedVectors=pretrainedVectors,
        )

    def predict(self, text, k=1, threshold=0.0, on_unicode_error="strict"):
        """
        Given a string, get a list of labels and a list of
        corresponding probabilities. k controls the number
        of returned labels. A choice of 5, will return the 5
        most probable labels. By default this returns only
        the most likely label and probability. threshold filters
        the returned labels by a threshold on probability. A
        choice of 0.5 will return labels with at least 0.5
        probability. k and threshold will be applied together to
        determine the returned labels.
        This function assumes to be given
        a single line of text. We split words on whitespace (space,
        newline, tab, vertical tab) and the control characters carriage
        return, formfeed and the null character.
        If the model is not supervised, this function will throw a ValueError.
        If given a list of strings, it will return a list of results as usually
        received for a single line of text.
        """
        r = self.model.predict(text)
        return r

    def predict_proba(self, text):
        result_predict = self.model.predict(text)
        if result_predict and len(result_predict) >= 2:
            probas = result_predict[1]
            if probas:
                return probas[0]
        return False

    def score(self, X, y=None):
        return sum(self.predict(X))

    def quantize(
        self,
        input=None,
        qout=False,
        cutoff=0,
        retrain=False,
        epoch=None,
        lr=None,
        thread=None,
        verbose=None,
        dsub=2,
        qnorm=False,
    ):
        self.model.quantize(
            input, qout, cutoff, retrain, epoch, lr, thread, verbose, dsub, qnorm
        )

    def test(self, path, k=1):
        """Evaluate supervised model using file given by path"""
        return self.model.test(path, k)

    def test_label(self, path, k=1, threshold=0.0):
        """
        Return the precision and recall score for each label.
        The returned value is a dictionary, where the key is the label.
        For example:
        f.test_label(...)
        {'__label__italian-cuisine' : {'precision' : 0.7, 'recall' : 0.74}}
        """
        return self.model.test_label(path, k, threshold)

    def save_model(self, path):
        """Save the model to the given path"""
        self.model.save_model(path)
