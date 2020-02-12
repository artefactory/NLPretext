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
import pytest
from nautilus_nlp.preprocessing.lemmatization import lemmatize_french_tokens, lemmatize_english_tokens

def test_lemmatize_french_tokens_spacy():
    input_tokens = ['Ceci', 'est', 'un', 'texte', 'français', ',', "j'", 'adore', 'tes', 'frites', 'bien', 'grasses', 'YOLO', '!']
    expected = ['ceci', 'être', 'un', 'texte', 'français', ',', 'j', "'", 'adorer', 'ton', 'frit', 'bien', 'gras', 'yolo', '!']
    res = lemmatize_french_tokens(input_tokens, module='spacy')
    assert res == expected


def test_lemmatize_english_tokens_spacy():
    input_tokens = ['The', 'strip', 'bats', 'are', 'hanging', 'on', 'their', 'feet', 'for', 'best']
    expected = ['the', 'strip', 'bat', 'be', 'hang', 'on', '-PRON-', 'foot', 'for', 'good']
    res = lemmatize_english_tokens(input_tokens, module='spacy')
    assert res == expected


def test_lemmatize_english_tokens_nltk():
    input_tokens = ['The', 'striped', 'bats', 'are', 'hanging', 'on', 'their', 'feet', 'for', 'best']
    expected = ['The', 'strip', 'bat', 'be', 'hang', 'on', 'their', 'foot', 'for', 'best']
    res = lemmatize_english_tokens(input_tokens, module='nltk')
    assert res == expected