from nautilus_nlp.models.fasttext_classifier import Fasttext_clf as langdetect
from nautilus_nlp.preprocessing.preprocess import remove_EOL_characters
import pkg_resources

lang_path = pkg_resources.resource_filename(
    "nautilus_nlp.data", "lang_identification.ftz"
)


class LangDetector:
    """ 
    This class is to instantiante a language detector.
    """

    def __init__(self, path=None):
        self.path = path if path is not None else lang_path
        self.model = langdetect(self.path)

    def detect_language(self, text_to_detect=None):
        """
        Detected the language of a text

        Parameters
        ----------
        hint_language : string
            language you expect your text to be

        Returns
        -------
        is_reliable : 
            is the top language is much better than 2nd best language?
        language: 
            2-letter code for the language of the text
        """
        best_guesses = self.model.predict(remove_EOL_characters(text_to_detect))
        return best_guesses[0][0].replace("__label__", ""), best_guesses[1][0]
