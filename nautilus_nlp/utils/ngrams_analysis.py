# -*- coding: utf-8 -*-
"""
Functions to calculate words or ngrams frequencies.
"""
from collections import Counter


def create_ngrams(token, n):
    """
    Create n-grams for list of tokens

    Parameters
    ----------    
    token : list
        list of strings
    n :
        number of elements in the n-gram

    Returns
    -------
    list
        list of n-grams
    """    
    ngrams = zip(*[token[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]


def frequent_words(list_words, ngrams_number=1, number_top_words=10):
    """
    Create n-grams for list of tokens

    Parameters
    ----------    
    ngrams_number : int
    
    number_top_words : int 
        output dataframe length

    Returns
    -------
    DataFrame
        Dataframe with the entities and their frequencies.
    """             
    frequent = []
    if ngrams_number == 1:
        pass
    elif ngrams_number >= 2:
        list_words = create_ngrams(list_words, ngrams_number)
    else:
        raise ValueError("number of n-grams should be >= 1")
    x = Counter(list_words)
    frequent = x.most_common(number_top_words)
    return frequent
