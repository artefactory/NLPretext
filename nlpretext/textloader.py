import json

import dask.bag as db
import dask.dataframe as dd

from nlpretext._utils.file_loader import check_text_file_format


class TextLoader():
    def __init__(
            self,
            text_column="text",
            encoding="utf-8"):
        """
        Initialize DataLoader object to retrieve text data

        Parameters
        ----------
        text_column : string
            name of the column containing texts in json / csv
        """
        self.text_column = text_column
        self.file_format = ""
        self.encoding = encoding

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
        text_ddf = db.read_text(files_path, encoding=self.encoding).str.strip().to_dataframe()
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
        text_ddf = db.read_text(files_path, encoding=self.encoding).map((json.loads)).to_dataframe()
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
        dask.dataframe
        """
        text_ddf = dd.read_csv(files_path)
        try:
            return text_ddf[[self.text_column]]
        except KeyError:
            raise KeyError(f"Specified text_column '{self.text_column}' not in file keys")

    def read_text(self, files_path, is_computed=True, preprocessor=None):
        """
        Read the text files stored in files_path

        Parameters
        ----------
        files_path: string | list[string]
            single or multiple files path
        is_computed: bool
            True if user wants Dask Dataframe to be computed as pandas DF, False otherwise
        preprocessor: nlpretext.preprocessor.Preprocessor
            NLPretext preprocessor can be specified to pre-process text after loading

        Returns
        -------
        dask.dataframe | pandas.DataFrame
        """
        self.file_format = check_text_file_format(files_path)

        reader_mapping = {"csv": self._read_text_csv,
                          "txt": self._read_text_txt,
                          "json": self._read_text_json}
        reader = reader_mapping.get(self.file_format)
        if reader is None:
            raise ValueError("Format not handled")
        text = reader(files_path)

        if preprocessor is not None:
            text[self.text_column] = text[self.text_column].map(preprocessor.run)

        if is_computed:
            return text.compute()
        return text
