import pytest
from nautilus_nlp.preprocessing.data_augmentation import augment_text, CouldNotAugment, UnavailableAugmenter

@pytest.mark.parametrize(
    "text, method, stopwords, entities, expected",
    [
        (
            "I want to buy a small black handbag.",
            'wordnet_synonym',
            ['small', 'black', 'handbag'],
            [
                {'entity': 'Size', 'word': 'small', 'startCharIndex': 16, 'endCharIndex': 21},
                {'entity': 'Color', 'word': 'black', 'startCharIndex': 22, 'endCharIndex': 27},
                {'entity': 'Type', 'word': 'handbag', 'startCharIndex': 28, 'endCharIndex': 35}
            ],
            {'type':str, 'entities':['black', 'handbag', 'small']}
        ),
        (
            "I want to buy a small black handbag.",
            'aug_sub_bert',
            ['small', 'black', 'handbag'],
            [
                {'entity': 'Size', 'word': 'small', 'startCharIndex': 16, 'endCharIndex': 21},
                {'entity': 'Color', 'word': 'black', 'startCharIndex': 22, 'endCharIndex': 27},
                {'entity': 'Type', 'word': 'handbag', 'startCharIndex': 28, 'endCharIndex': 35}
            ],
            {'type':str, 'entities':['black', 'handbag', 'small']}
        ),
        (
            "I live in New York and I am looking for a lipstick",
            'wordnet_synonym',
            ['New York', 'lipstick'],
            [
                {'entity': 'City', 'word': 'New York', 'startCharIndex': 10, 'endCharIndex': 18},
                {'entity': 'Type', 'word': 'bag', 'startCharIndex': 42, 'endCharIndex': 50}
            ],
            {'type':str, 'entities':['lipstick', 'New York']}
        ),
        (
            "I live in New York and I am looking for a lipstick",
            'ppdb_synonym',
            ['New York', 'lipstick'],
            [
                {'entity': 'City', 'word': 'New York', 'startCharIndex': 10, 'endCharIndex': 18},
                {'entity': 'Type', 'word': 'bag', 'startCharIndex': 42, 'endCharIndex': 50}
            ],
            {}
        ),
        (
            "I want to buy a small black bag",
            'aug_sub_bert',
            None,
            None,
            {'type':str}
        )
    ]
    )

def test_data_augmentation(text, method, stopwords, entities, expected):
    if method not in ['aug_sub_bert', 'wordnet_synonym']:
        with pytest.raises(UnavailableAugmenter) as excinfo:
            augment_text(text, method, stopwords, entities)
            assert str(excinfo.value) == 'The given augmenter is not supported. You must choose one \
                of the following: wordnet_synonym or aug_sub_bert'
    else:
        if entities is not None:
            try:
                augmented_text, augmented_entities = augment_text(text, method, stopwords, entities)
                augmented_entities = sorted([el['word'] for el in augmented_entities])
                assert {'type': type(augmented_text), 'entities': augmented_entities} == expected
            except CouldNotAugment:
                assert True
        else:
            assert {'type': type(augment_text(text, method, stopwords, entities))} == expected
