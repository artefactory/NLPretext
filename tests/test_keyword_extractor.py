import pytest
from nautilus_nlp.analysis.keyword_extractor import get_frequent_words


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
