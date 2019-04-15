# -*- coding: utf-8 -*-
"""
Functions that modify raw text *in-place*, replacing contractions, URLs, emails,
phone numbers, and currency symbols with standardized forms. These should be
applied before processing by `Spacy <http://spacy.io>`_, but be warned: preprocessing
may affect the interpretation of the text -- and spacy's processing of it.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import json
import re
import unicodedata

from ftfy import fix_text
from stop_words import get_stop_words as _get_stop_words
from stop_words import LANGUAGE_MAPPING as _LANGUAGE_MAPPING

from . import constants
from nautilus_nlp.config.config import ROOT_FOLDER
from nautilus_nlp.utils.file_loader import documents_loader

STOPWORDS_JSON_FILEPATH = os.path.join(ROOT_FOLDER,'data','stopwords.json')


def remove_multiple_spaces_and_strip_text(text):
    """Remove multiple spaces, strip text, and remove '-', '*' characters.
    Parameters
    ----------
    text : str,
        Header content.
    Returns
    -------
    str
    """
    regex_remove_multiple_spaces_list= ["\\t", "[\\s\\-\\*]{2,}"]
    for regex_remove_multiple_spaces in regex_remove_multiple_spaces_list:
        text = re.sub(regex_remove_multiple_spaces, ' ', text)
        text = text.strip()
    return text

def remove_tokens_with_nonletters(tokens):
    '''
    Inputs a list of tokens, outputs a list of tokens without tokens that
    includes numbers of special caracters
    '''
    return [word for word in tokens if re.search('[a-zA-Z]', word)]


def remove_special_caracters(tokens):
    """ Checks for letters in the token - using a regex search.
    Strings that are just punctuation will
    be removed! No more custom '--'. But ''s' and '9' will remain.
    """
    return [word for word in tokens if re.search('[a-zA-Z0-9]', word)]


def _load_stopwords_from_json(filepath=STOPWORDS_JSON_FILEPATH):
    stopwords = documents_loader(filepath)
    stopwords = json.loads(stopwords)
    return stopwords


def get_stopwords(lang:str = 'en'): 
    '''
    Inputs a language code, returns a list of stopwords for the specified language

    Args:
        lang: Supported languages: ['ar', 'bg', 'ca', 'cz', 'da', 'nl', 'en',
         'fi', 'fr', 'de', 'hi', 'hu', 'id', 'it', 'nb', 'pl', 'pt', 'ro', 'ru', 
         'sk', 'es', 'sv', 'tr', 'uk', 'vi', 'af', 'ha', 'so', 'st', 'sw', 'yo', 
         'zu', 'da', 'de', 'es', 'et', 'fi', 'fr', 'hr', 'hu', 'it', 'ko', 'nl',
          'no', 'pl', 'pt', 'ru', 'sv', 'tr', 'zh', 'eo', 'he', 'la', 'sk', 'sl', 
          'br', 'ca', 'cs', 'el', 'eu', 'ga', 'gl', 'hy', 'id', 'ja', 'lv', 'th',
           'ar', 'bg', 'bn', 'fa', 'hi', 'mr', 'ro', 'en']
    '''
    if type(lang) == str and len(lang) == 2:
        lang = lang.lower()
        
        custom_stopwords = _load_stopwords_from_json(STOPWORDS_JSON_FILEPATH)
        stopwords = []
        
        supported_lang_lib = list(_LANGUAGE_MAPPING.keys())
        supported_lang_custom = list(custom_stopwords.keys())
        supported_lang = supported_lang_lib+supported_lang_custom
        if lang in supported_lang:
            if lang in supported_lang_lib:
                stopwords += _get_stop_words(lang)
            if lang in supported_lang_custom:
                stopwords += custom_stopwords[lang]
        else:
            raise ValueError('Language not available yet or incorrect country code. Supported languages: {}'.format(supported_lang))
    else:
        raise ValueError('Please input a valid country code, in 2 letters. Eg. "us" for USA. ')
    return list(set(stopwords))


def remove_stopwords(text_or_tokens, stopwords):
    ''' 
    Remove stopwords from tokens.
    '''
    if type(text_or_tokens) is str:
        return [word for word in text_or_tokens.split() if word not in stopwords]
    elif type(text_or_tokens) is list:
        return [word for word in text_or_tokens if word not in stopwords]                                                    
    else:
        raise ValueError('must input string or list of tokens')    


def fix_bad_unicode(text, normalization="NFC") -> str:
    """
    Fix unicode text that's "broken" using `ftfy <http://ftfy.readthedocs.org/>`_;
    this includes mojibake, HTML entities and other code cruft,
    and non-standard forms for display purposes.

    Args:
        text (str): raw text
        normalization ({'NFC', 'NFKC', 'NFD', 'NFKD'}): if 'NFC',
            combines characters and diacritics written using separate code points,
            e.g. converting "e" plus an acute accent modifier into "é"; unicode
            can be converted to NFC form without any change in its meaning!
            if 'NFKC', additional normalizations are applied that can change
            the meanings of characters, e.g. ellipsis characters will be replaced
            with three periods

    Returns:
        str
    """
    return fix_text(text, normalization=normalization)


def normalize_whitespace(text) -> str:
    """
    Given ``text`` str, replace one or more spacings with a single space, and one
    or more linebreaks with a single newline. Also strip leading/trailing whitespace.
    """
    return constants.NONBREAKING_SPACE_REGEX.sub(
        " ", constants.LINEBREAK_REGEX.sub(r"\n", text)
    ).strip()


def unpack_french_contractions(text) -> str:

    return text


def unpack_english_contractions(text) -> str:
    """
    Replace *English* contractions in ``text`` str with their unshortened forms.
    N.B. The "'d" and "'s" forms are ambiguous (had/would, is/has/possessive),
    so are left as-is.
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


