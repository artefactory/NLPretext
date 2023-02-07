from typing import Any, Dict, List, Optional, Tuple

import logging
import re
from itertools import combinations

import nlpaug.augmenter.word as naw


class CouldNotAugment(ValueError):
    pass


class UnavailableAugmenter(ValueError):
    pass


def augment_text(
    text: str,
    method: str,
    stopwords: Optional[List[str]] = None,
    entities: Optional[List[Dict[str, Any]]] = None,
) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Given a text with or without associated entities, generate a new text by
    modifying some words in the initial one, modifications depend on the chosen
    method (substitution with synonym, addition, deletion). If entities are
    given as input, they will remain unchanged. If you want some words other
    than entities to remain unchanged, specify it within the stopwords argument.

    Parameters
    ----------
    text : string
    method : {'wordnet_synonym', 'aug_sub_bert'}
        augmenter to use ('wordnet_synonym' or 'aug_sub_bert')
    stopwords : list, optional
        list of words to freeze throughout the augmentation
    entities : list, optional
        entities associated to text if any, must be in the following format:
        [
            {
                'entity': str,
                'word': str,
                'startCharIndex': int,
                'endCharIndex': int
            },
            {
                ...
            }
        ]

    Returns
    -------
    Augmented text and optional augmented entities
    """
    augmenter = get_augmenter(method, stopwords)
    augmented_text = augmenter.augment(text)
    if entities is not None:
        return process_entities_and_text(entities, text, augmented_text)
    return augmented_text, []


def process_entities_and_text(
    entities: List[Dict[str, Any]], text: str, augmented_text: str
) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Given a list of initial entities, verify that they have not been altered by
    the data augmentation operation and are still in the augmented text.
    Parameters
    ----------
    entities: list
        entities associated to text, must be in the following format:
        [
            {
                'entity': str,
                'word': str,
                'startCharIndex': int,
                'endCharIndex': int
            },
            {
                ...
            }
        ]
    text: str
        initial text
    augmented_text: str
        new text resulting of data augmentation operation
    Returns
    -------
    Augmented text and entities with their updated position in augmented text
    """
    formatted_entities = [
        (
            text[entities[i]["startCharIndex"] : entities[i]["endCharIndex"]].strip(),
            entities[i]["entity"],
        )
        for i in range(len(entities))
    ]
    if are_entities_in_augmented_text(entities, augmented_text):
        augmented_entities = get_augmented_entities(augmented_text, formatted_entities)
        clean_entities = clean_sentence_entities(augmented_text, augmented_entities)
        return augmented_text, clean_entities
    raise CouldNotAugment("Text was not correctly augmented because entities were altered")


def are_entities_in_augmented_text(entities: List[Dict[str, Any]], augmented_text: str) -> bool:
    """
    Given a list of entities, check if all the words associated to each entity
    are still present in augmented text.

    Parameters
    ----------
    entities : list
        entities associated to initial text, must be in the following format:
        [
            {
                'entity': str,
                'word': str,
                'startCharIndex': int,
                'endCharIndex': int
            },
            {
                ...
            }
        ]
    augmented_text : str

    Returns
    -------
    True if all entities are present in augmented text, False otherwise
    """
    check = True
    for ent in entities:
        if ent["word"] not in augmented_text:
            check = False
            return check
    return check


def get_augmenter(method: str, stopwords: Optional[List[str]] = None) -> naw.SynonymAug:
    """
    Initialize an augmenter depending on the given method.

    Parameters
    ----------
    method : str (supported methods: wordnet_synonym and aug_sub_bert)
    stopwords : list
        list of words to freeze throughout the augmentation

    Returns
    -------
    Initialized nlpaug augmenter
    """
    if method == "wordnet_synonym":
        return naw.SynonymAug(aug_src="wordnet", stopwords=stopwords)
    if method == "aug_sub_bert":
        return naw.ContextualWordEmbsAug(
            model_path="bert-base-uncased", action="substitute", stopwords=stopwords
        )
    raise UnavailableAugmenter(
        "The given augmenter is not supported. You must choose one \
        of the following: wordnet_synonym or aug_sub_bert"
    )


def get_augmented_entities(
    sentence_augmented: str, entities: List[Tuple[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Get entities with updated positions (start and end) in augmented text

    Parameters
    ----------
    sentence_augmented : str
        augmented text
    entities : list
        entities associated to initial text, must be in the following format:
        [
            {
                'entity': str,
                'word': str,
                'startCharIndex': int,
                'endCharIndex': int
            },
            {
                ...
            }
        ]

    Returns
    -------
    Entities with updated positions related to augmented text
    """
    entities_augmented = []
    for entity in entities:
        search = re.search(entity[0].strip(), sentence_augmented)
        if search:
            start_index = search.start()
            end_index = search.end()
            new_entity = {
                "entity": entity[1],
                "word": sentence_augmented[start_index:end_index],
                "startCharIndex": start_index,
                "endCharIndex": end_index,
            }
            entities_augmented.append(new_entity)
    return entities_augmented


def clean_sentence_entities(text: str, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Paired entities check to remove nested entities, the longest entity is kept

    Parameters
    ----------
    text : str
        augmented text
    entities : list
        entities associated to augmented text, must be in the following format:
        [
            {
                'entity': str,
                'word': str,
                'startCharIndex': int,
                'endCharIndex': int
            },
            {
                ...
            }
        ]

    Returns
    -------
    Cleaned entities
    """
    entities_to_clean = [dict(s) for s in {frozenset(d.items()) for d in entities}]
    for element1, element2 in combinations(entities_to_clean, 2):
        result = check_interval_included(element1, element2)
        if result is not None:
            try:
                entities_to_clean.remove(result[0])
            except IndexError:
                logging.warning(
                    "Cant remove entity : {} \n entities are now :{} \n for sentence : {} ".format(
                        result, entities_to_clean, text
                    )
                )
                continue
    return entities_to_clean


def check_interval_included(
    element1: Dict[str, Any], element2: Dict[str, Any]
) -> Optional[Tuple[Dict[str, Any], Dict[str, Any]]]:
    """
    Comparison of two entities on start and end positions to find if they are nested

    Parameters
    ----------
    element1 : dict
    element2 : dict
        both of them in the following format
        {
            'entity': str,
            'word': str,
            'startCharIndex': int,
            'endCharIndex': int
        }

    Returns
    -------
    If there is an entity to remove among the two returns a tuple (element to remove, element to keep)
    If not, returns None
    """
    if (
        (element1 != element2)
        and (element1["startCharIndex"] >= element2["startCharIndex"])
        and (element1["endCharIndex"] <= element2["endCharIndex"])
    ):
        return element1, element2
    if (
        (element1 != element2)
        and (element2["startCharIndex"] >= element1["startCharIndex"])
        and (element2["endCharIndex"] <= element1["endCharIndex"])
    ):
        return element2, element1
    if (
        (element1 != element2)
        and (element1["startCharIndex"] >= element2["startCharIndex"])
        and (element1["endCharIndex"] >= element2["endCharIndex"])
        and (element1["startCharIndex"] <= element2["endCharIndex"] - 1)
    ):
        return element1, element2
    if (
        (element1 != element2)
        and (element2["startCharIndex"] >= element1["startCharIndex"])
        and (element2["endCharIndex"] >= element1["endCharIndex"])
        and (element2["startCharIndex"] < element1["endCharIndex"] - 1)
    ):
        return element2, element1
    return None
