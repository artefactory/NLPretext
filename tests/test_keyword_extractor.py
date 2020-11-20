import pytest
from nautilus_nlp.utils.keyword_extractor import extract_keywords


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
