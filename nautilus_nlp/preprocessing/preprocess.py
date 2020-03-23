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

import os
import json
import re
import unicodedata

import emoji as _emoji
import regex
from ftfy import fix_text as _fix_text
from stop_words import get_stop_words as _get_stop_words
from stop_words import LANGUAGE_MAPPING as _LANGUAGE_MAPPING

from nautilus_nlp.utils.phone_number import extract_phone_numbers as _extract_phone_numbers
from nautilus_nlp.utils import constants
from nautilus_nlp.config.config import ROOT_FOLDER
from nautilus_nlp.utils.file_loader import documents_loader

STOPWORDS_JSON_FILEPATH = os.path.join(ROOT_FOLDER, "data", "stopwords.json")


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


def remove_EOL_characters(text: str) -> str:
    """
    Remove end of line (\n) char.

    Parameters
    ----------
    text : str

    Returns
    -------
    str
    """
    return text.replace("\n", " ")


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
    if type(lang) == str and len(lang) == 2:
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


def remove_stopwords(text_or_tokens, stopwords: list) -> list:
    """ 
    Remove stopwords from a list of tokens or a text.
    eg. ['I','like','when','you','move','your','body','!'] -> ['I', 'move', 'body', '!']

    Parameters
    ----------
    text_or_tokens : list or string
        list of tokens to be cleaned

    Returns
    -------
    list
        list of tokens without stopwords

    Raises
    ------
    ValueError
        When inputs is not a string or a list
    """
    if type(text_or_tokens) is str:
        return [word for word in text_or_tokens.split() if word not in stopwords]
    elif type(text_or_tokens) is list:
        return [word for word in text_or_tokens if word not in stopwords]
    else:
        raise ValueError("must input string or list of tokens")


def fix_bad_unicode(text: str, normalization: str = "NFC") -> str:
    """
    Fix unicode text that's "broken" using `ftfy <http://ftfy.readthedocs.org/>`_;
    this includes mojibake, HTML entities and other code cruft,
    and non-standard forms for display purposes.

    Parameters
    ----------
    text : string

    normalization ({'NFC', 'NFKC', 'NFD', 'NFKD'}): 
        if 'NFC', combines characters and diacritics written using separate code points,
        e.g. converting "e" plus an acute accent modifier into "é"; unicode
        can be converted to NFC form without any change in its meaning!
        if 'NFKC', additional normalizations are applied that can change
        the meanings of characters, e.g. ellipsis characters will be replaced
        with three periods
    Returns
    -------
    string
    """
    return _fix_text(text, normalization=normalization)


def normalize_whitespace(text:str) -> str:
    """
    Given ``text`` str, replace one or more spacings with a single space, and one
    or more linebreaks with a single newline. Also strip leading/trailing whitespace.
    eg. "   foo  bar  " -> "foo bar"

    Parameters
    ----------
    text : string

    Returns
    -------
    string    
    """
    return constants.NONBREAKING_SPACE_REGEX.sub(
        " ", constants.LINEBREAK_REGEX.sub(r"\n", text)
    ).strip()



def unpack_english_contractions(text:str) -> str:
    """
    Replace *English* contractions in ``text`` str with their unshortened forms.
    N.B. The "'d" and "'s" forms are ambiguous (had/would, is/has/possessive),
    so are left as-is.
    eg. "You're fired. She's nice." -> "You are fired. She's nice."

    Parameters
    ----------
    text : string

    Returns
    -------
    string    
    """

    # standard
    text = re.sub(
        r"(\b)([Aa]re|[Cc]ould|[Dd]id|[Dd]oes|[Dd]o|[Hh]ad|[Hh]as|[Hh]ave|[Ii]s|[Mm]ight|[Mm]ust|[Ss]hould|[Ww]ere|[Ww]ould)n't",
        r"\1\2 not",
        text,
    )
    text = re.sub(
        r"(\b)([Hh]e|[Ii]|[Ss]he|[Tt]hey|[Ww]e|[Ww]hat|[Ww]ho|[Yy]ou)'ll",
        r"\1\2 will",
        text,
    )
    text = re.sub(r"(\b)([Tt]hey|[Ww]e|[Ww]hat|[Ww]ho|[Yy]ou)'re", r"\1\2 are", text)
    text = re.sub(
        r"(\b)([Ii]|[Ss]hould|[Tt]hey|[Ww]e|[Ww]hat|[Ww]ho|[Ww]ould|[Yy]ou)'ve",
        r"\1\2 have",
        text,
    )
    # non-standard
    text = re.sub(r"(\b)([Cc]a)n't", r"\1\2n not", text)
    text = re.sub(r"(\b)([Ii])'m", r"\1\2 am", text)
    text = re.sub(r"(\b)([Ll]et)'s", r"\1\2 us", text)
    text = re.sub(r"(\b)([Ww])on't", r"\1\2ill not", text)
    text = re.sub(r"(\b)([Ss])han't", r"\1\2hall not", text)
    text = re.sub(r"(\b)([Yy])(?:'all|a'll)", r"\1\2ou all", text)
    return text


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
    text = regex.sub(r'[^\p{Latin}1-9]', ' ', text).strip()
    return re.sub(' +', ' ', text)


