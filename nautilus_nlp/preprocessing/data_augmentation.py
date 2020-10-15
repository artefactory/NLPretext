import copy
import logging
import re

import nlpaug.augmenter.word as naw


class CouldNotAugment(ValueError):
    pass

class UnavailableAugmenter(ValueError):
    pass

def augment_text(text, method, stopwords=None, entities=None):
    """
    Given a text with or without associated entities, generate a new text by
    modifying some words in the initial one, modifications depend on the chosen
    method (substitution with synonym, addition, deletion). If entities are
    given as input, they will remain unchanged. If you want some words other
    than entities to remain unchanged, specify it within the stopwords argument.

    Parameters
    ----------
    text : string
    method : string
        augmenter to use ('wordnet_synonym' or 'aug_sub_bert')
    stopwords : list
        list of words to freeze throughout the augmentation
    entities : list
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
        formatted_entities = [(
            text[entities[i]['startCharIndex']:entities[i]['endCharIndex']].strip(),
            entities[i]['entity']) for i in range(len(entities))]
        if are_entities_in_augmented_text(entities, augmented_text):
            augmented_entities = get_augmented_entities(
                augmented_text,
                formatted_entities
            )
            return clean_sentence_entities(text, augmented_entities)
        raise CouldNotAugment('Text was not correctly augmented so not added')
    return augmented_text


def are_entities_in_augmented_text(entities, augmented_text):
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
        if ent['word'] not in augmented_text:
            check = False
    return check


def get_augmenter(method, stopwords=None):
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
    if method == 'wordnet_synonym':
        return naw.SynonymAug(aug_src='wordnet', stopwords=stopwords)
    if method == 'aug_sub_bert':
        return naw.ContextualWordEmbsAug(model_path='bert-base-uncased', action="substitute", stopwords=stopwords)
    raise UnavailableAugmenter('The given augmenter is not supported. You must choose one \
        of the following: wordnet_synonym or aug_sub_bert')


def get_augmented_entities(sentence_augmented, entities):
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
        regex = r'(?:^|\W)' + re.escape(entity[0].strip()) + r'(?:$|\W)'
        if (re.search(re.compile(regex), sentence_augmented)):
            start_index = re.search(regex, sentence_augmented).start()+1
            end_index = re.search(regex, sentence_augmented).end()-1
            new_entity = {
                'entity': entity[1],
                'word': sentence_augmented[start_index: end_index],
                'startCharIndex': start_index, 'endCharIndex': end_index}
            entities_augmented.append(new_entity)
    return entities_augmented


def clean_sentence_entities(text, entities):
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
    Augmented text and cleaned entities
    """
    entities_to_clean = copy.copy(entities)
    for element1 in entities_to_clean:
        for element2 in entities_to_clean:
            result = check_interval_included(element1, element2)
            if result is not None:
                try:
                    entities_to_clean.remove(result[0])
                except IndexError:
                    logging.warning(
                        "Cant remove entity : {} \n entities are now :{} \n for sentence : {} ".format(
                            result, entities_to_clean,
                            text))
                    continue
    return text, entities_to_clean


def check_interval_included(element1, element2):
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
    if ((element1 != element2) and (element1['startCharIndex'] >= element2['startCharIndex']) and
            (element1['endCharIndex'] <= element2['endCharIndex'])):
        return element1, element2
    if ((element1 != element2) and (element2['startCharIndex'] >= element1['startCharIndex']) and
            (element2['endCharIndex'] <= element1['endCharIndex'])):
        return element2, element1
    if ((element1 != element2) and (element1['startCharIndex'] >= element2['startCharIndex']) and
            (element1['endCharIndex'] >= element2['endCharIndex']) and
            (element1['startCharIndex'] <= element2['endCharIndex']-1)):
        return element1, element2
    if ((element1 != element2) and (element2['startCharIndex'] >= element1['startCharIndex']) and
            (element2['endCharIndex'] >= element1['endCharIndex']) and
            (element2['startCharIndex'] < element1['endCharIndex']-1)):
        return element2, element1
    return None
