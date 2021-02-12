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

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json
from stop_words import LANGUAGE_MAPPING as _LANGUAGE_MAPPING
from stop_words import get_stop_words as _get_stop_words
from nautilus_nlp._config.config import STOPWORDS_JSON_FILEPATH
from nautilus_nlp._utils.file_loader import documents_loader


def _load_stopwords_from_json(filepath=STOPWORDS_JSON_FILEPATH):
    stopwords = documents_loader(filepath)
    stopwords = json.loads(stopwords)
    return stopwords


def get_stopwords(lang: str = "en") -> list:
    """
    Inputs a language code, returns a list of stopwords for the specified language

    Parameters
    ----------
    lang : str
        Supported languages: ['ar', 'bg', 'ca', 'cz', 'da', 'nl', 'en',
         'fi', 'fr', 'de', 'hi', 'hu', 'id', 'it', 'nb', 'pl', 'pt', 'ro', 'ru',
         'sk', 'es', 'sv', 'tr', 'uk', 'vi', 'af', 'ha', 'so', 'st', 'sw', 'yo',
         'zu', 'da', 'de', 'es', 'et', 'fi', 'fr', 'hr', 'hu', 'it', 'ko', 'nl',
          'no', 'pl', 'pt', 'ru', 'sv', 'tr', 'zh', 'eo', 'he', 'la', 'sk', 'sl',
          'br', 'ca', 'cs', 'el', 'eu', 'ga', 'gl', 'hy', 'id', 'ja', 'lv', 'th',
           'ar', 'bg', 'bn', 'fa', 'hi', 'mr', 'ro', 'en']

    Returns
    -------
    list
        list of stopwords for a given language

    Raises
    ------
    ValueError
        When language is not available yet or incorrect country code
    """
    if isinstance(lang, str) and len(lang) == 2:
        lang = lang.lower()
        custom_stopwords = _load_stopwords_from_json(STOPWORDS_JSON_FILEPATH)
        stopwords = []

        supported_lang_lib = list(_LANGUAGE_MAPPING.keys())
        supported_lang_custom = list(custom_stopwords.keys())
        supported_lang = supported_lang_lib + supported_lang_custom
        if lang in supported_lang:
            if lang in supported_lang_lib:
                stopwords += _get_stop_words(lang)
            if lang in supported_lang_custom:
                stopwords += custom_stopwords[lang]
        else:
            raise ValueError(
                "Language not available yet or incorrect country code. Supported languages: {}".format(
                    supported_lang
                )
            )
    else:
        raise ValueError(
            'Please input a valid country code, in 2 letters. Eg. "us" for USA. '
        )
    return list(set(stopwords))
