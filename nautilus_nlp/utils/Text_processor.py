from .lemmatizer import Lemmatizer
from .stemmer import Stemmer
import spacy
import nltk
from .utils import *
from .tokenizer import tokenize


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

    def tokenize(self, text: str, lang: str = 'en'):
        return tokenize(text, lang=lang)


class TokensProcessor:
    def __init__(self, lang: str):
        self.module = module
        self.lemmatizer = None
        self.stemmer = None
        self.lang = lang

    def lemmatize(self, text: str):
        return text

    def stem(self, tokens_list: list, lang: str = lang:
        return stem_tokens(tokens_list, lang='english')

    def remove_stopwords(self, text: str):
        return text

    def untokenize(self, text: str, lang: str = 'en'):
        return tokenize(text, lang=lang)
