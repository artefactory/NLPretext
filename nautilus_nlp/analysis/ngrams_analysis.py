# GNU Lesser General Public License v3.0 only
# Copyright (C) 2020 Artefact
# licence-information@artefact.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
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
