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
from nautilus_nlp.models.fasttext_classifier import Fasttext_clf as langdetect
from nautilus_nlp.preprocessing.text_preprocess import TextPreprocessor
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
        preprocessor = TextPreprocessor(text_to_detect)
        best_guesses = self.model.predict(preprocessor.remove_EOL_characters())
        return best_guesses[0][0].replace("__label__", ""), best_guesses[1][0]
