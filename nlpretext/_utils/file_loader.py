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
import codecs
import glob
import io
import json
import os
import re
import shutil
import warnings
from typing import Optional, Union, List

import chardet

from nlpretext._config import constants


def open_textfile(filepath: str, encoding="utf-8"):
    with io.open(filepath, "r", encoding=encoding) as f:
        string = f.read()
    return string


def detect_encoding(file_path_or_string: str, n_lines: int = 100) -> str:
    """
    Predict a file's encoding using chardet

    Parameters
    ----------
    file_path_or_string : string
        if filepath, will open the file. Otherwise will predict from the string
    n_lines : int
        number of line to predict from

    Returns
    -------
    string
        the code of the detected encoding
    """
    if os.path.isfile(file_path_or_string):
        with open(file_path_or_string, "rb") as f:
            rawdata = b"".join([f.readline() for _ in range(n_lines)])
    elif isinstance(file_path_or_string, bytes):
        rawdata = file_path_or_string
    return chardet.detect(rawdata)


def text_loader(
        filepath: str, encoding: Optional[str] = None, detectencoding: bool = True
) -> str:
    """
    This util loads a file. If the encoding is specified, will use the specified
    encoding to load the text file.
    If not specified, this function tries to open the doc as UTF-U, and if
    it fails it will try to detect the encoding using **detect_encoding**

    Parameters
    ----------
    filepath : str
    encoding : str, optional
        If the encoding is specified, will use the specified encoding to load the text file.
    detectencoding : bool
        If file is not encoded into UTF-8, try to detect encoding using the chardet library.

    Returns
    -------
    string

    Raises
    ------
    UnicodeDecodeError
        if document can't be loaded with utf-8 encoding.
    """
    if encoding is not None:
        return open_textfile(filepath, encoding=encoding)
    try:
        return open_textfile(filepath, encoding="utf-8")
    except UnicodeDecodeError:
        warnings.warn(f"Encoding for {filepath} is not UTF-8.")
        if detectencoding is True:
            detected_encoding = detect_encoding(filepath)
            warnings.warn(
                f'{filepath}: detected encoding is {detected_encoding["encoding"]},\
                            with a confidence rate of {detected_encoding["confidence"]}'
            )
            return open_textfile(filepath, encoding=detected_encoding["encoding"])
        raise UnicodeDecodeError(
            "Cannot load document using utf-8. "
            "Try to detect encoding using detectencoding=True"
        )


def list_files(filepath: str) -> List[str]:
    """
    List files within a given filepath.

    Parameters
    ----------
    filepath : str
        Supports wildcard "*" character.

    Returns
    -------
    list
        list of filepaths
    """

    if os.path.isdir(filepath) and len(re.findall(r"[\w.]$", filepath)) > 0:
        filepath = filepath + "/*"
    if filepath.endswith("/"):
        filepath = filepath + "*"
    return [file for file in glob.glob(filepath) if os.path.isfile(file)]


def documents_loader(
        filepath: str,
        encoding: Optional[str] = None,
        detectencoding: bool = True,
        output_as: str = "dict",
) -> Union[str, list, dict]:
    """
    Input a filepath, a filepath with wildcard (eg. *.txt),
    or a list of filepaths. Output a string, or a dict of strings.

    Parameters
    ----------
    filepath : str
        A filepath with wildcard (eg. *.txt), or a list of filepaths.
    encoding : str, optional
        if not specified, will try to detect encoding except if detectencoding is false.
    detectencoding : bool
        if True and if encoding is not specified, will try to detect encoding using chardet.
    output_as: str {list, dict}
        If dict, key will be the filename.

    Returns
    -------
    Uniont[string, list, dict]
        The document loaded.
    """
    if isinstance(filepath, str):
        documents = list_files(filepath)
        nb_of_documents = len(documents)
    elif isinstance(filepath, list):
        nb_of_documents = len(filepath)
        documents = filepath
    else:
        raise TypeError("Please enter a valid filepath or a valid list of filepath")

    if nb_of_documents == 1:
        return text_loader(
            documents[0], encoding=encoding, detectencoding=detectencoding
        )
    if nb_of_documents > 1:
        if output_as == "list":
            return [
                text_loader(document, encoding=encoding, detectencoding=detectencoding)
                for document in documents
            ]
        if output_as == "dict":
            return {
                document: text_loader(
                    document, encoding=encoding, detectencoding=detectencoding
                )
                for document in documents
            }
        raise TypeError("Enter a valid output format between list or dict")
    raise IOError("No files detected in {}".format(filepath))



## File format detection

def check_text_file_format(filepath) -> str:
    """
    Retrieve format of a file path or list of files path, among .csv, .json and .txt

    Parameters
    ----------
    filepath : str | list(str)
        A filepath with wildcard (eg. *.txt), or a list of filepaths.

    Returns
    -------
    str
        Format of the specified file path, among .json, .csv or .txt
    """
    pattern = constants.TEXT_FILE_FORMATS_PATTERN
    if not isinstance(filepath, list):
        filepath = [filepath]

    format_re_list = [pattern.match(path) for path in filepath]
    if None in format_re_list:
        raise ValueError("Unrecognized format among specified files, only .csv, .json and .txt accepted")

    format_list = [format_re.group(1) for format_re in format_re_list]
    if len(set(format_list)) > 1:
        raise ValueError(f"Multiple file formats found in file path list: {format_list}")

    file_format = format_list[0]
    return file_format
