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
import re
import phonenumbers as _phonenumbers

SUPPORTED_COUNTRY = [None, 'US', 'AG', 'AI', 'AS', 'BB', 'BM', 'BS', 'CA', 'DM', 
                    'GD', 'GU', 'JM', 'KN', 'KY', 'LC', 'MP', 'MS', 'PR', 'SX', 'TC', 'TT', 
                    'VC', 'VG', 'VI', 'RU', 'KZ', 'EG', 'ZA', 'GR', 'NL', 'BE', 'FR', 'ES', 
                    'HU', 'IT', 'VA', 'RO', 'CH', 'AT', 'GB', 'GG', 'IM', 'JE', 'DK', 'SE', 
                    'NO', 'SJ', 'PL', 'DE', 'PE', 'MX', 'CU', 'AR', 'BR', 'CL', 'CO', 'VE', 
                    'MY', 'AU', 'CC', 'CX', 'ID', 'PH', 'NZ', 'SG', 'TH', 'JP', 'KR', 'VN', 
                    'CN', 'TR', 'IN', 'PK', 'AF', 'LK', 'MM', 'IR', 'SS', 'MA', 'EH', 'DZ', 
                    'TN', 'LY', 'GM', 'SN', 'MR', 'ML', 'GN', 'CI', 'BF', 'NE', 'TG', 'BJ', 
                    'MU', 'LR', 'SL', 'GH', 'NG', 'TD', 'CF', 'CM', 'CV', 'ST', 'GQ', 'GA', 
                    'CG', 'CD', 'AO', 'GW', 'IO', 'AC', 'SC', 'SD', 'RW', 'ET', 'SO', 'DJ', 
                    'KE', 'TZ', 'UG', 'BI', 'MZ', 'ZM', 'MG', 'RE', 'YT', 'ZW', 'NA', 'MW', 
                    'LS', 'BW', 'SZ', 'KM', 'SH', 'TA', 'ER', 'AW', 'FO', 'GL', 'GI', 'PT', 
                    'LU', 'IE', 'IS', 'AL', 'MT', 'CY', 'FI', 'AX', 'BG', 'LT', 'LV', 'EE', 
                    'MD', 'AM', 'BY', 'AD', 'MC', 'SM', 'UA', 'RS', 'ME', 'XK', 'HR', 'SI', 
                    'BA', 'MK', 'CZ', 'SK', 'LI', 'FK', 'BZ', 'GT', 'SV', 'HN', 'NI', 'CR', 
                    'PA', 'PM', 'HT', 'GP', 'BL', 'MF', 'BO', 'GY', 'EC', 'GF', 'PY', 'MQ',
                    'SR', 'UY', 'CW', 'BQ', 'TL', 'NF', 'BN', 'NR', 'PG', 'TO', 'SB', 'VU', 
                    'FJ', 'PW', 'WF', 'CK', 'NU', 'WS', 'KI', 'NC', 'TV', 'PF', 'TK', 'FM', 
                    'MH', 'KP', 'HK', 'MO', 'KH', 'LA', 'BD', 'TW', 'MV', 'LB', 'JO', 'SY',
                    'IQ', 'KW', 'SA', 'YE', 'OM', 'PS', 'AE', 'IL', 'BH', 'QA', 'BT', 'MN', 
                    'NP', 'TJ', 'TM', 'AZ', 'GE', 'KG', 'UZ','DO']


def find_phone_numbers(string, region_code=None):
    """
    Python port of Google's libphonenumber.
    https://github.com/daviddrysdale/python-phonenumbers

    Parameters
    ----------
    region_code
        If specified, will find the number of the specified country. 
    eg. 06.25.09.32.67 if "FR" is specified.

    If not specified, only works for international-formatted phone numbers.
    - ie. phone number with +counttry code specified 
    eg. 06.25.09.32.67 will return an error but +33 6 25 09 32 67 will work.        

    region_code
        supported value: look SUPPORTED_COUNTRY variable.

    """
    if region_code not in SUPPORTED_COUNTRY:
        raise ValueError('Please enter a valid contry code. See SUPPORTED_COUNTRY list.')

    return [match.raw_string for match in _phonenumbers.PhoneNumberMatcher(string, region_code)]


def extract_phone_numbers(string:str, countrylist:list=[None,'FR','US','GB'])->list:
    '''
    Find phone numbers in a string, returns a list of phone numbers. 

    Parameters
    ----------
    countrylist: list
        Look for phone numbers formatted according to the specified countlist. 
        supported value: look SUPPORTED_COUNTRY variable.
    '''
    res = []
    for country in countrylist:
        new_numbers_founds = find_phone_numbers(string, region_code=country)
        res += new_numbers_founds
    return list(set(res))


class phoneParser(object):
    """
    Python port of Google's libphonenumber.
    https://github.com/daviddrysdale/python-phonenumbers 
    """

    def __init__(self):
        self.region_code = None
        self.string = None
        self.parsed_num = None

    def parse_number(self, string:str, region_code=None):
        '''
        Parameters
        ----------
        region_code
            If specified, will find the number of the specified country. 
        eg. 06.25.09.32.67 if "FR" is specified.

        If not specified, only works for international-formatted phone numbers.
        - ie. phone number with +counttry code specified 
        eg. 06.25.09.32.67 will return an error but +33 6 25 09 32 67 will work.        

        region_code
            supported value: look SUPPORTED_COUNTRY variable.

        Raises
        ------
        NumberParseException
            If the string doesn't contains phone number of is the parser fails.             
        '''
        self.region_code = region_code
        self.string = string        
        self.parsed_num = _phonenumbers.parse(self.string, self.region_code)
        return self.parsed_num

    def format_number(self, num_format):
        '''
        ['E164','INTERNATIONAL','NATIONAL','RFC3966']
        '''
        standard_format = exec('_phonenumbers.PhoneNumberFormat.'+num_format)
        
        return _phonenumbers.format_number(self.parsed_num, standard_format)