# mypy: disable-error-code="attr-defined"
from typing import Any, List, Union

import dask.bag as db
import dask.dataframe as dd


def read_text(files_path: Union[str, List[str]], encoding: str):  # type: ignore
    return db.read_text(files_path, encoding=encoding).str.strip().to_dataframe()


def read_json(files_path: Union[str, List[str]], encoding: str):  # type: ignore
    return dd.read_json(files_path, encoding=encoding)


def read_csv(files_path: Union[str, List[str]], encoding: str):  # type: ignore
    return dd.read_csv(files_path, encoding=encoding)


def read_parquet(files_path: Union[str, List[str]], encoding: str):  # type: ignore
    return dd.read_parquet(files_path, encoding=encoding)
