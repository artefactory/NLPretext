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


from typing import List

from nlpretext._config.stopwords import STOPWORDS
from stop_words import LANGUAGE_MAPPING as _LANGUAGE_MAPPING
from stop_words import get_stop_words as _get_stop_words


def get_stopwords(lang: str = "en") -> List[str]:
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
        custom_stopwords = STOPWORDS
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
        raise ValueError('Please input a valid country code, in 2 letters. Eg. "us" for USA. ')
    return list(set(stopwords))
