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

from __future__ import absolute_import, division, print_function, unicode_literals

import re
from nautilus_nlp.utils import constants
from nautilus_nlp.preprocessing.main_preprocess import normalize_whitespace


def remove_multiple_spaces_and_strip_text(text: str) -> str:
    """
    Remove multiple spaces, strip text, and remove '-', '*' characters.

    Parameters
    ----------
    text : str
        the text to be processed

    Returns
    -------
    string
        the text with removed multiple spaces and strip text
    """
    regex_remove_multiple_spaces_list = ["\\t", "[\\s\\-\\*]{2,}"]
    for regex_remove_multiple_spaces in regex_remove_multiple_spaces_list:
        text = re.sub(regex_remove_multiple_spaces, " ", text)
        text = text.strip()
    return text


def remove_tokens_with_nonletters(tokens: list) -> list:
    """
    Inputs a list of tokens, outputs a list of tokens without tokens that
    includes numbers of special caracters.
    ['foo','bar','124','34euros'] -> ['foo','bar']

    Parameters
    ----------
    tokens : list
        list of tokens to be cleaned

    Returns
    -------
    list
        list of tokens without tokens with numbers
    """
    return [word for word in tokens if re.search("[^a-zA-Z]", word) is None]


def remove_special_caracters_from_tokenslist(tokens: list) -> list:
    """ 
    Remove tokens that doesn't contains any number or letter. 
    eg. ['foo','bar','---',"'s",'#'] -> ['foo','bar',"'s"]

    Parameters
    ----------
    tokens : list
        list of tokens to be cleaned

    Returns
    -------
    list
        list of tokens without tokens that contains only special caracters
    
    """
    return [word for word in tokens if re.search("[a-zA-Z0-9]", word)]


def filter_non_latin_characters(text:str) -> str:
    """
    Function that filters non latin characters of a text

    Parameters
    ----------
    text : string

    Returns
    -------
    string
    """
    text = constants.LATIN_CHARACTERS_RE.sub(' ', text)
    #text = regex.sub(r'[^\p{Latin}1-9]', ' ', text).strip()
    return normalize_whitespace(text)


def remove_smallwords(tokens_list:list, smallwords_threshold:int) -> list:
    """
    Function that removes words which length is below a threshold
    ["hello", "my", "name", "is", "John", "Doe"] --> ["hello","name","John","Doe"]

    Parameters
    ----------
    text : list
        list of strings
    smallwords_threshold: int
        threshold of small word

    Returns
    -------
    list
    """
    result = [word for word in tokens_list if len(word) > smallwords_threshold]
    return result