def replace_urls(text:str, replace_with:str="*URL*") -> str:
    """
    Replace all URLs in ``text`` str with ``replace_with`` str.

    Parameters
    ----------
    text : string
    replace_with : string
        the string you want the URL to be replaced with.

    Returns
    -------
    string
    """    
    return constants.URL_REGEX.sub(
        replace_with, constants.SHORT_URL_REGEX.sub(replace_with, text)
    )


def replace_emails(text, replace_with="*EMAIL*") -> str:
    """
    Replace all emails in ``text`` str with ``replace_with`` str

    Parameters
    ----------
    text : string
    replace_with : string
        the string you want the email address to be replaced with.

    Returns
    -------
    string
    """
    return constants.EMAIL_REGEX.sub(replace_with, text)


def replace_phone_numbers(text, replace_with:str="*PHONE*",
                                method:str="regex",
                                country_format_to_detect:list=[None,'FR','US','GB']) -> str:
    """
    Replace all phone numbers in ``text`` str with ``replace_with`` str

    Parameters
    ----------
    text : string
    replace_with : string
        the string you want the phone number to be replaced with.
    method : ['regex','detection']
        regex is faster but will omit a lot of numbers, while detection will 
        catch every numbers, but takes a while.
    country_format_to_detect : list 
        If a list of country code is specified, will catch every number formatted.
        Only when method = 'detection'.
    Returns
    -------
    string
    """
    if method == 'regex':
        return constants.PHONE_REGEX.sub(replace_with, text)
        
    elif method == 'detection':
        found_nums = _extract_phone_numbers(text, countrylist=country_format_to_detect)

        # order by lenght to avoid truncated numbers to be removed first.
        found_nums.sort(key=len,reverse=True) 
        for phone_number in found_nums:
            text = text.replace(phone_number, replace_with)
        
        return text
    else:
        raise ValueError('Please input a valid method between "regex" or "detection"')


def replace_numbers(text, replace_with="*NUMBER*") -> str:
    """
    Replace all numbers in ``text`` str with ``replace_with`` str.

    Parameters
    ----------
    text : string
    replace_with : string
        the string you want the number to be replaced with.

    Returns
    -------
    string
    """        
    return constants.NUMBERS_REGEX.sub(replace_with, text)


def replace_currency_symbols(text, replace_with=None) -> str:
    """
    Replace all currency symbols in ``text`` str with string specified by ``replace_with`` str.

    Parameters
    ----------
    text : str
        raw text
    replace_with : None or string
        if None (default), replace symbols with
            their standard 3-letter abbreviations (e.g. '$' with 'USD', '£' with 'GBP');
            otherwise, pass in a string with which to replace all symbols
            (e.g. "*CURRENCY*")

    Returns
    -------
    string
    """          
    if replace_with is None:
        for k, v in constants.CURRENCIES.items():
            text = text.replace(k, v)
        return text
    else:
        return constants.CURRENCY_REGEX.sub(replace_with, text)


def remove_punct(text, marks=None) -> str:
    """
    Remove punctuation from ``text`` by replacing all instances of ``marks``
    with whitespace.

    Parameters
    ----------
    text : str
        raw text
    
    marks : str or None
        If specified, remove only the characters in this string,
        e.g. ``marks=',;:'`` removes commas, semi-colons, and colons.
        Otherwise, all punctuation marks are removed.

    Returns
    -------
    string

    Note
    -------
    When ``marks=None``, Python's built-in :meth:`str.translate()` is
    used to remove punctuation; otherwise, a regular expression is used
    instead. The former's performance is about 5-10x faster.    
    """       
    if marks:
        return re.sub("[{}]+".format(re.escape(marks)), " ", text, flags=re.UNICODE)
    else:
        return text.translate(constants.PUNCT_TRANSLATE_UNICODE)


def remove_accents(text:str, method:str="unicode") -> str:
    """
    Remove accents from any accented unicode characters in ``text`` str, either by
    transforming them into ascii equivalents or removing them entirely.

    Parameters
    ----------
    text : str
        raw text
    
    method : ({'unicode', 'ascii'})
        if 'unicode', remove accented
        char for any unicode symbol with a direct ASCII equivalent; if 'ascii',
        remove accented char for any unicode symbol

        NB: the 'ascii' method is notably faster than 'unicode', but less good

    Returns
    -------
    string

    Raises
    -------
    ValueError
        if ``method`` is not in {'unicode', 'ascii'}   
    """
    if method == "unicode":
        return "".join(
            c
            for c in unicodedata.normalize("NFKD", text)
            if not unicodedata.combining(c)
        )
    elif method == "ascii":
        return (
            unicodedata.normalize("NFKD", text)
            .encode("ascii", errors="ignore")
            .decode("ascii")
        )
    else:
        msg = '`method` must be either "unicode" and "ascii", not {}'.format(method)
        raise ValueError(msg)


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


