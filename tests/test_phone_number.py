import pytest
import nautilus_nlp.utils.phone_number as phone

def test_extract_phone_number():
    input_str = '(541) 754-3010 is a US. Phone'
    expected = ['(541) 754-3010', '754-3010']
    res = phone.extract_phone_numbers(input_str, countrylist=phone.SUPPORTED_COUNTRY)
    assert res == expected

def test_extract_phone_number_us():
    input_str = '(541) 754-3010 is a US. Phone'
    expected = ['(541) 754-3010']
    res = phone.extract_phone_numbers(input_str, countrylist=['US'])
    assert res == expected    

def test_extract_phone_number_fr():
    input_str = '06.25.09.32.56 is a FR Phone'
    expected = ['06.25.09.32.56']
    res = phone.extract_phone_numbers(input_str)
    assert res == expected

def test_extract_phone_number_international():
    input_str = '+33625093423 is an international Phone number'
    expected = ['+33625093423']
    res = phone.extract_phone_numbers(input_str)
    assert res == expected

def test_phoneParser_us():
    input_str = '(541) 754-3010'
    expected = '541-754-3010'
    p = phone.phoneParser()
    p.parse_number(input_str,region_code='US')
    res = p.format_number('INTERNATIONAL')
    assert res == expected

def test_phoneParser_fr():
    input_str = '0625093267'
    expected = '6 25 09 32 67'
    p = phone.phoneParser()
    p.parse_number(input_str,region_code='FR')
    res = p.format_number('E164')
    assert res == expected    