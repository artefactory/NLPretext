import dask.bag as db
import dask.dataframe as dd


def read_text(files_path, encoding):
    return db.read_text(files_path, encoding=encoding).str.strip().to_dataframe()


def read_json(files_path, encoding):
    return dd.read_json(files_path, encoding)


def read_csv(files_path, encoding):
    return dd.read_csv(files_path, encoding)


def read_parquet(files_path, encoding):
    return dd.read_parquet(files_path, encoding)
