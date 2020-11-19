import pytest
from nautilus_nlp.analysis.keyword_extractor import get_frequent_words, extract_keywords


@pytest.mark.parametrize(
    "input_tokens, expected, ngrams_number, number_top_words",
    [
        (['I', 'eat', 'orange', 'oranges', 'at', 'orange'], [('orange', 2)], 1, 1),
        (['Un', 'chat', 'rose', 'reste', 'un', 'chat', 'rose'], [('chat rose', 2)], 2, 1),
    ]
    )
def test_get_frequent_words(input_tokens, expected, ngrams_number, number_top_words):
    result = get_frequent_words(
        input_tokens, ngrams_number=ngrams_number, number_top_words=number_top_words)
    assert result == expected


def test_get_frequent_words_output_lenght():
    input_tokens = ['one', 'two', 'three', 'four', 'five', 'six', 'seven']
    assert len(get_frequent_words(input_tokens, number_top_words=5)) == 5


@pytest.mark.parametrize(
    "input_text, keyword, case_sensitive, expected",
    [
        ("I eat an orange oranges at Orange", 'orange', False, ['orange', 'orange']),
        ("I eat an orange oranges at Orange", 'orange', True, ['orange']),
        ("I eat an orange oranges at Orange", {'orange': ['orange', 'oranges']}, False, ['orange', 'orange', 'orange']),
        ("I eat an orange oranges at Orange", {'orange': ['orange', 'oranges']}, True, ['orange', 'orange']),
        ("I eat an orange oranges at Orange", {'fruit': ['orange', 'oranges']}, True, ['fruit', 'fruit']),
    ]
    )
def test_extract_keywords(input_text, keyword, case_sensitive, expected):
    assert extract_keywords(input_text, keyword=keyword, case_sensitive=case_sensitive) == expected
