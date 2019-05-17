from nautilus_nlp.utils.tokenizer import _convert_tokens_to_string, _convert_string_to_tokens

import textblob
from textblob import Blobber
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def compute_sentiment_score(tokens_or_txt, lang_module='en_textblob'):
    '''

    '''
    text = _convert_tokens_to_string(tokens_or_txt)
    output = ''
    if lang_module is 'fr_textblob':
        tb = Blobber(pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
        blob = tb(text)
        output = blob.sentiment[0]

    elif lang_module is 'en_textblob':
        blob = TextBlob(text)
        output = blob.sentiment.polarity

    elif lang_module is 'en_vader':
        analyser = SentimentIntensityAnalyzer()
        snt = analyser.polarity_scores(text)
        output = snt['compound']
    else:
        raise ValueError('Please enter a valid module name!')

    assert output != ''
    return output