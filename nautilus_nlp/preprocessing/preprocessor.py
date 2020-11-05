from inspect import getmembers, isfunction

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

from nautilus_nlp.preprocessing import social_preprocess
from nautilus_nlp.preprocessing import text_preprocess


class Preprocessor(object):
    def __init__(
            self, social_pipelines=None, text_pipelines=None):
        """
        """
        if social_pipelines is None:
            self.social_pipelines = Pipeline(
                steps=[(function_name, FunctionTransformer(function_callable))
                       for function_name, function_callable in getmembers(social_preprocess)
                       if isfunction(function_callable)])
        if text_pipelines is None:
            self.text_pipelines = Pipeline(
                steps=[(function_name, FunctionTransformer(function_callable))
                       for function_name, function_callable in getmembers(text_preprocess)
                       if isfunction(function_callable)])

    def apply_social_pipeline(self, text):
        return self.social_pipelines.fit_transform(text)

    def apply_text_pipeline(self, text):
        return self.text_pipelines.fit_transform(text)

    def apply_all_pipeline(self, text):
        text = self.apply_social_pipeline(text)
        text = self.apply_text_pipeline(text)
        return text
