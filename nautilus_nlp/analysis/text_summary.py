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
from typing import Optional, Any
from summa.summarizer import summarize


def is_list_of_strings(lst: Any) -> bool:
    """
    Parameters
    ----------
    lst : list

    Returns
    -------
    book : bool
        True if is a list of strings, else returns False
    """
    return bool(lst) and isinstance(lst, list) and all(isinstance(elem, str) for elem in lst)


def summarize_text(
    txt: str, ratio: float = 0.2, language: str = "english", nb_words: Optional[int] = None) -> str:
    """
    This function uses the summa library to summazize text

    Parameters
    ----------
    txt : str
        Sting or list of strings containing text to summarize
    ratio : float
        Percentage giving the output text length in reference to the input length.
    language : str
        text language. eg. "english"
    nb_words : int 
        number of words of the output text or None

    Returns
    -------
    string
        string containing the summarized text
    """
    if is_list_of_strings(txt):
        txt = ' '.join(txt)
    elif not isinstance(txt, str):
        raise TypeError("Text parameter must be a Unicode object (str) or list of str!")
    return summarize(txt, ratio, nb_words, language)
