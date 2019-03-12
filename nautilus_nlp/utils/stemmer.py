import spacy
import nltk


class Stemmer:
    def __init__(self, module: str = "spacy"):
        self.module = module

    def transform(self, text):
        return text
