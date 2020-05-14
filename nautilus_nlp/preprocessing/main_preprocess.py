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
import unicodedata
from ftfy import fix_text as _fix_text

from nautilus_nlp.utils.stopwords import get_stopwords
from nautilus_nlp.utils.phone_number import extract_phone_numbers as _extract_phone_numbers
from nautilus_nlp.utils import constants


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
    text = constants.CONTRACTION_NT_NOT.sub(
        r"\1\2 not",
        text,
    )
    text = constants.CONTRACTION_LL_WILL.sub(
        r"\1\2 will",
        text,
    )
    text = constants.CONTRACTION_RE_ARE.sub(r"\1\2 are", text)
    text = constants.CONTRACTION_VE_HAVE.sub(
        r"\1\2 have",
        text,
    )
    text = constants.CONTRACTION_CANT_CANNOT.sub(r"\1\2n not", text)
    text = constants.CONTRACTION_M_AM.sub(r"\1\2 am", text)
    text = constants.CONTRACTION_LET_LETUS.sub(r"\1\2 us", text)
    text = constants.CONTRACTION_WONT_WILLNOT.sub(r"\1\2ill not", text)
    text = constants.CONTRACTION_SHANT_SHALLNOT.sub(r"\1\2hall not", text)
    text = constants.CONTRACTION_YALL_YOUALL.sub(r"\1\2ou all", text)
    return text





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









