import nltk
from sacremoses import MosesTokenizer, MosesDetokenizer
import spacy

nltk.download('punkt')

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


def tokenize(text: str, lang_module: str = 'en_spacy'):
    """
    Inputs string output a list of tokens
    French = "J' ai" >>> ["J'", 'ai']
    """
    if lang_module is 'en_nltk':
        return nltk.word_tokenize(text)
    elif lang_module is 'en_spacy':
        spacydoc = english_spacy(text)
        return [tokens.text for tokens in spacydoc]
    elif lang_module is 'fr_spacy':
        spacydoc = french_spacy(text)
        return [tokens.text for tokens in spacydoc]
    elif lang_module is 'fr_moses':
        t = MosesTokenizer(lang='fr')
        return t.tokenize(text, escape=False)


def untokenize(tokens, lang='fr'):
    '''
    Inputs a list of tokens output string.
    ["J'", 'ai'] >>> "J' ai"
    '''
    d = MosesDetokenizer(lang=lang)
    text = d.detokenize(tokens, unescape=False)
    return text    


def _tokensToString(tokens_or_str):
    if type(tokens_or_str) is str:
        return tokens_or_str
    elif type(tokens_or_str) is list:
        return untokenize(tokens_or_str)
    elif type(tokens_or_str) is None:
        return ''
    else:
        raise ValueError('Please input string or tokens')


def _stringToTokens(tokens_or_str, lang_module='en_spacy'):
    if type(tokens_or_str) is str:
        return tokenize(tokens_or_str, lang_module=lang_module)
    elif type(tokens_or_str) is list:
        return tokens_or_str
    elif type(tokens_or_str) is None:
        return []
    else:
        raise ValueError('Please input string or tokens')