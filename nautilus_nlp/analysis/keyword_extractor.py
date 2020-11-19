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
from typing import Union, List, Tuple, Dict
from collections import Counter

from flashtext import KeywordProcessor
from nautilus_nlp.analysis.ngrams import create_ngrams


def extract_keywords(
        text: str, keyword: Union[str, List[str], Dict[str, List[str]]], case_sensitive: bool = True
    ) -> List[str]:
    """
    Extract Keywords from a document, using FlashText

    Parameters
    ----------
    text : str
        Text to extract keywords from. 
    keyword : Union[str, list[str], dict[str, list[str]]]
        Single keyword (str), list of keywords (list), or keyword dict.
        Example of keyword dict: keyword_dict = {
                    "java": ["java_2e", "java programing"],
                    "product management": ["PM", "product manager"]
                }
    case_sensitive : bool
        If False, will be case insensitive.

    Returns
    -------
    list
        Return list of extracted keywords
    """

    processor = KeywordProcessor(case_sensitive=case_sensitive)
    if isinstance(keyword, list):
        processor.add_keywords_from_list(keyword)
    elif isinstance(keyword, str):
        processor.add_keyword(keyword)
    elif isinstance(keyword, dict):
        processor.add_keywords_from_dict(keyword)

    return processor.extract_keywords(text)


def get_frequent_words(
        tokens: List[str], ngrams_number: int = 1, number_top_words: int = 10) -> List[Tuple[str, int]]:
    """
    Create n-grams for a list of tokens

    Parameters
    ----------
    tokens : list
        list of tokens
    ngrams_number : int
    number_top_words : int
        number of top keywords to return

    Returns
    -------
    list[tuple[str, int]]
        Returns a list of the top n words ().
    """
    frequent = []
    if ngrams_number == 1:
        pass
    elif ngrams_number >= 2:
        tokens = create_ngrams(tokens, ngrams_number)
    else:
        raise ValueError("number of n-grams should be >= 1")
    counter = Counter(tokens)
    frequent = counter.most_common(number_top_words)
    return frequent
