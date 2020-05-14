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
#nltk.download('punkt')

try:
    french_spacy = spacylang.fr.French().tokenizer
except OSError:
    raise OSError("""You must install French langage to use SpaCy. 
                    python -m spacy download fr
                    See https://spacy.io/usage/ for details
                """)
try:
    english_spacy = spacylang.en.English().tokenizer
except OSError:
    raise OSError("""You must install english langage to use SpaCy. 
                    python -m spacy download en
                    See https://spacy.io/usage/ for details
                """)             


def tokenize(text: str, lang_module: str = 'en_spacy'):
    """
    Convert text to a list of tokens. 

    Parameters
    ----------    
    lang_module : ({'en_spacy', 'en_nltk', 'fr_spacy', 'fr_moses'})
        choose the tokenization module according to the langage and the implementation.
        Recommanded: Spacy (faster, better results). To process other langages
        import models.Spacy_models

    Returns
    -------
    list
        list of string
    """      
    if lang_module is 'en_nltk':
        return nltk.word_tokenize(text)
    elif lang_module is 'en_spacy':
        spacydoc = english_spacy(text)
        return [spacy_token.text for spacy_token in spacydoc]
    elif lang_module is 'fr_spacy':
        spacydoc = french_spacy(text)
        return [spacy_token.text for spacy_token in spacydoc]
    elif lang_module is 'fr_moses':
        t = MosesTokenizer(lang='fr')
        return t.tokenize(text, escape=False)


def untokenize(tokens, lang='fr'):
    '''
    Inputs a list of tokens output string.
    ["J'", 'ai'] >>> "J' ai"

    Parameters
    ----------    
    lang : string
        language code 
    '''
    d = MosesDetokenizer(lang=lang)
    text = d.detokenize(tokens, unescape=False)
    return text    


def _convert_tokens_to_string(tokens_or_str):
    if type(tokens_or_str) is str:
        return tokens_or_str
    elif type(tokens_or_str) is list:
        return untokenize(tokens_or_str)
    elif type(tokens_or_str) is None:
        return ''
    else:
        raise ValueError('Please input string or tokens')


def _convert_string_to_tokens(tokens_or_str, lang_module='en_spacy'):
    if type(tokens_or_str) is str:
        return tokenize(tokens_or_str, lang_module=lang_module)
    elif type(tokens_or_str) is list:
        return tokens_or_str
    elif type(tokens_or_str) is None:
        return []
    else:
        raise ValueError('Please input string or tokens')