import json

import dask.bag as db
import dask.dataframe as dd


class TextLoader():
    def __init__(
            self,
            file_format="txt",
            text_column="text"):
        """
        Initialize DataLoader object to retrieve text data

        Parameters
        ----------
        file_format : string
            file format to be read
        text_column : string
            name of the column containing texts in json / csv
        """
        self.text_column = text_column
        self.file_format = file_format

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

    def read_text(self, files_path):
        """
        Read the text files stored in files_path

        Parameters
        ----------
        files_path : string | list[string]
            single or multiple files path

        Returns
        -------
        dask.dataframe
        """
        reader_mapping = {"csv": self._read_text_csv,
                          "txt": self._read_text_txt,
                          "json": self._read_text_json}
        reader = reader_mapping.get(self.file_format)
        if reader is not None:
            text = reader(files_path)
        else:
            raise ValueError("Format not handled")
        return text.compute()
