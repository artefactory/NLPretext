from .lemmatizer import Lemmatizer
from .stemmer import Stemmer
import spacy
import nltk
from .utils import *


class TextProcessor:
    def __init__(self, lang: str, module: str = "spacy"):
        self.module = module
        self.lemmatizer = None
        self.stemmer = None
        self.lang = lang

    def transform(self, text):
        return text

    def lemmatize(self, text: str):
        return text

    def stem(self, text: str):
        return text

    def remove_stopwords(self, text: str):
        return text

    def lower(self, text: str):
        return text.lower()
