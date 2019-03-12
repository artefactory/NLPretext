import spacy
import nltk


class Lemmatizer:
    def __init__(self, module: str = "spacy"):
        self.module = module

    def transform(self, text):
        return text
