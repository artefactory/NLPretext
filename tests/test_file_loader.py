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
import re

import numpy as np
import pytest
from nlpretext._utils.file_loader import (check_text_file_format,
                                          detect_encoding)

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

def test_detect_encoding():
    create_files()
    expected = {'encoding': 'ISO-8859-1', 'confidence': 0.73, 'language': ''}
    result = detect_encoding('testdoc_latin1.txt')
    np.testing.assert_equal(result, expected)
    remove_files()

def remove_files():
    os.remove('testdoc_latin1.txt')
    os.remove('testdoc_utf8.txt')


@pytest.mark.parametrize(
    "input_filepath, raising, expected_str",
    [
        ("hello.csv", False, "csv"),
        ("folder/hello.csv", False, "csv"),
        ("gs://folder/hello.csv", False, "csv"),
        ("s3://folder/hello.csv", False, "csv"),
        ("hdfs://folder/hello.csv", False, "csv"),
        ("az://folder/hello.csv", False, "csv"),
        ("wildcards/*.csv", False, "csv"),
        ("compressed/gz/text.csv.gz", False, "csv"),
        ("compressed/zip/text.csv.zip", False, "csv"),
        (["hello.csv"], False, "csv"),
        (["hello.csv", "compressed.csv.gz"], False, "csv"),
        (["hello.csv", "other/folder/hello.csv"], False, "csv"),
        ("hello.json", False, "json"),
        ("folder/hello.json", False, "json"),
        ("gs://folder/hello.json", False, "json"),
        (["hello.json", "folder/hello.json"], False, "json"),
        ("hello.txt", False, "txt"),
        ("folder/hello.txt", False, "txt"),
        ("gs://folder/hello.txt", False, "txt"),
        (["hello.txt", "gs://folder/hello.txt"], False, "txt"),
        ("hello.parquet", False, "parquet"),
        ("folder/hello.parquet", False, "parquet"),
        ("gs://folder/hello.parquet", False, "parquet"),
        (["hello.parquet", "gs://folder/hello.parquet"], False, "parquet"),
        ("gs://folder/hello.notaformat", True,
         "Unrecognized format among specified files, only .csv, .json, .parquet and .txt accepted"),
        ("gs://folder/hello.gz", True,
         "Unrecognized format among specified files, only .csv, .json, .parquet and .txt accepted"),
        ("gs://folder/hello.zip", True,
         "Unrecognized format among specified files, only .csv, .json, .parquet and .txt accepted"),
        ("folder/*", True,
         "Unrecognized format among specified files, only .csv, .json, .parquet and .txt accepted"),
        (["hello.txt", "gs://folder/hello.csv"], True,
         re.escape("Multiple file formats found in file path list: ['txt', 'csv']")),
    ]
)
def test_check_text_file_format(input_filepath, raising, expected_str):
    if raising:
        with pytest.raises(ValueError, match=expected_str):
            check_text_file_format(input_filepath)
    else:
        result = check_text_file_format(input_filepath)
        assert result == expected_str
