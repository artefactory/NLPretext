import os

def load_text_file(file_path):
    '''
    load a file as string
    Inputs a file path, returns a string'''
    with open(file_path, errors="ignore") as handle:
        text = handle.read()
    return text


def load_texts_as_string(filenames):
    """ Input is a list of path, output is a dict """
    from collections import defaultdict
    loaded_text = defaultdict(str)  # each value is a string, the text
    for filename in filenames:
        with open(filename, errors="ignore") as handle:
            loaded_text[filename] = handle.read()
    return loaded_text


def get_filenames(folder):
    from os import listdir
    from os.path import isfile, join

    if not folder.endswith("/"):
        folder = folder + "/"
    # this will return only the filenames, not folders inside the path
    return [folder + f for f in listdir(folder)
        if isfile(join(folder, f)) and f != ".DS_Store"]    


def get_filepath(folder):
    """
    Return the path of all the files of a directory
    """
    import os
    if not folder.endswith("/"):
        folder = folder + "/"
    res = []
    for root, dirs, files in os.walk(folder, topdown=False):
        for name in files:
            res.append(os.path.join(root, name))
    return res        


def predict_encoding(file_path_or_string, file=True, n_lines=20):
'''
Predict a file's encoding using chardet
'''
import chardet

if file is True:
    # Open the file as binary data
    with open(file_path_or_string, 'rb') as f:
        # Join binary lines for specified number of lines
        rawdata = b''.join([f.readline() for _ in range(n_lines)])
else:
    rawdata = file_path_or_string

return chardet.detect(rawdata)['encoding']


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