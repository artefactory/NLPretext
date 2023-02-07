from typing import List, Union

import pandas as pd
from fsspec import open_files


def _list_handler(func):
    def wrapper_list_handler(file_path: Union[str, List[str]], *args, **kwargs) -> pd.DataFrame:  # type: ignore
        list_files = open_files(file_path)
        list_df = [func(file.path, *args, **kwargs) for file in list_files]
        df = pd.concat(list_df)
        return df

    return wrapper_list_handler


@_list_handler
def read_text(file_path: str, encoding: str) -> pd.DataFrame:
    df = pd.read_fwf(file_path, encoding=encoding, colspecs=[(None, None)])
    return df


@_list_handler
def read_json(file_path: str, encoding: str) -> pd.DataFrame:
    df = pd.read_json(file_path, encoding=encoding)
    return df


@_list_handler
def read_csv(file_path: str, encoding: str) -> pd.DataFrame:
    df = pd.read_csv(file_path, encoding=encoding)
    return df


@_list_handler
def read_parquet(file_path: str, encoding: str) -> pd.DataFrame:
    df = pd.read_parquet(file_path, encoding=encoding)
    return df
