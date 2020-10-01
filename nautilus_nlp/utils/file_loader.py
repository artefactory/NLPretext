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
import logging
import os
import re
import shutil

import chardet

logging.basicConfig(level=logging.INFO)


def open_textfile(filepath, encoding='utf-8'):
    with io.open(filepath, 'r', encoding=encoding) as f:
        string = f.read()
    return string


def detect_encoding(file_path_or_string, n_lines=100):
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
    the code of the detected encoding
    """
    if os.path.isfile(file_path_or_string):
        with open(file_path_or_string, 'rb') as f:                      # Open the file as binary data
            # Join binary lines for specified number of lines
            rawdata = b''.join([f.readline() for _ in range(n_lines)])
    elif isinstance(file_path_or_string, bytes):
        rawdata = file_path_or_string
    return chardet.detect(rawdata)


def text_loader(filepath, encoding=None, detectencoding=True):
    '''
    This util loads a file. If the encoding is specified, will use the specified
    encoding to load the text file.
    If not specified, this function tries to open the doc as UTF-U, and if
    it fails it will try to detect the encoding using **detect_encoding**

    Parameters
    ----------
    filepath : str
    encoding : str
        If the encoding is specified, will use the specified encoding to load the text file.
    detect_encoding : bool
    If file is not encoded into UTF-8, try to detect encoding using the chardet library.

    Returns
    -------
    string
    '''
    if encoding is not None:
        return open_textfile(filepath, encoding=encoding)
    try:
        return open_textfile(filepath, encoding='utf-8')
    except UnicodeDecodeError:
        logging.warning('Encoding for {} is not UTF-8.'.format(filepath))
        if detectencoding is True:
            logging.warning('Trying to detect encoding for {}'.format(filepath))
            detected_encoding = detect_encoding(filepath)
            logging.info('{filepath}: detected encoding is {encod}, with a confidence rate of {conf_rate}'.format(
                filepath=filepath, encod=detected_encoding['encoding'], conf_rate=detected_encoding['confidence']))
            return open_textfile(filepath, encoding=detected_encoding['encoding'])
        raise UnicodeDecodeError(
            'Cannot load document using utf-8. Try to detect encoding using detectencoding=True')


def get_subfolders_path(folder):
    if not folder.endswith("/"):
        folder = folder + "/"
    return [folder + f+'/' for f in os.listdir(folder)if os.path.isdir(os.path.join(folder, f)) and f != ".DS_Store"]


def list_files_in_subdir(filepath):
    '''
    Get a list of all the filepath of files in directory and subdirectory.
    '''
    res = []
    for path, _, files in os.walk(filepath):
        for name in files:
            res.append(os.path.join(path, name))
    return res


def list_files(filepath: str):
    """
    inputs a filepath.
    Outputs a list of filepath.
    Supports regex
    """

    if os.path.isdir(filepath) and len(re.findall(r"[\w.]$", filepath)) > 0:
        filepath = filepath+'/*'
    if filepath.endswith('/'):
        filepath = filepath+'*'
    return[file for file in glob.glob(filepath) if os.path.isdir(file)]


def documents_loader(filepath: str, encoding=None, detectencoding=True, output_as='dict'):
    '''
    Input a filepath, a filepath with wildcard (eg. *.txt),
    or a list of filepaths.
    Output a string, or a dict of strings.

    Parameters
    ----------
    filepath: filepath
        A filepath with wildcard (eg. *.txt), or a list of filepaths.
    output_as: list or dict.
        If dict, key will be the filename.
    encoding:
        if not specified, will try to detect encoding except if detectencoding is false.
    detectencoding : bool
        if True and if encoding is not specified, will try to detect encoding using chardet.

    Returns
    -------
    string
    the document loaded
    '''
    if isinstance(filepath, str):
        documents = list_files(filepath)
        nb_of_documents = len(documents)
    elif isinstance(filepath, list):
        nb_of_documents = len(filepath)
        documents = filepath
    else:
        raise IOError('Please enter a valid filepath or a valid list of filepath')

    if nb_of_documents == 1:
        return text_loader(
            documents[0], encoding=encoding, detectencoding=detectencoding)
    if nb_of_documents > 1:
        if output_as == 'list':
            return [text_loader(
                document, encoding=encoding, detectencoding=detectencoding) for document in documents]
        if output_as == 'dict':
            return {document: text_loader(
                document, encoding=encoding, detectencoding=detectencoding) for document in documents}
        raise ValueError('Enter a valid output format between list or dict')
    raise IOError('No files detected in {}'.format(filepath))


#################
# CSV Loader

def encode_columns(df, columns_to_encode):
    '''
    apply json.dumps on columns
    '''
    for col in columns_to_encode:
        df[col] = df[col].apply(json.dumps)


def decode_columns(df, columns_to_encode):
    '''
    apply json.loads on columns
    '''
    for col in columns_to_encode:
        df[col] = df[col].apply(json.loads)


#################
# Encoding functions


def convert_encoding(file_path, input_encoding, output_encoding):
    '''
    Encode a file according to a specified encoding
    '''
    with codecs.open(file_path, encoding=input_encoding) as input_file:
        with codecs.open(
                'encoded_'+file_path, "w", encoding=output_encoding) as output_file:
            shutil.copyfileobj(input_file, output_file)
