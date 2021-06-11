# GNU Lesser General Public License v3.0 only
# Copyright (C) 2020 Artefact
# licence-information@artefact.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from unittest.mock import MagicMock, patch
try:
    import dask.bag as db
    import dask.dataframe as dd
except ImportError:
    raise ImportError('please install dask: pip install dask[complete]')

try:
    import pandas as pd
except ImportError:
    raise ImportError('please install pandas: pip install pandas')
from pandas.testing import assert_frame_equal
import pytest

from nlpretext.preprocessor import Preprocessor
from nlpretext.textloader import TextLoader


# pylint: disable=protected-access

@patch("dask.bag.read_text")
def test__read_text_txt(mock_read_text):
    # Given
    files_path = "some_path/to_read.txt"
    file_format = "txt"
    encoding = "utf-8"
    text_column = "text"
    mock_read_text.return_value = db.from_sequence(["This is a text \n", "This is another text \n"])

    expected_result = dd.from_pandas(pd.DataFrame({text_column: ["This is a text", "This is another text"]}),
                                     npartitions=2)

    # When
    dummy_instance = TextLoader(file_format=file_format, encoding=encoding, text_column=text_column)
    actual_result = dummy_instance._read_text_txt(files_path)

    # Then
    mock_read_text.assert_called_once_with(files_path, encoding=encoding)
    assert_frame_equal(expected_result.compute(), actual_result.compute().reset_index(drop=True))


@patch("dask.dataframe.read_json")
def test__read_text_json(mock_read_json):
    # Given
    files_path = "some_path/to_read.json"
    file_format = "json"
    encoding = "utf-8"
    text_column = "text"

    text_ddf = dd.from_pandas(pd.DataFrame({text_column: ["This is a text", "This is another text"]}),
                              npartitions=2)
    mock_read_json.return_value = text_ddf

    expected_result = text_ddf[[text_column]]

    # When
    dummy_instance = TextLoader(file_format=file_format, encoding=encoding, text_column=text_column)
    actual_result = dummy_instance._read_text_json(files_path)

    # Then
    mock_read_json.assert_called_once_with(files_path, encoding=encoding)
    assert_frame_equal(expected_result.compute(), actual_result.compute())


@patch("dask.dataframe.read_csv")
def test__read_text_csv(mock_read_csv):
    # Given
    files_path = "some_path/to_read.csv"
    file_format = "csv"
    encoding = "utf-8"
    text_column = "text"

    text_ddf = dd.from_pandas(pd.DataFrame({text_column: ["This is a text", "This is another text"]}),
                              npartitions=2)
    mock_read_csv.return_value = text_ddf

    expected_result = text_ddf[[text_column]]

    # When
    dummy_instance = TextLoader(file_format=file_format, encoding=encoding, text_column=text_column)
    actual_result = dummy_instance._read_text_csv(files_path)

    # Then
    mock_read_csv.assert_called_once_with(files_path)
    assert_frame_equal(expected_result.compute(), actual_result.compute())


@patch("dask.dataframe.read_parquet")
def test__read_text_parquet(mock_read_parquet):
    # Given
    files_path = "some_path/to_read.parquet"
    file_format = "parquet"
    encoding = "utf-8"
    text_column = "text"

    text_ddf = dd.from_pandas(pd.DataFrame({text_column: ["This is a text", "This is another text"]}),
                              npartitions=2)
    mock_read_parquet.return_value = text_ddf

    expected_result = text_ddf[[text_column]]

    # When
    dummy_instance = TextLoader(file_format=file_format, encoding=encoding, text_column=text_column)
    actual_result = dummy_instance._read_text_parquet(files_path)

    # Then
    mock_read_parquet.assert_called_once_with(files_path)
    assert_frame_equal(expected_result.compute(), actual_result.compute())


@pytest.mark.parametrize(
    "files_path, file_format, encoding, compute_to_pandas, preprocessor, expected_format, raised",
    [
        ("text_file1.json", None, None, True, None, "json", None),
        ("text_file2.json", "json", None, True, None, "json", None),
        ("text_file3.csv", None, "utf-8", True, None, "csv", None),
        ("text_file4.csv", None, None, False, None, "csv", None),
        ("text_file3.parquet", None, "utf-8", True, None, "parquet", None),
        ("text_file4.parquet", None, None, False, None, "parquet", None),
        ("text_file5.pdf", "pdf", None, False, None, "csv", "Format not handled"),
        ("text_file6.txt", None, None, False, Preprocessor(), "txt", None),
        ("text_file8.txt", None, None, False, MagicMock(), "txt", "Only NLPretext preprocessors can be specified"),
    ])
@patch("nlpretext.preprocessor.Preprocessor.run")
@patch("nlpretext.textloader.TextLoader._read_text_json")
@patch("nlpretext.textloader.TextLoader._read_text_txt")
@patch("nlpretext.textloader.TextLoader._read_text_csv")
@patch("nlpretext.textloader.TextLoader._read_text_parquet")
@patch("nlpretext.textloader.check_text_file_format")
def test_read_text(mock_check_text_file_format,
                   mock__read_text_parquet,
                   mock__read_text_csv,
                   mock__read_text_txt,
                   mock__read_text_json,
                   mock_run,
                   files_path,
                   file_format,
                   encoding,
                   compute_to_pandas,
                   preprocessor,
                   expected_format,
                   raised):

    # Given
    text_column = "text"
    if encoding is None:
        encoding = "utf-8"

    if file_format is None:
        mock_check_text_file_format.return_value = expected_format

    mock_reader_mapping = {"csv": mock__read_text_csv,
                           "txt": mock__read_text_txt,
                           "json": mock__read_text_json,
                           "parquet": mock__read_text_parquet}

    expected_result = dd.from_pandas(
        pd.DataFrame({text_column: ["Text with #", "Text with  double  space"]}),
        npartitions=2)
    mock_reader_mapping.get(expected_format).return_value = expected_result

    # When
    dummy_textloader = TextLoader(text_column=text_column,
                                  encoding=encoding,
                                  file_format=file_format)

    if raised is None:
        actual_result = dummy_textloader.read_text(files_path, file_format, encoding, compute_to_pandas, preprocessor)

        # Then
        if file_format is None:
            mock_check_text_file_format.assert_called_once_with(files_path)

        mock_reader_mapping.get(expected_format).assert_called_once_with(files_path)

        if preprocessor is not None:
            if isinstance(preprocessor, Preprocessor):
                mock_run.assert_called()
                preprocessed_texts = ["Text with", "Text with double space"]
                mock_run.side_effect = preprocessed_texts
                expected_result = dd.from_pandas(pd.DataFrame({text_column: preprocessed_texts}), npartitions=2)

        if not compute_to_pandas:
            actual_result = actual_result.compute()
        assert_frame_equal(expected_result.compute(), actual_result)

    else:
        with pytest.raises(ValueError, match=raised):
            dummy_textloader.read_text(files_path, file_format, encoding, compute_to_pandas, preprocessor)
