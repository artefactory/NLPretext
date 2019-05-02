from nautilus_nlp.utils.ngrams_analysis import frequent_words
import pytest


def test_frequent_words():
    list_words = ['Hello', 'world', 'this', 'is', 'an', 'example', 'of', 'ngrams', 'count', 'an', 'example',
                  'to', 'test', 'this', 'is', 'an', 'example', 'function', 'hello', 'world']

    res_1 = frequent_words(list_words, ngrams_number=1, number_top_words=10)
    res_2 = frequent_words(list_words, ngrams_number=2, number_top_words=3)
    res_3 = frequent_words(list_words, ngrams_number=3, number_top_words=5)

    exp_res_1 = [('an', 3), ('example', 3), ('world', 2), ('this', 2), ('is', 2), ('Hello', 1), ('of', 1), ('ngrams', 1),
                 ('count', 1), ('to', 1)]
    exp_res_2 = [('an example', 3), ('this is', 2), ('is an', 2)]
    exp_res_3 = [('this is an', 2), ('is an example', 2), ('Hello world this', 1),
                 ('world this is', 1), ('an example of', 1)]

    assert res_1 == exp_res_1
    assert res_2 == exp_res_2
    assert res_3 == exp_res_3