def preprocess_text(
    text,
    remove_eol_char=True,
    fix_unicode=False,
    lowercase=False,
    no_urls=False,
    no_emails=False,
    no_phone_numbers=False,
    no_numbers=False,
    no_currency_symbols=False,
    no_punct=False,
    no_contractions=False,
    no_accents=False,
    no_emoji=False,
    replace_with=' ', 
    no_stopwords=None,
    phone_countries_format=[None,'US','FR'],
    phone_method='regex'
) -> str:
    """
    Normalize various aspects of a raw text doc. A convenience function for
    applying all other preprocessing functions in one go.

    Parameters
    ----------
    text : str
        raw text to preprocess
    fix_unicode : bool
        if True, fix "broken" unicode such as mojibake and garbled HTML entities
    remove_eol_char : bool 
        if True, will remove the end-of-line characters \\n
    lowercase : bool
        if True, all text is lower-cased
    no_urls : bool
        if True, replace all URL strings with '*URL*' or with "replace_with" if 
        specified.
    no_emails : bool
        if True, replace all email strings with '*EMAIL*' or with "replace_with" if 
        specified.
    no_phone_numbers : bool
        if True, replace all phone number strings with '*PHONE*' or with "replace_with" if 
        specified.
    no_numbers : bool
        if True, replace all number-like strings with '*NUMBER*' or with "replace_with" if 
        specified.
    no_currency_symbols : bool
        if True, if True, replace all currency symbols with their standard 
        3-letter abbreviations.
    no_punct : bool
        if True, remove all punctuation (replace with empty string)
    no_contractions : bool
        if True, if True, replace *English* contractions with their unshortened forms
    no_accents : bool
        if True, replace all accented characters with unaccented versions
    no_emoji : bool
        if True, remove all emojis from text
    replace_with : string
        The string you want the entities to be replaced with.
    no_stopwords : 2-letter country code
        If specified, will remove the stopwords of the given language. 
        Supported languages: ['ar', 'bg', 'ca', 'cz', 'da', 'nl', 'en',
         'fi', 'fr', 'de', 'hi', 'hu', 'id', 'it', 'nb', 'pl', 'pt', 'ro', 'ru', 
         'sk', 'es', 'sv', 'tr', 'uk', 'vi', 'af', 'ha', 'so', 'st', 'sw', 'yo', 
         'zu', 'da', 'de', 'es', 'et', 'fi', 'fr', 'hr', 'hu', 'it', 'ko', 'nl',
          'no', 'pl', 'pt', 'ru', 'sv', 'tr', 'zh', 'eo', 'he', 'la', 'sk', 'sl', 
          'br', 'ca', 'cs', 'el', 'eu', 'ga', 'gl', 'hy', 'id', 'ja', 'lv', 'th',
           'ar', 'bg', 'bn', 'fa', 'hi', 'mr', 'ro', 'en']    
    phone_countries_format : list
        formats of the phone numbers to be removed. Full list is available at
    utils.SUPPORTED_COUNTRY
    phone_method : ['regex','detection']
        regex is faster but will omit a lot of numbers, while detection will 
        catch every numbers, but takes a while.
    Returns
    -------
    string
        input ``text`` processed according to function args        

    Warning
    -------
    These changes may negatively affect subsequent NLP analysis performed
        on the text, so choose carefully, and preprocess at your own risk!        
    """
    assert isinstance(text, str), "The text to preprocess must be a string"

    if fix_unicode is True:
        text = fix_bad_unicode(text, normalization="NFC")
    if remove_eol_char is True:
        text = remove_EOL_characters(text)
    if no_urls is True:
        text = replace_urls(text, replace_with=replace_with)
    if no_emails is True:
        text = replace_emails(text, replace_with=replace_with)
    if no_phone_numbers is True:
        text = replace_phone_numbers(text,  replace_with=replace_with,
                                            method=phone_method,
                                            country_format_to_detect=phone_countries_format)
    if no_numbers is True:
        text = replace_numbers(text, replace_with=replace_with)
    if no_currency_symbols is True:
        text = replace_currency_symbols(text, replace_with=replace_with)
    if no_emoji is True:
        text = remove_emoji(text)
    if no_contractions is True:
        text = unpack_english_contractions(text)
    if no_accents is True:
        text = remove_accents(text, method="unicode")
    if no_punct is True:
        text = remove_punct(text)
    if lowercase is True:
        text = text.lower()
    if no_stopwords is not None:
        stopwords = get_stopwords(no_stopwords)
        text = ' '.join(remove_stopwords(text, stopwords))
    # always normalize whitespace; treat linebreaks separately from spacing
    text = normalize_whitespace(text)
    
    return text
