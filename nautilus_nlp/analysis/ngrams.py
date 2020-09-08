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


def create_ngrams(token_list, n):
    """
    Create n-grams for list of tokens

    Parameters
    ----------    
    token_list : list
        list of strings
    n :
        number of elements in the n-gram

    Returns
    -------
    Generator
        generator of all n-grams
    """
    ngrams = zip(*[token_list[i:] for i in range(n)])
    return (" ".join(ngram) for ngram in ngrams)
