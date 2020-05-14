import copy
import logging
import nlpaug.augmenter.word as naw
import re

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
    if entities:
        formatted_entities = [(text[entities[i]['startCharIndex']:entities[i]['endCharIndex']].strip(),entities[i]['entity']) for i in range(len(entities))]
    augmenter = select_augmenter(method,stopwords)
    new_utt['text'] = augmenter.augment(text)
    if intent:
        new_utt['intent'] = intent
    if entities:
        if are_entities_in_augmented_text(entities,new_utt['text']):        
            new_utt['entities'] = get_augmented_entities(new_utt['text'],formatted_entities)
            return clean_sentence_entities(new_utt)
        else:
            logging.info('Text was not correctly augmented so not added')
    else:
        return new_utt

def are_entities_in_augmented_text(entities,augmented_text):
    check = True
    for ent in entities:
        if ent['word'] not in augmented_text:
            check = False
    return check

def select_augmenter(method,stopwords,use_stopwords=True):
    if use_stopwords:
        stopwords = stopwords
    else: 
        stopwords = []
    if method == 'wordnet_synonym':
        augmenter = naw.SynonymAug(aug_src='wordnet',stopwords=stopwords)
    elif method == 'aug_sub_bert':
        augmenter = naw.ContextualWordEmbsAug(model_path='bert-base-uncased', action="substitute",stopwords=stopwords)  
    return(augmenter) 

def get_augmented_entities(sentence_augmented,entities):
    entities_augmented = []
    for entity in entities :
        regex = r'(?:^|\W)' + re.escape(entity[0].strip()) + '(?:$|\W)'
        if (re.search(re.compile(regex), sentence_augmented)):
            start_index = re.search(regex,sentence_augmented).start()+1
            end_index = re.search(regex,sentence_augmented).end()-1
            new_entity = {'entity': entity[1],'word': sentence_augmented[start_index:end_index],'startCharIndex': start_index,'endCharIndex': end_index}
            entities_augmented.append(new_entity) 
    return entities_augmented

def clean_sentence_entities(sentence_input):
    sentence = copy.copy(sentence_input)
    for element1 in sentence['entities']: 
        for element2 in sentence['entities'] :
            result = check_interval_included(element1,element2)
            if result:
                try :                                                                       
                    sentence[1]['entities'].remove(result[0])
                except : 
                    logging.info("Cant remove entity : {} \n entities are now :{} \n for sentence : {} ".format(result,sentence['entities'],sentence['text']))
                    continue
    return(sentence)       

def check_interval_included(element1,element2):
    if ((element1 != element2) and (element1['startCharIndex'] >= element2['startCharIndex']) and (element1['endCharIndex'] <= element2['endCharIndex'])):
        return((element1,element2))
    elif ((element1 != element2) and (element2['startCharIndex'] >= element1['startCharIndex']) and (element2['endCharIndex'] <= element1['endCharIndex'])):
        return((element2,element1))
    elif ((element1 != element2) and (element1['startCharIndex'] >= element2['startCharIndex']) and (element1['endCharIndex'] >= element2['endCharIndex']) and (element1['startCharIndex'] <= element2['endCharIndex']-1)):
        return((element1,element2))
    elif ((element1 != element2) and (element2['startCharIndex'] >= element1['startCharIndex']) and (element2['endCharIndex'] >= element1['endCharIndex']) and (element2['startCharIndex'] < element1['endCharIndex']-1)):
        return((element2,element1))
    else :
        return(False)