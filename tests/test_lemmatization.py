import pytest
from nautilus_nlp.preprocessing.lemmatization import lemmatize_french_tokens, lemmatize_english_tokens

def test_lemmatize_french_tokens_spacy():
    input_tokens = ['Ceci', 'est', 'un', 'texte', 'français', ',', "j'", 'adore', 'tes', 'frites', 'bien', 'grasses', 'YOLO', '!']
    expected = ['ceci', 'être', 'un', 'texte', 'français', ',', 'j', "'", 'adorer', 'ton', 'frit', 'bien', 'gras', 'yolo', '!']
    res = lemmatize_french_tokens(input_tokens, module='spacy')
    assert res == expected


def test_lemmatize_english_tokens_spacy():
    input_tokens = ['The', 'striped', 'bats', 'are', 'hanging', 'on', 'their', 'feet', 'for', 'best']
    expected = ['the', 'strip', 'bat', 'be', 'hang', 'on', '-PRON-', 'foot', 'for', 'good']
    res = lemmatize_french_tokens(input_tokens, module='spacy')
    assert res == expected


def test_lemmatize_english_tokens_nltk():
    input_tokens = ['The', 'striped', 'bats', 'are', 'hanging', 'on', 'their', 'feet', 'for', 'best']
    expected = ['The', 'strip', 'bat', 'be', 'hang', 'on', 'their', 'foot', 'for', 'best']
    res = lemmatize_french_tokens(input_tokens, module='nltk')
    assert res == expected    