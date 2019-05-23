import pytest
from nautilus_nlp.preprocessing.stemming import stem_tokens

def test_stem_en():
    input_tokens = ['I','survived','these', 'dogs']
    expected = ['i', 'surviv', 'these', 'dog']
    res = stem_tokens(input_tokens, lang='english')
    assert res == expected

def test_stem_fr():
    input_tokens = ['je', 'mangerai', 'dans', 'les', 'cuisines', 'du', 'château']
    expected = ['je', 'mang', 'dan', 'le', 'cuisin', 'du', 'château']
    res = stem_tokens(input_tokens, lang='french')
    assert res == expected

    