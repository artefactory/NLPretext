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
import nlpretext._utils.phone_number as phone

def test_extract_phone_number():
    input_str = '(541) 754-3010 is a US. Phone'
    expected = ['(541) 754-3010', '754-3010']
    res = phone.extract_phone_numbers(input_str, countrylist=phone.SUPPORTED_COUNTRY)
    assert sorted(res) == sorted(expected)

def test_extract_phone_number_us():
    input_str = '(541) 754-3010 is a US. Phone'
    expected = ['(541) 754-3010']
    res = phone.extract_phone_numbers(input_str, countrylist=['US'])
    assert res == expected

def test_extract_phone_number_fr():
    input_str = '06.00.00.00.00 is a FR Phone'
    expected = ['06.00.00.00.00']
    res = phone.extract_phone_numbers(input_str, countrylist=['FR'])
    assert res == expected

def test_extract_phone_number_international():
    input_str = '+33600000000 is an international Phone number'
    expected = ['+33600000000']
    res = phone.extract_phone_numbers(input_str, countrylist=['US', 'GB', 'FR', None])
    assert res == expected

def test_phone_parser_us():
    input_str = '(541) 754-3010'
    expected = '+1 541-754-3010'
    p = phone.PhoneParser()
    p.parse_number(input_str, region_code='US')
    res = p.format_number('INTERNATIONAL')
    assert res == expected

def test_phone_parser_fr():
    input_str = '0600000000'
    expected = '+33600000000'
    p = phone.PhoneParser()
    p.parse_number(input_str, region_code='FR')
    res = p.format_number('E164')
    assert res == expected
