from typing import List, Callable

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

from nlpretext.social.preprocess import (
    remove_html_tags, remove_mentions, remove_emoji, remove_hashtag)
from nlpretext.basic.preprocess import normalize_whitespace, remove_eol_characters, fix_bad_unicode


class Preprocessor():
    def __init__(
            self):
        """
        Initialize preprocessor object to apply all text transformation
        """
        self.__operations = []
        self.pipeline = None

    def pipe(self, operation: Callable, args: dict = None):
        """
        Add an operation and its arguments to pipe in the preprocessor

        Parameters
        ----------
        operation : callable
            text preprocessing function
        args : dict of arguments
        """
        self.__operations.append({
            'operation': operation,
            'args': args
        })


    @staticmethod
    def build_pipeline(operation_list: List[dict]) -> Pipeline:
        """
        Build sklearn pipeline from a operation list

        Parameters
        ----------
        operation_list : iterable
            list of __operations of preprocessing

        Returns
        -------
        sklearn.pipeline.Pipeline
        """
        return Pipeline(
            steps=[
                (
                    operation['operation'].__name__,
                    FunctionTransformer(operation['operation'], kw_args=operation['args'])
                )
                for operation in operation_list])


    def run(self, text: str) -> str:
        """
        Apply pipeline to text

        Parameters
        ----------
        text : string
            text to preprocess

        Returns
        -------
        string
        """
        operations = self.__operations
        if operations == []:
            operations_to_pipe = (
                remove_html_tags, remove_mentions, remove_emoji, remove_hashtag,
                remove_eol_characters, fix_bad_unicode, normalize_whitespace
            )
            operations = [{'operation': operation, 'args': None} for operation in operations_to_pipe]
        self.pipeline = self.build_pipeline(operations)
        text = self.pipeline.fit_transform(text)
        return text
