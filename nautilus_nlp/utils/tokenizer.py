import nltk
from sacremoses import MosesTokenizer, MosesDetokenizer


def tokenize(text, lang='en'):
    """
    Inputs string output a list of tokens
    French = "J' ai" >>> ["J'", 'ai']
    """
    if lang is 'en':
        tokens = nltk.word_tokenize(text)

    elif lang is 'fr':
        t = MosesTokenizer(lang='fr')
        tokens = t.tokenize(text, escape=False)
    return tokens


def untokenize(tokens, lang='fr'):
    '''
    Inputs a list of tokens output string.
    ["J'", 'ai'] >>> "J' ai"
    '''
    d = MosesDetokenizer(lang=lang)
    text = d.detokenize(tokens, unescape=False)
    return text    