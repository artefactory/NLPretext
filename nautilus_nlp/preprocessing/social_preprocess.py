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
import emoji as _emoji

from nautilus_nlp.utils.preprocess import normalize_whitespace


def remove_mentions(text:str) -> str:
    """
    Function that removes words preceded with a '@'

    Parameters
    ----------
    text : str
    
    Returns
    -------
    string
    """
    return normalize_whitespace(re.sub(r'@\w*', '', text))


def extract_mentions(text:str) -> str:
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
    return re.findall(r'[@][^\s@]+', text)


def remove_html_tags(text:str) -> str:
    """
    Function that removes words between < and >

    Parameters
    ----------
    text : str
    
    Returns
    -------
    string
    """
    return normalize_whitespace(re.sub(r'<.*?>', '', text))


def remove_emoji(text:str) -> str:
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
    emoji_pattern = _emoji.get_emoji_regexp()
    word = emoji_pattern.sub("", text)
    return word


def convert_emoji_to_text(text:str, code_delimiters=(':', ':')) -> str:
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


def extract_emojis(text:str) -> list:
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
    emoji_pattern = _emoji.get_emoji_regexp()
    emojis_in_text = re.findall(emoji_pattern, text)
    emojis_converted = [convert_emoji_to_text(emoji_text) for emoji_text in emojis_in_text]
    return emojis_converted


def extract_hashtags(text) -> list:
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
    return re.findall(r'[#][^\s#]+', text)


def remove_hashtag(text) -> str:
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
    return normalize_whitespace(re.sub(r'#\w*', '', text))
