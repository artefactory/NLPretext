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
import spacy
import nltk
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import wordnet

try:
    french_spacy = spacy.load('fr_core_news_sm')
except:
    raise OSError("""You must install French langage to use SpaCy. 
                    python -m spacy download fr
                    See https://spacy.io/usage/ for details
                """)
try:
    english_spacy = spacy.load('en_core_web_sm')
except:
    raise OSError("""You must install english langage to use SpaCy. 
                    python -m spacy download en
                    See https://spacy.io/usage/ for details
                """)             


def lemmatize_french_tokens(tokens:list, module:str='spacy')->list:
    """
    Wrappers of SpaCy french lemmatizers (based on FrenchLeffLemmatizer but 
    faster and more accurate.) 

    Parameters
    ----------
    tokens : list
        List of tokens
    module : ({'spacy'})
        Only spaCy is available. We removed FrenchLeffLemmatizer for performance
        considerations.

    Returns
    -------
    list
        list of lemmatized tokens
    """

    tokens = _make_sure_input_is_list_of_tokens(tokens)

    if module == 'spacy':
        # Doc : https://spacy.io/api/token#attributes
        text = ' '.join(tokens)
        doc = french_spacy(text)
        return [token.lemma_ for token in doc]

    else:
        raise ValueError("must pass a valid module name!")


def lemmatize_english_tokens(tokens:list, module:str='spacy')->list:
    """
    Wrapper of SpaCy english lemmatizer and NLTK WordNet.

    Parameters
    ----------
    tokens : list
        List of tokens
    module : ({'spacy'},{'nltk'})
        Tokenizer module. Default: 'spacy'

    Returns
    -------
    list
        list of lemmatized tokens
    """
    tokens = _make_sure_input_is_list_of_tokens(tokens)

    if module == 'nltk':
        # Doc : https://github.com/ClaudeCoulombe/FrenchLefffLemmatizer
        lemmatizer = WordNetLemmatizer()
        return [lemmatizer.lemmatize(word, _get_wordnet_pos(word)) for word in tokens]

    elif module == 'spacy':
        # Doc : https://spacy.io/api/token#attributes
        text = ' '.join(tokens)
        doc = english_spacy(text)
        return [token.lemma_ for token in doc]

    else:
        raise ValueError("must pass a valid module name!")


def _get_wordnet_pos(word):
    """
    Map POS tag to first character lemmatize() accepts
    """
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)        


def _make_sure_input_is_list_of_tokens(tokens):
    """
    Raises an error if input is not a list, and convert "None" to blank list
    to handle dataset with no text.
    """    
    if type(tokens) is list:
        return tokens
    elif tokens is None:
        return []
    elif type(tokens) is str:
        raise ValueError("must pass a list of tokens, not text!")    

