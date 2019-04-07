import functools
import pkg_resources
import nautilus_nlp
import spacy
import textacy
from collections import Counter
import re
import unicodedata
import spacy
import spacy.matcher
import textacy
import textacy.keyterms
import textacy.text_utils

class NautilusMissingModelException(Exception):
    """Raised when the requested model is missing"""

    pass


class Doc:
    """
    Create a doc instance of text, obtain cleaned, readable text and
    metadata from this doc.

    Properties:
    raw: incoming, unedited text
    language: 2-letter code for the language of the text
    is_detected_language: is the language detected or specified beforehand
    is_reliable_language: is the language specified or was it reliably detected
    _spacy_nlps: nested dictionary {lang: {model_id: model}} with loaded spacy language modules
    """

    def __init__(
        self,
        raw,
        language=None,
        spacy_nlps=None,
        langdetect=None,
        sentiment_detect=None,
    ):
        self.raw = raw
        self._spacy_nlps = spacy_nlps or dict()
        self._language = language
        self._is_reliable_language = 1 if language else None
        self._language_detector = langdetect
        self._sentiment_detector = sentiment_detect
        self._text_stats = {}

    @property
    def language(self):
        """
        Provided or detected language of a text
        
        >>> from nautilus_nlp.doc import Doc
        >>> Doc('Test sentence for testing text').language
        'en'
        >>> Doc('Test sentence for testing text', language='en').language
        'en'
        >>> Doc('Test', hint_language='nl').language
        'nl'
        """

        if not self._language:
            if self._language_detector:
                self._language,self._is_reliable_language = self._language_detector.detect_language(
                    self.clean
                )
            else:
                raise NautilusMissingModelException(
                    "You must either provide a language for the document or an instance of LangDetector"
                )

        return self._language

    @property
    def _spacy_doc(self):
        """
        Loads the default spacy doc or creates one if necessary

        >>> doc = Doc('Test sentence for testing text')
        >>> type(doc._spacy_doc)
        <class 'spacy.tokens.doc.Doc'>
        """
        lang = self.language

        return self._load_spacy_doc(lang)

    def _load_spacy_doc(self, lang, model_name=None):
        """
        Loads a spacy doc or creates one if necessary
        """
        # Load default spacy model if necessary, if not loaded already
        if lang not in self._spacy_nlps or (
            model_name is None and model_name not in self._spacy_nlps[lang]
        ):
            if lang not in self._spacy_nlps:
                self._spacy_nlps[lang] = {}
            self._spacy_nlps[lang][None] = self._get_default_nlp(lang)
        if model_name not in self._spacy_nlps[lang] and model_name is not None:
            raise NautilusMissingModelException(
                f"Custom model {model_name} " f"is missing."
            )
        nlp = self._spacy_nlps[lang][model_name]
        doc = nlp(self.clean_text())
        return doc

    @staticmethod
    @functools.lru_cache()
    def _get_default_nlp(lang):
        """
        Loads the spacy default language module for the Doc's language
        """
        try:
            if lang!='un':
                return spacy.load(
                    "{}_core_{}_sm".format(lang, "web" if lang == "en" else "news")
                )
            else:
                return spacy.load('xx_ent_wiki_sm')
        except IOError:
            raise NautilusMissingModelException(
                f'Default model for language "{lang}" is not available. You should try to run python -m spacy download {lang}_core_news_sm'
            
            )

    @property
    def clean(self):
        """
        Cleaned text with sensible defaults.
        >>> doc = Doc('“Please clean this piece… of text</b>„')
        >>> doc.clean
        '"Please clean this piece... of text"'
        
        Right now this is done here by a simple regex. Next step is to use the preprocessing functions
        """

        return self.clean_text()

    @functools.lru_cache()
    def clean_text(self, clean_dots=True, clean_quotes=True, clean_whitespace=True):
        """
        Clean text and normalise punctuation.
        >>> doc = Doc('“Please clean this piece… of text„')
        >>> doc.clean_text(False, False, False, False) == doc.raw
        True
        """
        text = self.raw
        text.replace('\n',' ')
        if clean_dots:
            text = re.sub(r"…", "...", text)
        if clean_quotes:
            text = re.sub(r"[`‘’‛⸂⸃⸌⸍⸜⸝]", "'", text)
            text = re.sub(r"[„“]|(\'\')|(,,)", '"', text)
        if clean_whitespace:
            text = re.sub(r"\s+", " ", text).strip()

        return text

    @property
    def lemma(self):

        return self.get_lemma()
    
    @functools.lru_cache()
    def get_lemma(self,model_name=None):
        
        return [token.lemma_ for token in  self._load_spacy_doc(self.language, model_name)]

    @property
    def entities(self):
        """
        A list of the named entities with sensible defaults.

        >>> doc = Doc('Sentence for testing Google text')
        >>> doc.entities
        [('Google', 'ORG')]
        """
        return self.find_entities()

    @functools.lru_cache()
    def find_entities(self, model_name=None):
        """
        Extract a list of the named entities in text, with the possibility of using a custom model.

        >>> doc = Doc('Sentence for testing Google text')
        >>> doc.find_entities()
        [('Google', 'ORG')]
        """

        return list(
            {
                (ent.text, ent.label_)
                for ent in self._load_spacy_doc(self.language, model_name).ents
            }
        )

    @property
    def n_sentences(self):
        """
        Extract the number of sentences from text

        >>> doc = Doc('Test sentence for testing text. And another sentence for testing!')
        >>> doc.n_sentences
        2
        """
        return len(list(self._spacy_doc.sents))

    @property
    def sentences(self):
        """
        Extract the text and character offset (begin) of sentences from text

        >>> doc = Doc('Test sentence for testing text. And another one with, some, punctuation! And stuff.')
        >>> doc.sentences
        [('Test sentence for testing text.', 0), ('And another one with, some, punctuation!', 32), ('And stuff.', 73)]
        """

        return [(span.text, span.start_char) for span in self._spacy_doc.sents]

    @property
    def n_words(self):
        """
        Extract the number of words from text

        >>> doc = Doc('Test sentence for testing text')
        >>> doc.n_words
        5
        """
        return len(self.words)

    @property
    def words(self):
        """
        Extract the text and character offset (begin) of words from text

        >>> doc = Doc('Test sentence for testing text.')
        >>> doc.words
        [('Test', 0), ('sentence', 5), ('for', 14), ('testing', 18), ('text', 26), ('.', 30)]
        """

        return [(token.text, token.idx) for token in self._spacy_doc]

    @property
    def word_counts(self):
        """
        Extract words with their counts

        >>> doc = Doc('Test sentence for testing vectorisation of a sentence.')
        >>> doc.word_counts
        {'Test': 1, 'sentence': 2, 'for': 1, 'testing': 1, 'vectorisation': 1, 'of': 1, 'a': 1, '.': 1}
        """

        return dict(Counter(word for word, _ in self.words))

    @property
    def complexity(self):
        """
        Determine the complexity of text using the Flesch
        reading ease test ranging from 0.0 - 100.0 with 0.0
        being the most difficult to read.

        >>> doc = Doc('Test sentence for testing text')
        >>> doc.complexity
        83.32000000000004
        """
        if not self._text_stats:
            self._text_stats = textacy.TextStats(self._spacy_doc)
        if self._text_stats.n_syllables == 0:
            return 100
        return self._text_stats.flesch_reading_ease

    @property
    def sentiment(self):
        """
        Returns polarity score (-1 to 1) and a subjectivity score (0 to 1)

        >>> doc = Doc('C'est trop cool !.')
        >>> doc.sentiment
        (0.8, 0.9666666666666667)
        """

        raise NautilusMissingModelException(f"No sentiment model for {self.language}")

    @functools.lru_cache()
    def extract_keyterms(self, ranker="textrank", n_terms=10, **kwargs):
        """
        Extract and rank key terms in the document by proxying to
        `textacy.keyterms`. Returns a list of (term, score) tuples. Depending
        on the ranking algorithm used, terms can consist of multiple words.

        Available rankers are TextRank (textrank), SingleRank (singlerank) and
        SGRank ('sgrank').

        >>> doc = Doc('Amsterdam is the awesome capital of the Netherlands.')
        >>> doc.extract_keyterms(n_terms=3)
        [('awesome', 0.32456160227748454), ('capital', 0.32456160227748454), ('Amsterdam', 0.17543839772251532)]
        >>> doc.extract_keyterms(ranker='sgrank')
        [('awesome capital', 0.5638711013322963), ('Netherlands', 0.22636566128805719), ('Amsterdam', 0.20976323737964653)]
        >>> doc.extract_keyterms(ranker='sgrank', ngrams=(1))
        [('Netherlands', 0.4020557546031188), ('capital', 0.29395103364295216), ('awesome', 0.18105611227666252), ('Amsterdam', 0.12293709947726655)]
        """
        if self.n_words < 1:
            return []
        rankers = ["textrank", "sgrank", "singlerank"]
        if ranker not in rankers:
            raise ValueError(
                f'ranker "{ranker}" not available; use one ' f"of {rankers}"
            )
        ranking_fn = getattr(textacy.keyterms, ranker)
        return ranking_fn(self._spacy_doc, n_keyterms=n_terms, **kwargs)

    @property
    def keyterms(self):
        """
        Return textranked keyterms for the document.

        >>> doc = Doc('Amsterdam is the awesome capital of the Netherlands.')
        >>> doc.extract_keyterms(n_terms=3)
        [('awesome', 0.32456160227748454), ('capital', 0.32456160227748454), ('Amsterdam', 0.17543839772251532)]
        """
        return self.extract_keyterms()
   
    @functools.lru_cache()
    def extract_keywords(self,keyword_list:list):
        from flashtext import KeywordProcessor
        return KeywordProcessor().add_keywords_from_list(keyword_list).extract_keywords(self.raw)
