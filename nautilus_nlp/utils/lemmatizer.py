import spacy
import nltk
from french_lefff_lemmatizer.french_lefff_lemmatizer \
                                    import FrenchLefffLemmatizer
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import wordnet

try:
    french_spacy = spacy.load('fr')
except OSError:
    raise OSError("""You must install French langage to use SpaCy. 
                    python -m spacy download fr
                    See https://spacy.io/usage/ for details
                """)
try:
    english_spacy = spacy.load('en')
except OSError:
    raise OSError("""You must install english langage to use SpaCy. 
                    python -m spacy download en
                    See https://spacy.io/usage/ for details
                """)             




def lemmatize_french_tokens(tokens, module='spacy', load_only_pos='all'):
    '''
    Wrappers of french lemmatizers. SpaCy is much faster but sometimes 
    FrenchLefffLemmatizer returns more accurate results. Give a try to the 
    2 modules and choose the one that better fit your needs. 

    Args:
        tokens (list): list of tokens
        module ({'french_leff_v', 'spacy'}): modules availables.
        load_only_pos ({'a', v', 'r', 'n', 'all'}): If not "all", applies 
        lemmatization only to a certain POS tags, for french_leff_v module.
        a = adjectives, v = verbs, n = noun, r = adverb. 
        See https://github.com/ClaudeCoulombe/FrenchLefffLemmatizer.

    Returns:
        list of lemmatized tokens
    
    '''

    tokens = _make_sure_input_is_list_of_tokens(tokens)

    if module == 'french_leff_v':
        # Doc : https://github.com/ClaudeCoulombe/FrenchLefffLemmatizer
        lemmatizer = FrenchLefffLemmatizer()
        
        if load_only_pos == 'all':
            lemmatized_tokens = []
            for word in tokens:

                word = lemmatizer.lemmatize(word,'n')
                word = lemmatizer.lemmatize((word),'a') 
                word = lemmatizer.lemmatize((word),'r') 
                word = lemmatizer.lemmatize((word),'v') 
                lemmatized_tokens.append(word)

            return lemmatized_tokens
        else:
            return [lemmatizer.lemmatize(t, load_only_pos) for t in tokens]

    elif module == 'spacy':
        # Doc : https://spacy.io/api/token#attributes
        text = ' '.join(tokens)
        doc = french_spacy(text)
        return [token.lemma_ for token in doc]

    else:
        raise ValueError("must pass a valid module name!")


def lemmatize_english_tokens(tokens, module='spacy', pos_tag_prio='v'):
    '''
    Args:
        tokens (list): list of tokens
        module ({'french_leff_v', 'spacy'}): modules availables.
        pos_tag_prio ({'v', 'n', 'all'}): grammatical priority, applies
        for french_leff_v module. 

    Returns:
        list of lemmatized tokens
    
    '''
    tokens = _make_sure_input_is_list_of_tokens(tokens)

    if module == 'nltk':
        # Doc : https://github.com/ClaudeCoulombe/FrenchLefffLemmatizer
        lemmatizer = WordNetLemmatizer()
        return [lemmatizer.lemmatize(word, _get_wordnet_pos(word)) for word in tokens]

    elif module == 'spacy':
        # Doc : https://spacy.io/api/token#attributes
        text = ' '.join(tokens)
        doc = english_spacy(text)
        return [token.lemma_ for token in doc]

    else:
        raise ValueError("must pass a valid module name!")


def _get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)        


def _make_sure_input_is_list_of_tokens(tokens):
    if type(tokens) is list:
        return tokens
    elif tokens is None:
        return []
    elif type(tokens) is str:
        raise ValueError("must pass a list of tokens, not text!")    

