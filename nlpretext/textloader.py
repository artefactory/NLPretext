try:
    import dask.bag as db
    import dask.dataframe as dd
except ImportError:
    raise ImportError("please install dask: pip install dask[complete]")

from nlpretext._utils.file_loader import check_text_file_format
from nlpretext.preprocessor import Preprocessor


class TextLoader:
    def __init__(self, text_column="text", encoding="utf-8", file_format=None):
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
        """
        self.text_column = text_column
        self.encoding = encoding
        self.file_format = file_format

    def __repr__(self):
        """
        Method to represent class attributes
        """
        class_repr_dict = {
            "text_column": self.text_column,
            "encoding": self.encoding,
            "file_format": self.file_format,
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
        text_ddf = dd.read_json(files_path, encoding=self.encoding)
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

    def _read_text_parquet(self, files_path):
        """
        Read parquet text files stored in files_path

        Parameters
        ----------
        files_path : string | list[string]
            single or multiple files path

        Returns
        -------
        dask.dataframe
        """
        text_ddf = dd.read_parquet(files_path)
        try:
            return text_ddf[[self.text_column]]
        except KeyError:
            raise KeyError(f"Specified text_column '{self.text_column}' not in file keys")

    def read_text(
        self, files_path, file_format=None, encoding=None, compute_to_pandas=True, preprocessor=None
    ):
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

        if compute_to_pandas:
            return text.compute()
        return text
