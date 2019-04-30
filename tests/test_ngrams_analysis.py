import pandas as pd
import pytest
from nautilus_nlp.utils.ngrams_analysis import frequent_words


def test_frequent_words():
    list_words = ['Hello', 'world', 'this', 'is', 'an', 'example', 'of', 'ngrams', 'count', 'an', 'example',
                  'to', 'test', 'this', 'is', 'an', 'example', 'function', 'hello', 'world']

    df1 = frequent_words(list_words, 1, 5)
    df2 = frequent_words(list_words, 2, 5)
    df3 = frequent_words(list_words, 3, 3)

    res_df1 = pd.DataFrame({'Entity': ['an', 'example', 'world', 'this', 'is'], 'Counts': [3, 3, 2, 2, 2]})
    res_df2 = pd.DataFrame({'Entity': ['an example', 'this is', 'is an', 'Hello world', 'world this'], 'Counts': [3, 2, 2, 1, 1]})
    res_df3 = pd.DataFrame({'Entity': ['this is an', 'is an example', 'Hello world this'], 'Counts': [2, 2, 1]})

    pd.testing.assert_frame_equal(df1, res_df1)
    pd.testing.assert_frame_equal(df2, res_df2)
    pd.testing.assert_frame_equal(df3, res_df3)


