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
from summa.summarizer import summarize


def is_list_of_strings(lst):
    """
    Parameters
    ----------
    lst : list

    Returns
    -------
    book
        boolean indicator
    """
    return bool(lst) and isinstance(lst, list) and all(isinstance(elem, str) for elem in lst)


def summarize_text(txt, ratio=0.2, language="english", words=None):
    """
    Parameters
    ----------
    txt : str
        Sting or list of strings containing text to summarize
    ratio : float
        Percentage giving the output text length in reference to the input length.
    language :
        text language. eg. "english"
    words :
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
    return summarize(txt, ratio, words, language)
