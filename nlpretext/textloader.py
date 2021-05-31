import json
import re

import dask.bag as db
import dask.dataframe as dd

from nlpretext._utils.file_loader import check_text_file_format


class TextLoader():
    def __init__(
            self,
            text_column="text"):
        """
        Initialize DataLoader object to retrieve text data

        Parameters
        ----------
        text_column : string
            name of the column containing texts in json / csv
        """
        self.text_column = text_column
        self.file_format = ""

    def _read_text_txt(self, files_path):
        """
        Read txt text files stored in files_path

        Parameters
        ----------
        files_path : string | list[string]
            single or multiple files path

        Returns
        -------
        dask.dataframe
        """
        text_ddf = db.read_text(files_path).str.strip().to_dataframe()
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
        dask.dataframe
        """
        text_ddf = db.read_text(files_path).map((json.loads)).to_dataframe()
        return text_ddf[[self.text_column]]

    def _read_text_csv(self, files_path):
        """
        Read csv text files stored in files_path

        Parameters
        ----------
        files_path : string | list[string]
            single or multiple files path

        Returns
        -------
        dask.dataframe
        """
        text_ddf = dd.read_csv(files_path)
        return text_ddf[[self.text_column]]

    def read_text(self, files_path, compute_df=True):
        """
        Read the text files stored in files_path

        Parameters
        ----------
        files_path: string | list[string]
            single or multiple files path
        compute_df: bool
            True if user wants Dask Dataframe to be computed as pandas DF, False otherwise
        Returns
        -------
        dask.dataframe | pandas.DataFrame
        """
        self.file_format = check_text_file_format(files_path)

        reader_mapping = {"csv": self._read_text_csv,
                          "txt": self._read_text_txt,
                          "json": self._read_text_json}
        reader = reader_mapping.get(self.file_format)
        if reader is not None:
            text = reader(files_path)
        else:
            raise ValueError("Format not handled")

        if compute_df:
            return text.compute()
        return text