def unpack_contractions_from_lang(text, lang: str = "fr") -> str:
    if lang == "fr":
        return unpack_english_contractions(text)
    else:
        return unpack_english_contractions(text)


def replace_urls(text, replace_with="*URL*") -> str:
    """Replace all URLs in ``text`` str with ``replace_with`` str."""
    return constants.URL_REGEX.sub(
        replace_with, constants.SHORT_URL_REGEX.sub(replace_with, text)
    )


def replace_emails(text, replace_with="*EMAIL*") -> str:
    """Replace all emails in ``text`` str with ``replace_with`` str."""
    return constants.EMAIL_REGEX.sub(replace_with, text)


def replace_phone_numbers(text, replace_with="*PHONE*") -> str:
    """Replace all phone numbers in ``text`` str with ``replace_with`` str."""
    return constants.PHONE_REGEX.sub(replace_with, text)


def replace_numbers(text, replace_with="*NUMBER*") -> str:
    """Replace all numbers in ``text`` str with ``replace_with`` str."""
    return constants.NUMBERS_REGEX.sub(replace_with, text)


def replace_currency_symbols(text, replace_with=None) -> str:
    """
    Replace all currency symbols in ``text`` str with string specified by ``replace_with`` str.

    Args:
        text (str): raw text
        replace_with (str): if None (default), replace symbols with
            their standard 3-letter abbreviations (e.g. '$' with 'USD', '£' with 'GBP');
            otherwise, pass in a string with which to replace all symbols
            (e.g. "*CURRENCY*")

    Returns:
        str
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

    Args:
        text (str): raw text
        marks (str): If specified, remove only the characters in this string,
            e.g. ``marks=',;:'`` removes commas, semi-colons, and colons.
            Otherwise, all punctuation marks are removed.

    Returns:
        str

    Note:
        When ``marks=None``, Python's built-in :meth:`str.translate()` is
        used to remove punctuation; otherwise, a regular expression is used
        instead. The former's performance is about 5-10x faster.
    """
    if marks:
        return re.sub("[{}]+".format(re.escape(marks)), " ", text, flags=re.UNICODE)
    else:
        return text.translate(constants.PUNCT_TRANSLATE_UNICODE)


def remove_accents(text, method="unicode") -> str:
    """
    Remove accents from any accented unicode characters in ``text`` str, either by
    transforming them into ascii equivalents or removing them entirely.

    Args:
        text (str): raw text
        method ({'unicode', 'ascii'}): if 'unicode', remove accented
            char for any unicode symbol with a direct ASCII equivalent; if 'ascii',
            remove accented char for any unicode symbol

            NB: the 'ascii' method is notably faster than 'unicode', but less good

    Returns:
        str

    Raises:
        ValueError: if ``method`` is not in {'unicode', 'ascii'}
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

def remove_emoji(word):
    """
    Remove emoji from any  str by stripping any unicode in the range of Emoji unicode,

    Args:
        word (str): raw word

    Returns:
        str

    """
    RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
    word = RE_EMOJI.sub(r'', word)
    return word

def preprocess_text(
    text,
    no_emoji=False,
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
) -> str:
    """
    Normalize various aspects of a raw text doc before parsing it with Spacy.
    A convenience function for applying all other preprocessing functions in one go.

    Args:
        text (str): raw text to preprocess
        fix_unicode (bool): if True, fix "broken" unicode such as
            mojibake and garbled HTML entities
        lowercase (bool): if True, all text is lower-cased
        no_urls (bool): if True, replace all URL strings with '*URL*'
        no_emails (bool): if True, replace all email strings with '*EMAIL*'
        no_phone_numbers (bool): if True, replace all phone number strings
            with '*PHONE*'
        no_numbers (bool): if True, replace all number-like strings
            with '*NUMBER*'
        no_currency_symbols (bool): if True, replace all currency symbols
            with their standard 3-letter abbreviations
        no_punct (bool): if True, remove all punctuation (replace with
            empty string)
        no_contractions (bool): if True, replace *English* contractions
            with their unshortened forms
        no_accents (bool): if True, replace all accented characters
            with unaccented versions

    Returns:
        str: input ``text`` processed according to function args

    Warning:
        These changes may negatively affect subsequent NLP analysis performed
        on the text, so choose carefully, and preprocess at your own risk!
    """
    if fix_unicode is True:
        text = fix_bad_unicode(text, normalization="NFC")
    if no_urls is True:
        text = replace_urls(text)
    if no_emails is True:
        text = replace_emails(text)
    if no_phone_numbers is True:
        text = replace_phone_numbers(text)
    if no_numbers is True:
        text = replace_numbers(text)
    if no_currency_symbols is True:
        text = replace_currency_symbols(text)
    if no_contractions is True:
        text = unpack_contractions_from_lang(text)
    if no_accents is True:
        text = remove_accents(text, method="unicode")
    if no_punct is True:
        text = remove_punct(text)
    if lowercase is True:
        text = text.lower()
    # always normalize whitespace; treat linebreaks separately from spacing
    text = normalize_whitespace(text)

    return text
