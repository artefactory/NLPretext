# coding=utf-8
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

import os

import numpy as np
from nlpretext._utils.file_loader import (detect_encoding, documents_loader)

TESTDOC_LATIN1 = "J'aime les frites bien grasse étalon châpeau!"
TESTDOC_UTF8 = "Un deuxième exemple de texte en utf-8 cette fois!"

def create_files():
    encoded_s = TESTDOC_LATIN1.encode('latin-1')
    with open('testdoc_latin1.txt', 'wb') as f:
        f.write(encoded_s)


    encoded_s = TESTDOC_UTF8.encode('utf-8')
    with open('testdoc_utf8.txt', 'wb') as f:
        f.write(encoded_s)
    return True


def test_openfile_with_encoding():
    create_files()
    input_str = "testdoc_latin1.txt"
    expected_str = TESTDOC_LATIN1
    result = documents_loader(input_str, encoding='latin-1')
    np.testing.assert_string_equal(result, expected_str)
    remove_files()


def test_openfile_utf8():
    create_files()
    input_str = "testdoc_utf8.txt"
    expected_str = TESTDOC_UTF8
    result = documents_loader(input_str)
    np.testing.assert_string_equal(result, expected_str)
    remove_files()

def test_encoding_detection():
    create_files()
    input_str = "testdoc_latin1.txt"
    expected_str = TESTDOC_LATIN1
    result = documents_loader(input_str)
    np.testing.assert_string_equal(result, expected_str)
    remove_files()

def test_load_several_docs_wildcard():
    create_files()
    expected = {'testdoc_latin1.txt': "J'aime les frites bien grasse étalon châpeau!",
                'testdoc_utf8.txt': 'Un deuxième exemple de texte en utf-8 cette fois!'}
    result = documents_loader('test*.txt', output_as='dict')
    np.testing.assert_equal(result, expected)
    remove_files()

def test_load_several_docs_list():
    create_files()
    expected = {'testdoc_latin1.txt': "J'aime les frites bien grasse étalon châpeau!",
                'testdoc_utf8.txt': 'Un deuxième exemple de texte en utf-8 cette fois!'}
    result = documents_loader(['testdoc_latin1.txt', 'testdoc_utf8.txt'], output_as='dict')
    np.testing.assert_equal(result, expected)
    remove_files()


def test_load_several_docs_output_list():
    create_files()
    expected = ["J'aime les frites bien grasse étalon châpeau!",
                'Un deuxième exemple de texte en utf-8 cette fois!']
    result = documents_loader(['testdoc_latin1.txt', 'testdoc_utf8.txt'], output_as='list')
    remove_files()
    return len(expected) == len(result) and sorted(expected) == sorted(result)


def test_detect_encoding():
    create_files()
    expected = {'encoding': 'ISO-8859-1', 'confidence': 0.73, 'language': ''}
    result = detect_encoding('testdoc_latin1.txt')
    np.testing.assert_equal(result, expected)
    remove_files()

def remove_files():
    os.remove('testdoc_latin1.txt')
    os.remove('testdoc_utf8.txt')
