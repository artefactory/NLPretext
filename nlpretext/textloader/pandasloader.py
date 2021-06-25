from fsspec import open_files
import pandas as pd


def _list_handler(func):
    def wrapper_list_handler(file_path, *args, **kwargs):
        list_files = open_files(file_path)
        list_df = [func(file, *args, **kwargs) for file in list_files]
        df = list_df[0]
        return df
    return wrapper_list_handler


@_list_handler
def read_text(file_path, encoding):
    df = pd.read_fwf(file_path, encoding=encoding, colspecs=[(None, None)])
    return df


@_list_handler
def read_json(file_path, encoding):
    df = pd.read_json(file_path, encoding=encoding)
    return df


@_list_handler
def read_csv(file_path, encoding):
    print("ok")
    df = pd.read_csv(file_path, encoding=encoding)
    return df


@_list_handler
def read_parquet(file_path, encoding):
    df = pd.read_parquet(file_path, encoding=encoding)
    return df
