from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

from nautilus_nlp.preprocessing.social_preprocess import (remove_html_tags, remove_mentions, remove_emoji,
                                                          remove_hashtag)
from nautilus_nlp.preprocessing.text_preprocess import normalize_whitespace, remove_eol_characters, fix_bad_unicode


class Preprocessor():
    def __init__(
            self, social_functions=None, text_functions=None):
        """
        """
        if social_functions is None:
            social_functions = (remove_html_tags, remove_mentions, remove_emoji, remove_hashtag)
        if text_functions is None:
            text_functions = (remove_eol_characters, fix_bad_unicode, normalize_whitespace)
        self.social_pipeline = self.build_pipeline(social_functions)
        self.text_pipeline = self.build_pipeline(text_functions)

    @staticmethod
    def build_pipeline(function_list):
        return Pipeline(
            steps=[
                (function.__name__, FunctionTransformer(function))
                for function in function_list])


    @staticmethod
    def apply_pipeline(text, pipeline):
        return pipeline.fit_transform(text)

    def apply_all_pipeline(self, text):
        text = self.apply_pipeline(text, self.social_pipeline)
        text = self.apply_pipeline(text, self.text_pipeline)
        return text
