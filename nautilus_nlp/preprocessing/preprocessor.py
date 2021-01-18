from typing import List, Callable, Optional

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

from nautilus_nlp.preprocessing.social_preprocess import (remove_html_tags, remove_mentions, remove_emoji,
                                                          remove_hashtag)
from nautilus_nlp.preprocessing.text_preprocess import normalize_whitespace, remove_eol_characters, fix_bad_unicode


class Preprocessor():
    def __init__(
            self,
            functions: Optional[Callable] = None):
        """
        Initialize preprocessor object to apply all text transformation

        Parameters
        ----------
        functions : iterable|None
            list of functions of preprocessing
        """
        if functions is None:
            functions = (remove_html_tags, remove_mentions, remove_emoji, remove_hashtag,
                         remove_eol_characters, fix_bad_unicode, normalize_whitespace)
        if len(functions) == 0:
            raise ValueError("Cannot initialize a preprocessor with 0 function")
        self.pipeline = self.build_pipeline(functions)

    @staticmethod
    def build_pipeline(function_list: List[Callable]) -> Pipeline:
        """
        Build sklearn pipeline from a function list

        Parameters
        ----------
        function_list : iterable
            list of functions of preprocessing

        Returns
        -------
        sklearn.pipeline.Pipeline
        """
        return Pipeline(
            steps=[
                (function.__name__, FunctionTransformer(function))
                for function in function_list])


    def apply_pipeline(self, text: str) -> str:
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
        text = self.pipeline.fit_transform(text)
        return text
