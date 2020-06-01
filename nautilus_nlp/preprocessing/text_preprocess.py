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
import regex
import unicodedata
from ftfy import fix_text as _fix_text

from nautilus_nlp.utils.stopwords import get_stopwords
from nautilus_nlp.utils.phone_number import extract_phone_numbers as _extract_phone_numbers
from nautilus_nlp.utils import constants

class TextPreprocessor():

    def __init__(self,text):
        if isinstance(text,str):
            self.text = text
        else:
            raise ValueError("Input must be a string")

    def clean_text(self,lang='en') -> str:
        stopwords = get_stopwords(lang)
        self.text = self.fix_bad_unicode(normalization="NFC")
        self.text = self.remove_EOL_characters()
        self.text = self.remove_accents(method="unicode")
        self.text = self.remove_punct()
        self.text = self.text.lower()
        self.text = self.remove_stopwords(stopwords=stopwords)
        return self.normalize_whitespace()

    def remove_EOL_characters(self) -> str:
        """
        Remove end of line (\n) char.

        Parameters
        ----------
        text : str

        Returns
        -------
        str
        """
        self.text = self.text.replace("\n", " ")
        return self.text

    def remove_stopwords(self, stopwords: list) -> str:
        """ 
        Remove stopwords from a text.
        eg. 'I like when you move your body !' -> 'I move body !'

        Parameters
        ----------
        stopwords : list of stopwords to remove

        Returns
        -------
        str
            text without stopwords

        Raises
        ------
        ValueError
            When inputs is not a string
        """
        self.text =  ' '.join([word.strip() for word in self.text.split() if word not in stopwords])
        
        return self.text

    def fix_bad_unicode(self, normalization: str = "NFC") -> str:
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
        self.text = _fix_text(self.text, normalization=normalization)
        return self.text

    def normalize_whitespace(self) -> str:
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
        self.text = constants.NONBREAKING_SPACE_REGEX.sub(
            " ", constants.LINEBREAK_REGEX.sub(r"\n", self.text)
        ).strip()
        return self.text

    def unpack_english_contractions(self) -> str:
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
        self.text = constants.CONTRACTION_NT_NOT.sub(
            r"\1\2 not",
            self.text,
        )
        self.text = constants.CONTRACTION_LL_WILL.sub(
            r"\1\2 will",
            self.text,
        )
        self.text = constants.CONTRACTION_RE_ARE.sub(r"\1\2 are", self.text)
        self.text = constants.CONTRACTION_VE_HAVE.sub(
            r"\1\2 have",
            self.text,
        )
        self.text = constants.CONTRACTION_CANT_CANNOT.sub(r"\1\2n not", self.text)
        self.text = constants.CONTRACTION_M_AM.sub(r"\1\2 am", self.text)
        self.text = constants.CONTRACTION_LET_LETUS.sub(r"\1\2 us", self.text)
        self.text = constants.CONTRACTION_WONT_WILLNOT.sub(r"\1\2ill not", self.text)
        self.text = constants.CONTRACTION_SHANT_SHALLNOT.sub(r"\1\2hall not", self.text)
        self.text = constants.CONTRACTION_YALL_YOUALL.sub(r"\1\2ou all", self.text)
        return self.text

    def replace_urls(self, replace_with:str="*URL*") -> str:
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
        self.text = constants.URL_REGEX.sub(
            replace_with, constants.SHORT_URL_REGEX.sub(replace_with, self.text)
        )
        return self.text

    def replace_emails(self, replace_with="*EMAIL*") -> str:
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
        self.text = constants.EMAIL_REGEX.sub(replace_with, self.text)
        return self.text

    def replace_phone_numbers(self, replace_with:str="*PHONE*",
                                    method:str="regex",
                                    country_format_to_detect:list=[None,'FR','US','GB'],
                                    return_text: bool = False) -> str:
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
            self.text = constants.PHONE_REGEX.sub(replace_with, self.text)
        elif method == 'detection':
            found_nums = _extract_phone_numbers(self.text, countrylist=country_format_to_detect)

            # order by lenght to avoid truncated numbers to be removed first.
            found_nums.sort(key=len,reverse=True) 
            for phone_number in found_nums:
                self.text = self.text.replace(phone_number, replace_with)
        else:
            raise ValueError('Please input a valid method between "regex" or "detection"')
        return self.text

    def replace_numbers(self, replace_with="*NUMBER*") -> str:
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
        self.text = constants.NUMBERS_REGEX.sub(replace_with, self.text)
        return self.text

    def replace_currency_symbols(self, replace_with=None) -> str:
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
                self.text = self.text.replace(k, v)                
        else:
            self.text = constants.CURRENCY_REGEX.sub(replace_with, self.text)
        return self.text

    def remove_punct(self, marks=None) -> str:
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
            self.text = re.sub("[{}]+".format(re.escape(marks)), " ", self.text, flags=re.UNICODE)
        else:
            self.text = self.text.translate(constants.PUNCT_TRANSLATE_UNICODE)
        return self.text

    def remove_accents(self, method:str="unicode") -> str:
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
            self.text = "".join(
                c
                for c in unicodedata.normalize("NFKD", self.text)
                if not unicodedata.combining(c)
            )
        elif method == "ascii":
            self.text = (
                unicodedata.normalize("NFKD", self.text)
                .encode("ascii", errors="ignore")
                .decode("ascii")
            )
        else:
            msg = '`method` must be either "unicode" and "ascii", not {}'.format(method)
            raise ValueError(msg)
        return self.text

    def remove_multiple_spaces_and_strip_text(self) -> str:
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
            self.text = re.sub(regex_remove_multiple_spaces, " ", self.text)
            self.text = self.text.strip()
        return self.text

    def filter_non_latin_characters(self) -> str:
        """
        Function that filters non latin characters of a text

        Parameters
        ----------
        text : string

        Returns
        -------
        string
        """
        self.text = constants.LATIN_CHARACTERS_RE.sub(' ', self.text)
        self.text = self.normalize_whitespace()
        return self.text

    def remove_smallwords(self, smallwords_threshold:int) -> list:
        """
        Function that removes words which length is below a threshold
        'Hello my name is John Doe' --> 'Hello name John Doe'

        Parameters
        ----------
        text : str
        smallwords_threshold: int
            threshold of small word

        Returns
        -------
        str
        """
        self.text = ' '.join([word for word in self.text.split() if len(word) > smallwords_threshold])
        return self.text










