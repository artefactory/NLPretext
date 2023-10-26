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
# mypy: disable-error-code="assignment"

from typing import Any, List, Optional, Union

import os
import re

import nltk
import spacy
from sacremoses import MosesDetokenizer, MosesTokenizer

MODEL_REGEX = re.compile(r"^[a-z]{2}_(?:core|dep|ent|sent)_(?:web|news|wiki|ud)_(?:sm|md|lg|trf)$")
SUPPORTED_LANG_MODULES = {"en_spacy", "en_nltk", "fr_spacy", "fr_moses", "ko_spacy", "ja_spacy"}


class LanguageNotHandled(Exception):
    pass


class LanguageNotInstalledError(Exception):
    pass


class SpacyModel:
    class SingletonSpacyModel:
        def __init__(self, lang: str) -> None:
            self.lang = lang
            if lang == "en":
                self.model = _load_spacy_model("en_core_web_sm")
            elif lang == "fr":
                self.model = _load_spacy_model("fr_core_news_sm")
            elif lang == "ko":
                self.model = spacy.blank("ko")
            elif lang == "ja":
                self.model = spacy.blank("ja")
            else:
                raise (LanguageNotHandled("This spacy model is not available"))

    model: Optional[spacy.language.Language] = None

    def __init__(self, lang):
        if not SpacyModel.model:
            SpacyModel.model = SpacyModel.SingletonSpacyModel(lang).model

    def get_lang_model(self) -> Optional[str]:
        if self.model:
            lang: str = self.model.lang
            return lang
        return None


def _load_spacy_model(model: str) -> Any:
    try:
        return spacy.load(model)
    except OSError:
        if MODEL_REGEX.match(model):
            os.system(f"python -m spacy download {model}")  # nosec
            return spacy.load(model)
        else:
            raise LanguageNotInstalledError(
                f"Model {model} is not installed. "
                f"To install, run: python -m spacy download {model}"
            )


def _get_spacy_tokenizer(lang: str) -> Optional[spacy.tokenizer.Tokenizer]:
    """
    Function that gets the right tokenizer given the language

    Parameters
    ----------
    lang : str
        Language in which text is written. Languages handled : ["en", "fr", "ko", "ja"]

    Returns
    -------
    spacy.tokenizer.Tokenizer
        spacy tokenizer
    """
    model = SpacyModel(lang).model
    if model:
        return model.tokenizer
    return None


def tokenize(text: str, lang_module: str = "en_spacy") -> List[str]:
    """
    Convert text to a list of tokens.

    Parameters
    ----------
    lang_module : str {'en_spacy', 'en_nltk', 'fr_spacy', 'fr_moses', 'ko_spacy', 'ja_spacy'}
        choose the tokenization module according to the langage and the implementation.
        Recommanded: Spacy (faster, better results). To process other langages
        import models.Spacy_models

    Returns
    -------
    list
        list of string

    Raises
    ------
    ValueError
        If lang_module is not a valid module name
    """
    if lang_module not in SUPPORTED_LANG_MODULES:
        raise ValueError(
            f"Invalid lang_module: {lang_module}. "
            f"lang_module must be one of {SUPPORTED_LANG_MODULES}."
        )

    tokenized_words: List[str] = []
    if "spacy" in lang_module:
        lang = lang_module.split("_")[0]
        spacymodel = _get_spacy_tokenizer(lang)
        if spacymodel:
            spacydoc = spacymodel(text)
            tokenized_words = [spacy_token.text for spacy_token in spacydoc]
    if lang_module == "en_nltk":
        tokenized_words = nltk.word_tokenize(text)
    if lang_module == "fr_moses":
        tokenized_words = MosesTokenizer(lang="fr").tokenize(text, escape=False)

    return tokenized_words


def untokenize(tokens: List[str], lang: str = "fr") -> str:
    """
    Inputs a list of tokens output string.
    ["J'", 'ai'] >>> "J' ai"

    Parameters
    ----------
    lang : string
        language code

    Returns
    -------
    string
        text
    """
    d = MosesDetokenizer(lang=lang)
    text: str = d.detokenize(tokens, unescape=False)
    return text


def convert_tokens_to_string(tokens_or_str: Optional[Union[str, List[str]]]) -> str:
    if isinstance(tokens_or_str, str):
        return tokens_or_str
    if isinstance(tokens_or_str, list):
        return untokenize(tokens_or_str)
    if tokens_or_str is None:
        return ""
    raise TypeError("Please input string or tokens")


def convert_string_to_tokens(
    tokens_or_str: Optional[Union[str, List[str]]], lang_module: str = "en_spacy"
) -> List[str]:
    if isinstance(tokens_or_str, str):
        return tokenize(tokens_or_str, lang_module=lang_module)
    if isinstance(tokens_or_str, list):
        return tokens_or_str
    if tokens_or_str is None:
        return []
    raise TypeError("Please input string or tokens")
