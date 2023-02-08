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
from types import ModuleType
from typing import Any, List, Optional, Union

import sys
import warnings

import pandas as pd

try:
    from nlpretext._utils import daskloader
except ImportError:
    warnings.warn(
        "Dask not found, switching to pandas. To be able to use Dask, run : pip install dask[complete]"
    )

from nlpretext._utils import pandasloader
from nlpretext._utils.file_loader import check_text_file_format
from nlpretext.preprocessor import Preprocessor


class TextLoader:
    def __init__(self, text_column="text", encoding="utf-8", file_format=None, use_dask=True):
        """
        Initialize DataLoader object to retrieve text data

        Parameters
        ----------
        text_column: string
            name of the column containing texts in json / csv / parquet files
        encoding: string
            encoding of the text to be loaded, can be utf-8 or latin-1 for example
        file_format: string | None
            format of the files to be loaded
        use_dask: bool
            use dask to load text
        """
        self.text_column = text_column
        self.encoding = encoding
        self.file_format = file_format

        self.use_dask = use_dask

        self.loader: ModuleType
        if self.use_dask:
            if "dask" in sys.modules:
                self.loader = daskloader
            else:
                warnings.warn(
                    "Dask is not intalled, switching to pandas. Run pip install dask to use dask"
                )
                self.use_dask = False
                self.loader = pandasloader
        else:
            self.loader = pandasloader

    def __repr__(self):
        """
        Method to represent class attributes
        """
        class_repr_dict = {
            "text_column": self.text_column,
            "encoding": self.encoding,
            "file_format": self.file_format,
            "use_dask": self.use_dask,
        }
        return f"TextLoader({class_repr_dict})"

    def _read_text_txt(self, files_path):
        """
        Read txt text files stored in files_path

        Parameters
        ----------
        files_path : string | list[string]
            single or multiple files path

        Returns
        -------
        dask.dataframe | pandas.DataFrame
        """
        text_ddf = self.loader.read_text(files_path, encoding=self.encoding)
        text_ddf.columns = [self.text_column]
        return text_ddf

    def _read_text_json(self, files_path):
        """
        Read json text files stored in files_path

        Parameters
        ----------
        files_path : string | list[string]
            single or multiple files path

        Returns
        -------
        dask.dataframe | pandas.DataFrame
        """
        text_ddf = self.loader.read_json(files_path, encoding=self.encoding)
        try:
            return text_ddf[[self.text_column]]
        except KeyError:
            raise KeyError(f"Specified text_column '{self.text_column}' not in file keys")

    def _read_text_csv(self, files_path):
        """
        Read csv text files stored in files_path

        Parameters
        ----------
        files_path : string | list[string]
            single or multiple files path

        Returns
        -------
        dask.dataframe | pandas.DataFrame
        """
        text_ddf = self.loader.read_csv(files_path, encoding=self.encoding)
        try:
            return text_ddf[[self.text_column]]
        except KeyError:
            raise KeyError(f"Specified text_column '{self.text_column}' not in file keys")

    def _read_text_parquet(self, files_path):
        """
        Read parquet text files stored in files_path

        Parameters
        ----------
        files_path : string | list[string]
            single or multiple files path

        Returns
        -------
        dask.dataframe | pandas.DataFrame
        """
        text_ddf = self.loader.read_parquet(files_path, encoding=self.encoding)
        try:
            return text_ddf[[self.text_column]]
        except KeyError:
            raise KeyError(f"Specified text_column '{self.text_column}' not in file keys")

    def read_text(
        self,
        files_path: Union[str, List[str]],
        file_format: Optional[str] = None,
        encoding: Optional[str] = None,
        compute_to_pandas: bool = True,
        preprocessor: Optional[Preprocessor] = None,
    ) -> Union[pd.DataFrame, Any]:
        """
        Read the text files stored in files_path

        Parameters
        ----------
        files_path: string | list[string]
            single or multiple files path
        file_format: string
            Format of the files to be loaded, to be selected among csv, json, parquet or txt
        encoding:
            encoding of the text to be loaded, can be utf-8 or latin-1 for example
        compute_to_pandas: bool
            True if user wants Dask Dataframe to be computed as pandas DF, False otherwise
        preprocessor: nlpretext.preprocessor.Preprocessor
            NLPretext preprocessor can be specified to pre-process text after loading

        Returns
        -------
        dask.dataframe | pandas.DataFrame
        """
        if encoding is not None:
            self.encoding = encoding

        if file_format is not None:
            self.file_format = file_format
        else:
            self.file_format = check_text_file_format(files_path)

        reader_mapping = {
            "csv": self._read_text_csv,
            "txt": self._read_text_txt,
            "json": self._read_text_json,
            "parquet": self._read_text_parquet,
        }
        reader = reader_mapping.get(self.file_format)
        if reader is None:
            raise ValueError("Format not handled")
        text = reader(files_path)

        if preprocessor is not None:
            if isinstance(preprocessor, Preprocessor):
                print(f"before: {text.head()}")
                text[self.text_column] = text[self.text_column].apply(preprocessor.run)
                print(f"after: {text.head()}")
            else:
                raise ValueError("Only NLPretext preprocessors can be specified")

        if compute_to_pandas and self.use_dask:
            return text.compute()
        return text
