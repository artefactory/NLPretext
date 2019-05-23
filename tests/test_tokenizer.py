import pytest
from nautilus_nlp.preprocessing.tokenizer import tokenize, untokenize


def test_tokenize_fr_spacy():
    input_str = """Les moteurs de recherche tels Google, Exalead ou Yahoo! sont des applications très connues de fouille de textes sur de grandes masses de données. Cependant, les moteurs de recherche ne se basent pas uniquement sur le texte pour l'indexer, mais également sur la façon dont les pages sont mises en valeur les unes par rapport aux autres. L'algorithme utilisé par Google est PageRank, et il est courant de voir HITS dans le milieu académique"""
    expected = ['Les', 'moteurs', 'de', 'recherche', 'tels', 'Google', ',', 'Exalead', 'ou', 'Yahoo', '!', 'sont', 'des', 'applications', 'très', 'connues', 'de', 'fouille', 'de', 'textes', 'sur', 'de', 'grandes', 'masses', 'de', 'données', '.', 'Cependant', ',', 'les', 'moteurs', 'de', 'recherche', 'ne', 'se', 'basent', 'pas', 'uniquement', 'sur', 'le', 'texte', 'pour', "l'", 'indexer', ',', 'mais', 'également', 'sur', 'la', 'façon', 'dont', 'les', 'pages', 'sont', 'mises', 'en', 'valeur', 'les', 'unes', 'par', 'rapport', 'aux', 'autres', '.', "L'", 'algorithme', 'utilisé', 'par', 'Google', 'est', 'PageRank', ',', 'et', 'il', 'est', 'courant', 'de', 'voir', 'HITS', 'dans', 'le', 'milieu', 'académique']
    res = tokenize(input_str, lang_module="fr_spacy")
    assert res == expected


def test_tokenize_fr_moses():
    input_str = """Les moteurs de recherche tels Google, Exalead ou Yahoo! sont des applications très connues de fouille de textes sur de grandes masses de données. Cependant, les moteurs de recherche ne se basent pas uniquement sur le texte pour l'indexer, mais également sur la façon dont les pages sont mises en valeur les unes par rapport aux autres. L'algorithme utilisé par Google est PageRank, et il est courant de voir HITS dans le milieu académique"""
    expected = ['Les', 'moteurs', 'de', 'recherche', 'tels', 'Google', ',', 'Exalead', 'ou', 'Yahoo', '!', 'sont', 'des', 'applications', 'très', 'connues', 'de', 'fouille', 'de', 'textes', 'sur', 'de', 'grandes', 'masses', 'de', 'données', '.', 'Cependant', ',', 'les', 'moteurs', 'de', 'recherche', 'ne', 'se', 'basent', 'pas', 'uniquement', 'sur', 'le', 'texte', 'pour', "l'", 'indexer', ',', 'mais', 'également', 'sur', 'la', 'façon', 'dont', 'les', 'pages', 'sont', 'mises', 'en', 'valeur', 'les', 'unes', 'par', 'rapport', 'aux', 'autres', '.', "L'", 'algorithme', 'utilisé', 'par', 'Google', 'est', 'PageRank', ',', 'et', 'il', 'est', 'courant', 'de', 'voir', 'HITS', 'dans', 'le', 'milieu', 'académique']
    res = tokenize(input_str, lang_module="fr_moses")
    assert res == expected    

def test_tokenize_null_input():
    input_str = ''
    expected = []
    res = tokenize(input_str, lang_module="en_spacy")
    assert res == expected

def test_tokenize_en_spacy():
    input_str = "Let's play together!"
    expected = ['Let', "'s", 'play', 'together', '!']
    res = tokenize(input_str, lang_module="en_spacy")
    assert res == expected
    
def test_tokenize_en_nltk():
    input_str = "Let's play together!"
    expected = ['Let', "'s", 'play', 'together', '!']
    res = tokenize(input_str, lang_module="en_nltk")
    assert res == expected    

def test_untokenize_en():
    input_str = ['Let', "'s", 'play', 'together', '!']
    expected = "Let's play together!"
    res = untokenize(input_str,lang='en')
    assert res == expected

def test_untokenize_fr():
    input_str = ['Les', 'moteurs', 'de', 'recherche', 'tels', 'Google', ',', 'Exalead', 'ou', 'Yahoo', '!']
    expected = "Les moteurs de recherche tels Google, Exalead ou Yahoo !"
    res = untokenize(input_str,lang='fr')
    assert res == expected