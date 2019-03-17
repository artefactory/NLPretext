from nltk.stem.snowball import *


def stem_tokens(tokens: list, lang: str ='english'):
    '''
    Wrapper of NLTK's stemmers : http://www.nltk.org/howto/stem.html

    Args:
        tokens (list): list of tokens
        lang ({'arabic', 'danish', 'dutch', 'english', 'finnish', 'french',
        'german', 'hungarian', 'italian', 'norwegian', 'porter', 'portuguese', 
        'romanian', 'russian', 'spanish', 'swedish'}): supported langages

    Returns:
        list of stemmed tokens
    
    '''
    supported_lang = [lang for lang in SnowballStemmer.languages]
    
    if lang in supported_lang:
        stemmer = eval(lang.capitalize()+'Stemmer()')
    else:
        raise ValueError("Langage not supported of mispelled")
        
    if type(tokens) is list:
        return [stemmer.stem(token) for token in tokens]
    elif tokens is None:
        return []
    elif type(tokens) is str:
        raise ValueError("must pass a list of tokens, not text!")
