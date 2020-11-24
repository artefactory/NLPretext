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

from flashtext import KeywordProcessor


def extract_keywords(text, keyword, case_sensitive=True):
    """
    Extract Keywords from a document.

    Parameters
    ----------
    text : str
        Text to extract keywords from
    keyword :
        Single keyword (str) or list of keywords (list)
    case_sensitive :
        If False, will be case insensitive.

    Returns
    -------
    list
        Return list of extracted keyworkds
    """

    processor = KeywordProcessor(case_sensitive=case_sensitive)
    if isinstance(keyword, list):
        processor.add_keywords_from_list(keyword)
    elif isinstance(keyword, str):
        processor.add_keyword(keyword)
    elif isinstance(keyword, dict):
        processor.add_keywords_from_dict(keyword)

    return processor.extract_keywords(text)
    