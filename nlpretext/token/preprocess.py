# Copyright (C) 2020 Artefact
# licence-information@artefact.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License


from typing import List, Optional

import re

from nlpretext._utils.stopwords import get_stopwords


def remove_stopwords(
    tokens: List[str], lang: str, custom_stopwords: Optional[List[str]] = None
) -> List[str]:
    """
    Remove stopwords from a text.
    eg. 'I like when you move your body !' -> 'I move body !'

    Parameters
    ----------
    tokens: list(str)
        list of tokens
    lang: str
        language iso code (e.g : "en")
    custom_stopwords : list(str)|None
        list of custom stopwords to add. None by default

    Returns
    -------
    list
        tokens without stopwords

    Raises
    ------
    ValueError
        When inputs is not a list
    """
    stopwords = get_stopwords(lang)
    if custom_stopwords:
        stopwords += custom_stopwords
    tokens = [word for word in tokens if word not in stopwords]
    return tokens


def remove_tokens_with_nonletters(tokens: List[str]) -> List[str]:
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
    tokens = [word for word in tokens if re.search("[^a-zA-Z]", word) is None]
    return tokens


def remove_special_caracters_from_tokenslist(tokens: List[str]) -> List[str]:
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
    tokens = [word for word in tokens if re.search("[a-zA-Z0-9]", word)]
    return tokens


def remove_smallwords(tokens: List[str], smallwords_threshold: int) -> List[str]:
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
    tokens = [word for word in tokens if len(word) > smallwords_threshold]
    return tokens
