from nautilus_nlp.models.Fasttext_classifier import Fasttext_clf as langdetect
import cld2
import pkg_resources
lang_path = pkg_resources.resource_filename('nautilus_nlp.data', 'lang_identification.ftz')
class LangDetector():
    """ This class is to instantiante a language detector.

    """
    def __init__(self,typemodel,path=lang_path,):
        self.typemodel=typemodel
        self.path = None if path is None else lang_path 
        self.model=langdetect(self.path) if typemodel=='fasttext' else None
    
    def detect_language(self, text_to_detect=None):
        """
        Detected the language of a text

        Args:
        hint_language: language you expect your text to be

        Returns:
        is_reliable: is the top language is much better than 2nd best language?
        language: 2-letter code for the language of the text
        """
        if self.typemodel!='fasttext':
            _, _, best_guesses = cld2.detect(text_to_detect,
                                                    bestEffort=True)

            if len(best_guesses) == 0 or len(best_guesses[0]) != 4 or best_guesses[0][1] == 'un':
                return 'un',0

            return  best_guesses[0][1],(best_guesses[0][2]/100)
        else:
            best_guesses=self.model.predict(text_to_detect)
            return best_guesses[0][0].replace('__label__',''),best_guesses[1][0]


