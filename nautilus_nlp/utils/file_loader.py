import io
import chardet
import glob
import re
from os.path import isfile, isdir
import json
import logging

logging.basicConfig(level=logging.INFO)


def open_textfile(filepath, encoding='utf-8'):
    with io.open(filepath, 'r', encoding=encoding) as f:
        string = f.read()
    return string


def detect_encoding(file_path_or_string, n_lines=100):
    '''
    Predict a file's encoding using chardet
    '''
    if isfile(file_path_or_string):
        with open(file_path_or_string, 'rb') as f:                      # Open the file as binary data
            rawdata = b''.join([f.readline() for _ in range(n_lines)])  # Join binary lines for specified number of lines
    elif type(file_path_or_string) is bytes:
        rawdata = file_path_or_string
    return chardet.detect(rawdata)


def text_loader(filepath, encoding=None, detectencoding=True):
    '''
    Args:
        detect_encoding[bool]= If file is not encoded into UTF-8, try to detect encoding using the chardet library.
    '''
    if encoding is not None:
        return open_textfile(filepath, encoding=encoding)
    else:
        try:
            return open_textfile(filepath, encoding='utf-8')
        except UnicodeDecodeError:
            logging.warning('Encoding for {} is not UTF-8.'.format(filepath))
            if detectencoding is True:
                logging.warning('Trying to detect encoding for {}'.format(filepath))
                detected_encoding = detect_encoding(filepath)
                logging.info('{filepath}: detected encoding is {encod}, with a confidence rate of {conf_rate}'.format(filepath=filepath, encod=detected_encoding['encoding'],
                                                                                                        conf_rate=detected_encoding['confidence']))
                return open_textfile(filepath, encoding=detected_encoding['encoding'])
            else:
                raise UnicodeDecodeError('Cannot load document using utf-8. Try to detect encoding using detectencoding=True')


def list_files(filepath:str):
    """  
    inputs a filepath. 
    Outputs a list of filepath. 
    Supports regex
    """

    if isdir(filepath) and len(re.findall(r"[\w.]$",filepath)):
        filepath=filepath+'/*'
    if filepath.endswith('/'):
        filepath=filepath+'*'
    return[file for file in glob.glob(filepath) if isfile(file)]            


def documents_loader(filepath:str, encoding=None, detectencoding=True, output_as='dict'):
    '''
    Input a filepath, a filepath with wildcard (eg. *.txt), 
    or a list of filepaths.
    Output a string, or a dict of strings.
    Args:
        filepath: filepath, a filepath with wildcard (eg. *.txt), 
            or a list of filepaths.
        output_as: list or dict. If dict, key will be the filename.
        encoding: if not specified, will try to detect encoding except if 
            detectencoding is false. 
        detectencoding: if True and if encoding is not specified, will try to 
            detect encoding using chardet. 

    '''
    
    if type(filepath) is str:
        documents = list_files(filepath)
        nb_of_documents = len(documents)
    elif type(filepath) is list:
        nb_of_documents = len(filepath)
        documents = filepath
    else:
        raise IOError('Please enter a valid filepath or a valid list of filepath')
    
    if nb_of_documents == 1:
        return text_loader(documents[0],encoding=encoding, detectencoding=detectencoding)
    elif nb_of_documents > 1:
        if output_as == 'list':
            return [text_loader(document, encoding=encoding, detectencoding=detectencoding) for document in documents]
        elif output_as == 'dict':
            return { document : text_loader(document, encoding=encoding, detectencoding=detectencoding) for document in documents}
        else:
            raise ValueError('Enter a valid output format between list or dict')
    else:
        raise IOError('No files detected in {}'.format(filepath))        


#################
## CSV Loader

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
## Encoding functions


def convert_encoding(file_path, input_encoding, output_encoding):
    '''
    Encode a file according to a specified encoding
    '''
    import codecs
    import shutil

    with codecs.open(file_path, encoding=input_encoding) as input_file:
        with codecs.open(
                'encoded_'+file_path, "w", encoding=output_encoding) as output_file:
            shutil.copyfileobj(input_file, output_file)

