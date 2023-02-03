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
# mypy: disable-error-code="assignment"

from typing import List, Union

import chardet
from nlpretext._config import constants


def detect_encoding(file_path_or_string: Union[str, bytes], n_lines: int = 100) -> str:
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
    if isinstance(file_path_or_string, bytes):
        rawdata = file_path_or_string
    else:
        with open(file_path_or_string, "rb") as f:
            rawdata = b"".join([f.readline() for _ in range(n_lines)])
    chardet_value: str = chardet.detect(rawdata)
    return chardet_value


def check_text_file_format(filepath: Union[str, List[str]]) -> str:
    """
    Retrieve format of a file path or list of files path, among .csv, .json, .parquet and .txt

    Parameters
    ----------
    filepath : str | list(str)
        A filepath with wildcard (eg. *.txt), or a list of filepaths.

    Returns
    -------
    str
        Format of the specified file path, among .json, .csv, .parquet or .txt
    """
    pattern = constants.TEXT_FILE_FORMATS_PATTERN
    if not isinstance(filepath, (list, tuple)):
        filepath = [filepath]
    format_re_list = [pattern.match(path) for path in filepath]
    format_list = [format_re.group(1) for format_re in format_re_list if format_re]
    if len(set(format_list)) > 1:
        raise ValueError(f"Multiple file formats found in file path list: {format_list}")
    if None in format_re_list:
        raise ValueError(
            "Unrecognized format among specified files, only .csv, .json, .parquet and .txt accepted"
        )
    file_format = format_list[0]
    return file_format
