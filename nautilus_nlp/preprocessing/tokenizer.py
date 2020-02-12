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
import nltk
from sacremoses import MosesTokenizer, MosesDetokenizer
import spacy
from spacy.lang.fr import French
from spacy.lang.en import English
import spacy.lang as spacylang
nltk.download('punkt')

try:
    french_spacy = spacylang.fr.French()
except:
    raise OSError("""You must install French langage to use SpaCy. 
                    python -m spacy download fr
                    See https://spacy.io/usage/ for details
                """)
try:
    english_spacy = spacylang.en.English()
except:
    raise OSError("""You must install english langage to use SpaCy. 
                    python -m spacy download en
                    See https://spacy.io/usage/ for details
                """)             


def tokenize(text: str, lang_module: str = 'en_spacy')-> list:
    """
    Split text into a list of tokens. 

    Parameters
    ----------
    lang_module
        ({'en_spacy', 'en_nltk', 'fr_spacy', 'fr_moses'}): choose
        the tokenization module according to the langage and the implementation.
        Recommanded: Spacy (faster, better results). To process other langages
        import models.Spacy_models

    Returns
    -------
    list
        Outputs a list of tokens.
    """
    if lang_module == 'en_nltk':
        return nltk.word_tokenize(text)
    elif lang_module == 'en_spacy':
        spacydoc = english_spacy(text)
        return [tokens.text for tokens in spacydoc]
    elif lang_module == 'fr_spacy':
        spacydoc = french_spacy(text)
        return [tokens.text for tokens in spacydoc]
    elif lang_module == 'fr_moses':
        t = MosesTokenizer(lang='fr')
        return t.tokenize(text, escape=False)


def untokenize(tokens:list, lang:str='fr')->str:
    """
    Inputs a list of tokens, output the text joined.
    Wrapper of https://github.com/alvations/sacremoses

    Parameters
    ----------
    lang
        Supported languages: ({'fr', 'en', 'cs','it','ga'})

    Returns
    -------
    string
    """
    d = MosesDetokenizer(lang=lang)
    text = d.detokenize(tokens, unescape=False)
    return text    


def _convert_tokens_to_string(tokens_or_str, lang:str='en')->str:
    """
    Test if the input is tokens or string, and convert tokens to string
    using untokenize(). If the input is null, it will return an empty string. 

    Parameters
    ----------
    lang
        Supported languages: ({'fr', 'en', 'cs','it','ga'}).

    Returns
    -------
    string

    Raises
    -------
    ValueError
        If the input is not string, list or Nonetype.     
    """
    if type(tokens_or_str) is str:
        return tokens_or_str
    elif type(tokens_or_str) is list:
        return untokenize(tokens_or_str, lang=lang)
    elif type(tokens_or_str) is None:
        return ''
    else:
        raise ValueError('Please input string or tokens')


def _convert_string_to_tokens(tokens_or_str, lang_module:str='en_spacy')->str:
    """
    Test if the input is tokens or string, and convert string to tokens
    using tokenize(). If the input is null, it will return an empty list. 

    Parameters
    ----------
    lang_module
        ({'en_spacy', 'en_nltk', 'fr_spacy', 'fr_moses'}): choose
        the tokenization module according to the langage and the implementation.
        Recommanded: Spacy (faster, better results). To process other langages
        import models.Spacy_models

    Returns
    -------
    list
        list of tokens

    Raises
    -------
    ValueError
        If the input is not string, list or Nonetype.     
    """
    if type(tokens_or_str) is str:
        return tokenize(tokens_or_str, lang_module=lang_module)
    elif type(tokens_or_str) is list:
        return tokens_or_str
    elif type(tokens_or_str) is None:
        return []
    else:
        raise ValueError('Please input string or tokens')