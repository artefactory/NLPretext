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
from nltk.stem.snowball import *


def stem_tokens(tokens: list, lang: str ='english')-> list:
    """
    Wrapper of NLTK's Snowball stemmers : http://www.nltk.org/howto/stem.html

    Parameters
    ----------
    tokens : list
        List of tokens
    lang : string
        Supported languages: ({'arabic', 'danish', 'dutch', 'english', 'finnish', 'french',
        'german', 'hungarian', 'italian', 'norwegian', 'porter', 'portuguese', 
        'romanian', 'russian', 'spanish', 'swedish'}): 

    Returns
    -------
    list
        list of stemmed tokens
    """

    supported_lang = [lang for lang in SnowballStemmer.languages]
    
    if lang in supported_lang:
        stemmer = eval(lang.capitalize()+'Stemmer()')
    else:
        raise ValueError("Langage not supported of mispelled")
    
    # Make sure tokens are actually a list, and handle NaN. 
    if type(tokens) is list:
        return [stemmer.stem(token) for token in tokens]
    elif tokens is None:
        return []
    elif type(tokens) is str:
        raise ValueError("must pass a list of tokens, not text!")