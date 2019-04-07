import pytest
import numpy as np
from nautilus_nlp.utils.preprocess import (remove_multiple_spaces_and_strip_text, remove_accents)


@pytest.mark.parametrize("input_str, expected_str", [
    ("hello   world", "hello world"),
    ("\n   hello world    ", "hello world"),
    ("----- hello\tworld *****", "hello world"),
    ("hello-world", "hello-world"),
    ("hello - world", "hello world")
])

def test_remove_multiple_spaces_and_strip_text(input_str, expected_str):
    result = remove_multiple_spaces_and_strip_text(input_str)
    np.testing.assert_string_equal(result, expected_str)


def test_remove_accents():
    input_str = "éèëêàù"
    expected_str = "eeeeau"

    result = remove_accents(input_str)
    np.testing.assert_string_equal(result, expected_str)
