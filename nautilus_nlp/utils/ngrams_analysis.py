# -*- coding: utf-8 -*-
"""
Functions to calculate words or ngrams frequencies.
"""
import pandas as pd
from collections import Counter


def _create_ngrams(token, n):
    """
    Create n-grams for list of tokens
    :param token: list of strings
    :param n: number of elements in the n-gram
    :return: list of n-grams
    """
    ngrams = zip(*[token[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]


def frequent_words(list_words, ngrams_number=1, number_top_words=10 ):
    """
    Compute n-grams frequencies and return number_top_words top n-grams.
    :param list_words: list of strings
    :param ngrams_number: output dataframe length
    :param output_ngrams_number: output dataframe length
    :return: dataframe with the entities and their frequencies.
    """

    frequent = []
    if ngrams_number == 1:
        pass
    elif ngrams_number >= 2:
        list_words = _create_ngrams(list_words, ngrams_number)
    else:
        raise ValueError("number of n-grams should be >= 1")

    x = Counter(list_words)
    frequent = x.most_common(number_top_words)
    return pd.DataFrame(frequent, columns=['Entity', 'Counts'])




