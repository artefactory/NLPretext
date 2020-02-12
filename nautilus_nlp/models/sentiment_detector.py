# GNU Lesser General Public License v3.0 only
# Copyright (C) 2020 Artefact
# licence-information@artefact.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
from nautilus_nlp.utils.tokenizer import _convert_tokens_to_string, _convert_string_to_tokens

import textblob
from textblob import Blobber
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def compute_sentiment_score(tokens_or_txt, lang_module:str='en_textblob')->float:
    """
    Compute a sentiment score using pre-trained lexicons: TextBlob or Vader.
    Output a score from -1 to 1, depending if the text is negative neutral
    of positive.

    Parameters
    ----------
    tokens_or_txt
        the text to be processed

    lang_module
        ('fr_textblob','en_textblob','en_vader')

    Returns
    -------
    float 
        Polarity score from -1 to 1
    """
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