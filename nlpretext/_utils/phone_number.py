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
from typing import List, Optional

import phonenumbers as _phonenumbers
from nlpretext._config.config import FORMAT_NUMBERS, SUPPORTED_COUNTRY


def find_phone_numbers(string: str, region_code: Optional[str] = None) -> List[str]:
    """
    Python port of Google's libphonenumber.
    https://github.com/daviddrysdale/python-phonenumbers

    Parameters
    ----------
    region_code : str, optional
        If specified, will find the number of the specified country.
    eg. 06.00.00.00.00 if "FR" is specified.

    If not specified, only works for international-formatted phone numbers.
    - ie. phone number with +country code specified
    eg. 06.00.00.00.00 will return an error but +33 6 00 00 00 00 will work.
    supported value: look SUPPORTED_COUNTRY variable.

    Returns
    -------
    list
        list of matched phone numbers.

    Raises
    ------
    ValueError
        if country code is not supported.
    """
    if region_code not in SUPPORTED_COUNTRY:
        raise ValueError("Please enter a valid contry code. See SUPPORTED_COUNTRY list.")
    return [match.raw_string for match in _phonenumbers.PhoneNumberMatcher(string, region_code)]


def extract_phone_numbers(text: str, countrylist: List[Optional[str]]) -> List[str]:
    """
    Find phone numbers in a text, returns a list of phone numbers.

    Parameters
    ----------
    text : str
    countrylist : list (eg. [None,'FR','US','GB'])
        Look for phone numbers formatted according to the specified countlist.
        supported value: look SUPPORTED_COUNTRY variable.

    Returns
    -------
    list
        List of unique phone numbers found.
    """
    all_phone_numbers: List[str] = []
    for country in countrylist:
        new_numbers_founds = find_phone_numbers(text, region_code=country)
        all_phone_numbers.extend(new_numbers_founds)
    return list(set(all_phone_numbers))


class PhoneParser:
    """
    Python port of Google's libphonenumber.
    https://github.com/daviddrysdale/python-phonenumbers
    """

    def __init__(self):
        self.region_code = None
        self.text = None
        self.parsed_num: Optional[_phonenumbers.PhoneNumber] = None

    @property
    def parsed_num(self) -> Optional[_phonenumbers.PhoneNumber]:
        return self.__parsed_num

    @parsed_num.setter
    def parsed_num(self, value: Optional[_phonenumbers.PhoneNumber]) -> None:
        self.__parsed_num = value

    def parse_number(
        self, text: str, region_code: Optional[str] = None
    ) -> Optional[_phonenumbers.PhoneNumber]:
        """
        Extract phone number from text

        Parameters
        ----------
        text: str
        region_code : str, optional
            If specified, will find the number of the specified country.
        eg. 06.00.00.00.00 if "FR" is specified.
        If not specified, only works for international-formatted phone numbers.
        - ie. phone number with +country code specified
        eg. 06.00.00.00.00 will return an error but +33 6 00 00 00 00 will work.
        supported value: look SUPPORTED_COUNTRY variable.

        Returns
        -------
        str
            The parsed number

        Raises
        ------
        NumberParseException
            If the string doesn't contains phone number of is the parser fails.
        """
        self.region_code = region_code
        self.text = text
        self.parsed_num: Optional[_phonenumbers.PhoneNumber] = _phonenumbers.parse(
            self.text, self.region_code
        )
        return self.parsed_num

    def format_number(self, num_format: str) -> str:
        """
        Convert a phone number to another standard format.

        Parameters
        ----------
        num_format : str {'E164','INTERNATIONAL','NATIONAL','RFC3966'}

        Returns
        -------
        str
            Number formatted
        """
        standard_format = FORMAT_NUMBERS.get(num_format)
        if standard_format is None:
            raise ValueError(f"Please choose a num_format in {list(FORMAT_NUMBERS.keys())}")
        if self.parsed_num is None:
            raise ValueError(f"Could not parse phone number {self.parsed_num}")
        formatted_number: Optional[str] = _phonenumbers.format_number(
            self.parsed_num, standard_format
        )
        if formatted_number is None:
            raise ValueError(f"Could not format phone number {formatted_number}")
        return formatted_number
