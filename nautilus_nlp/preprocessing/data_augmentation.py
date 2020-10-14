import copy
import logging
import re

import nlpaug.augmenter.word as naw


class CouldNotAugment(ValueError):
    pass

class UnavailableAugmenter(ValueError):
    pass

def augment_utterance(text, method, stopwords, intent=None, entities=None):
    """
    Given ``text`` str, create a new similar utterance by modifying some words
    in the initial sentence, modifications depend on the chosen method
    (substitution with synonym, addition, deletion). If intent and/or entities
    are given as input, they will remain unchanged.

    Parameters
    ----------
    text : string
    method : string
        augmenter to use ('wordnet_synonym' or 'aug_sub_bert')
    stopwords : list
        list of words to freeze throughout the augmentation
    intent : string
        intent associated to text if any
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
    dictionary with augmented text and optional keys depending on input
    """
    new_utt = {}
    augmenter = get_augmenter(method, stopwords)
    new_utt['text'] = augmenter.augment(text)
    if intent is not None:
        new_utt['intent'] = intent
    if entities is not None:
        formatted_entities = [(
            text[entities[i]['startCharIndex']:entities[i]['endCharIndex']].strip(),
            entities[i]['entity']) for i in range(len(entities))]
        if are_entities_in_augmented_text(entities, new_utt['text']):
            new_utt['entities'] = get_augmented_entities(
                new_utt['text'],
                formatted_entities
            )
            return clean_sentence_entities(new_utt)
        raise CouldNotAugment('Text was not correctly augmented so not added')
    return new_utt


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
    raise UnavailableAugmenter('The given augmenter is not supported yet')


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


def clean_sentence_entities(sentence_input):
    """
    Paired entities check to remove nested entities, the longest entity is kept

    Parameters
    ----------
    sentence_input : dict
        dictionary in the following format
        {
            'text' : str,
            'entities' : list of dict,
            'intent' : str (optional)
        }

    Returns
    -------
    Sentence input with cleaned entities
    """
    sentence = copy.copy(sentence_input)
    for element1 in sentence['entities']:
        for element2 in sentence['entities']:
            result = check_interval_included(element1, element2)
            if result is not None:
                try:
                    sentence[1]['entities'].remove(result[0])
                except IndexError:
                    logging.warning(
                        "Cant remove entity : {} \n entities are now :{} \n for sentence : {} ".format(
                            result, sentence['entities'],
                            sentence['text']))
                    continue
    return sentence


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
