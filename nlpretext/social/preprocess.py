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


from typing import List, Tuple

import emoji as _emoji
from nlpretext._config import constants
from nlpretext.basic.preprocess import normalize_whitespace


def remove_mentions(text: str) -> str:
    """
    Function that removes words preceded with a '@'

    Parameters
    ----------
    text : str

    Returns
    -------
    string
    """
    text = normalize_whitespace(constants.AT_PATTERN.sub("", text))
    return text


def extract_mentions(text: str) -> List[str]:
    """
    Function that extracts words preceded with a '@'
    eg. "I take care of my skin with @thisproduct" --> ["@thisproduct"]

    Parameters
    ----------
    text : str

    Returns
    -------
    string
    """
    return constants.AT_PATTERN.findall(text)


def remove_html_tags(text: str) -> str:
    """
    Function that removes words between < and >

    Parameters
    ----------
    text : str

    Returns
    -------
    string
    """
    text = normalize_whitespace(constants.HTML_TAG_PATTERN.sub("", text))
    return text


def remove_emoji(text: str) -> str:
    """
    Remove emoji from any str by stripping any unicode in the range of Emoji unicode
    as defined in the unicode convention:
    http://www.unicode.org/emoji/charts/full-emoji-list.html

    Parameters
    ----------
    text : str

    Returns
    -------
    str
    """
    text = _emoji.replace_emoji(text, "")
    return text


# TODO: replace mutable default value :
#  https://docs.quantifiedcode.com/python-anti-patterns/correctness/mutable_default_value_as_argument.html
def convert_emoji_to_text(text: str, code_delimiters: Tuple[str, str] = (":", ":")) -> str:
    """
    Convert emoji to their CLDR Short Name, according to the unicode convention
    http://www.unicode.org/emoji/charts/full-emoji-list.html
    eg. 😀 --> :grinning_face:

    Parameters
    ----------
    text : str
    code_delimiters : tuple of symbols around the emoji code.
    eg: (':',':') --> :grinning_face:

    Returns
    -------
    str
        string
    """
    return _emoji.demojize(text, delimiters=code_delimiters)


def extract_emojis(text: str) -> List[str]:
    """
    Function that extracts emojis from a text and translates them into words
    eg. "I take care of my skin 😀 :(" --> [":grinning_face:"]

    Parameters
    ----------
    text : str

    Returns
    -------
    list
        list of all emojis converted with their unicode conventions
    """
    emojis_in_text = _emoji.emoji_list(text)
    emojis_converted = [
        convert_emoji_to_text(emoji_text.get("emoji", "")) for emoji_text in emojis_in_text
    ]
    return emojis_converted


def extract_hashtags(text: str) -> List[str]:
    """
    Function that extracts words preceded with a '#'
    eg. "I take care of my skin #selfcare#selfestim" --> ["skincare", "selfestim"]

    Parameters
    ----------
    text : str

    Returns
    -------
    list
        list of all hashtags
    """
    return constants.HASHTAG_PATTERN.findall(text)


def remove_hashtag(text: str) -> str:
    """
    Function that removes words preceded with a '#'
    eg. "I take care of my skin #selfcare#selfestim" --> "I take care of my skin"

    Parameters
    ----------
    text : str

    Returns
    -------
    str
        text of a post without hashtags
    """
    text = normalize_whitespace(constants.HASHTAG_PATTERN.sub("", text))
    return text
