import pytest
from nlpretext.augmentation.text_augmentation import (
    process_entities_and_text, get_augmenter, CouldNotAugment,
    UnavailableAugmenter
)

@pytest.mark.parametrize(
    "text, text_augmented, entities, expected",
    [
        (
            "I want to buy a small black handbag.",
            "I want to acquire a small black handbag",
            [
                {'entity': 'Size', 'word': 'small', 'startCharIndex': 16, 'endCharIndex': 21},
                {'entity': 'Color', 'word': 'black', 'startCharIndex': 22, 'endCharIndex': 27},
                {'entity': 'Type', 'word': 'handbag', 'startCharIndex': 28, 'endCharIndex': 35}
            ],
            {'type':str, 'entities':['black', 'handbag', 'small']}
        ),
        (
            "I want to buy a small black handbag.",
            "I would like to buy a black small handbag",
            [
                {'entity': 'Size', 'word': 'small', 'startCharIndex': 16, 'endCharIndex': 21},
                {'entity': 'Color', 'word': 'black', 'startCharIndex': 22, 'endCharIndex': 27},
                {'entity': 'Type', 'word': 'handbag', 'startCharIndex': 28, 'endCharIndex': 35}
            ],
            {'type':str, 'entities':['black', 'handbag', 'small']}
        ),
    ]
)

def test_process_entities_and_text_not_altered(text, text_augmented, entities, expected):
    augmented_text, augmented_entities = process_entities_and_text(entities, text, text_augmented)
    augmented_entities = sorted([el['word'] for el in augmented_entities])
    assert {'type': type(augmented_text), 'entities': augmented_entities} == expected


@pytest.mark.parametrize(
    "text, text_augmented, entities",
    [
        (
            "I live in New York and I am looking for a lipstick",
            "I live in New and York I an looking for a lipstick",
            [
                {'entity': 'City', 'word': 'New York', 'startCharIndex': 10, 'endCharIndex': 18},
                {'entity': 'Type', 'word': 'bag', 'startCharIndex': 42, 'endCharIndex': 50}
            ]
        )
    ]
)

def test_process_entities_and_text_altered(text, text_augmented, entities):
    with pytest.raises(CouldNotAugment) as excinfo:
        process_entities_and_text(entities, text, text_augmented)
        assert str(excinfo.value) == 'Text was not correctly augmented because entities were altered'


def test_get_augmenter():
    method = 'ppdb_synonym'
    with pytest.raises(UnavailableAugmenter) as excinfo:
        get_augmenter(method)
        assert str(excinfo.value) == 'The given augmenter is not supported. You must choose one \
               of the following: wordnet_synonym or aug_sub_bert'
