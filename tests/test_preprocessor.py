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
import pytest
import numpy as np
from nlpretext.basic.preprocess import (
    normalize_whitespace, remove_eol_characters, fix_bad_unicode,
    unpack_english_contractions, replace_urls, replace_emails,
    replace_phone_numbers, replace_numbers, replace_currency_symbols,
    remove_punct, remove_accents, remove_multiple_spaces_and_strip_text,
    filter_non_latin_characters
)
from nlpretext.basic.preprocess import (
    remove_stopwords as remove_stopwords_text
)
from nlpretext.social.preprocess import (
    remove_mentions, extract_mentions, remove_html_tags, remove_emoji,
    convert_emoji_to_text, extract_emojis, extract_hashtags, remove_hashtag
)
from nlpretext.token.preprocess import (
    remove_tokens_with_nonletters,
    remove_special_caracters_from_tokenslist, remove_smallwords
)
from nlpretext.token.preprocess import (
    remove_stopwords as remove_stopwords_token
)
from nlpretext.preprocessor import Preprocessor

import nlpretext._utils.phone_number as phone
from nlpretext._utils.stopwords import get_stopwords


@pytest.mark.parametrize("text, expected_result",
                         [("ACV water + cinnamon + turmeric + cucumber + lemon. 👍🏻",
                           [":thumbs_up_light_skin_tone:"]),
                          ("This is a text without emojis",
                           [])])
def test_extract_emojis(text, expected_result):
    result = extract_emojis(text)
    assert expected_result == result


@pytest.mark.parametrize("text, expected_result",
                         [("I take care of my skin with @hellobody",
                           "I take care of my skin with"),
                          ("This is a text without mentions",
                           "This is a text without mentions")])
def test_remove_mentions(text, expected_result):
    result = remove_mentions(text)
    assert expected_result == result


@pytest.mark.parametrize("text, expected_result",
                         [("I take care of my skin with @hellobody",
                           ["@hellobody"]),
                          ("This is a text without mentions",
                           [])])
def test_extract_mentions(text, expected_result):
    result = extract_mentions(text)
    assert expected_result == result


@pytest.mark.parametrize("text, expected_result",
                         [("This is a text with <html> content of html tag </html>",
                           "This is a text with content of html tag"),
                          ("This is a text without html tags",
                           "This is a text without html tags")])
def test_remove_html_tags(text, expected_result):
    result = remove_html_tags(text)
    assert expected_result == result


@pytest.mark.parametrize("tokens_list, smallwords_threshold, expected_result",
                         [(["I", "take", "care", "of", "my", "skin"],
                           2,
                           ["take", "care", "skin"]),
                          (["This", "text", "contains", "only", "long", "words"],
                           2,
                           ["This", "text", "contains", "only", "long", "words"])])
def test_remove_smallwords(tokens_list, smallwords_threshold, expected_result):
    result = remove_smallwords(tokens_list, smallwords_threshold)
    assert expected_result == result


@pytest.mark.parametrize("text, expected_result",
                         [("this is a #hashtag in the middle of the text",
                           ["#hashtag"]),
                          ("#this is a hashtag in the beginning of the text",
                           ["#this"]),
                          ("this is a hashtag in the end of the #text",
                           ["#text"]),
                          ("this is a text with no hashtag",
                           []),
                          ("this is a text with #many #hashtags",
                           ["#many", "#hashtags"])]
                         )
def test_extract_hashtags(text, expected_result):
    result = extract_hashtags(text)
    assert expected_result == result


@pytest.mark.parametrize("text, expected_result",
                         [("this is a #hashtag in the middle of the text",
                           "this is a in the middle of the text"),
                          ("#this is a hashtag in the beginning of the text",
                           "is a hashtag in the beginning of the text"),
                          ("this is a hashtag in the end of the #text",
                           "this is a hashtag in the end of the"),
                          ("this is a text with no hashtag",
                           "this is a text with no hashtag"),
                          ("this is a text with #many #hashtags",
                           "this is a text with")]
                         )
def test_remove_hashtag(text, expected_result):
    result = remove_hashtag(text)
    assert expected_result == result


@pytest.mark.parametrize("text, expected_filtered_text",
                         [("كلمات Learn 3 Arabic كلمات words EASILY- Vocabulary #1 تعلم ٣ جديدة",
                           "Learn 3 Arabic words EASILY Vocabulary 1")])
def test_filter_non_latin_characters(text, expected_filtered_text):
    result = filter_non_latin_characters(text)
    assert expected_filtered_text == result


@pytest.mark.parametrize(
    "input_str, expected_str",
    [
        ("hello   world", "hello world"),
        ("\n   hello world    ", "hello world"),
        ("----- hello\tworld *****", "hello world"),
        ("hello-world", "hello-world"),
        ("hello - world", "hello world"),
    ],
)
def test_remove_multiple_spaces_and_strip_text(input_str, expected_str):
    result = remove_multiple_spaces_and_strip_text(input_str)
    np.testing.assert_string_equal(result, expected_str)


@pytest.mark.parametrize(
    "input_str, expected_str",
    [
        ("\nhello world", " hello world"),
        ("hello\nworld", "hello world"),
        ("hello world\n", "hello world ")
    ],
)
def test_remove_eol_characters(input_str, expected_str):
    result = remove_eol_characters(input_str)
    np.testing.assert_string_equal(result, expected_str)


def test_remove_tokens_with_nonletters():
    input_tokens = ['foo', 'bar', '124', '34euros']
    expected_output = ['foo', 'bar']
    result = remove_tokens_with_nonletters(input_tokens)
    np.testing.assert_array_equal(result, expected_output)


def test_remove_special_caracters_from_tokenslist():
    input_tokens = ['foo', 'bar', '---', "'s", '#']
    expected_output = ['foo', 'bar', "'s"]
    result = remove_special_caracters_from_tokenslist(input_tokens)
    np.testing.assert_array_equal(result, expected_output)


def test_get_stopwords():
    languages_to_test = ['fr', 'en', 'ga', 'zh']
    for lang in languages_to_test:
        result = get_stopwords(lang)
        assert len(result) > 0 and isinstance(result, list)


@pytest.mark.parametrize(
    "input_tokens, lang, expected_output",
    [
        (['I', 'like', 'this', 'song', 'very', 'much', '!'], "en", ['I', 'song', '!'])
    ],
)
def test_remove_stopwords_tokens(input_tokens, lang, expected_output):
    result = remove_stopwords_token(input_tokens, lang)
    np.testing.assert_array_equal(result, expected_output)


@pytest.mark.parametrize(
    "input_text, lang, expected_output",
    [
        ('I like this song very much !', 'en', 'I song !'),
        ('Can I get a beer?', 'en', 'Can I beer ?'),
        ('Je vous recommande ce film !', 'fr', 'Je recommande film !'),
        ('je vous recommande ce film !', 'fr', 'recommande film !'),
        ('Quiero una cerveza, por favor.', 'es', 'Quiero cerveza, favor.')
    ],
)
def test_remove_stopwords_text(input_text, lang, expected_output):
    result = remove_stopwords_text(input_text, lang)
    np.testing.assert_array_equal(result, expected_output)


@pytest.mark.parametrize(
    "input_text, lang, custom_stopwords, expected_output",
    [
        ('I like this song very much !', 'en', ['song'], 'I !'),
        ('Je vous recommande ce film la scène de fin est géniale !', 'fr',
         ['film', 'scène'], 'Je recommande fin géniale !'),
    ],
)
def test_remove_custom_stopwords_text(
        input_text, lang, custom_stopwords, expected_output):
    result = remove_stopwords_text(input_text, lang, custom_stopwords)
    np.testing.assert_array_equal(result, expected_output)


def test_remove_accents():
    input_str = "éèëêàù"
    expected_str = "eeeeau"
    result = remove_accents(input_str)
    np.testing.assert_string_equal(result, expected_str)


@pytest.mark.parametrize(
    "input_str, expected_str",
    [('Les augmentations de rÃ©munÃ©rations', 'Les augmentations de rémunérations'),
     ("rÃ©nover l'enquÃªte publique pour en faire un vrai outil  d'amÃ©nagement du territoire et de dialogue social",
      "rénover l'enquête publique pour en faire un vrai outil  d'aménagement du territoire et de dialogue social"),
     ('Limitations de vitesse et sÃ©curitÃ© routiÃ¨re', 'Limitations de vitesse et sécurité routière'),
     ('Pour un nouveau contrat citoyen', 'Pour un nouveau contrat citoyen'),
     (
         'DÃ©velopper les dÃ©marches de budget participatif dans les collectivitÃ©s et associer les citoyens'\
             ' dans la rÃ©alisation des projets',
         'Développer les démarches de budget participatif dans les collectivités et associer les citoyens'\
             ' dans la réalisation des projets'),
     ('proportienelle', 'proportienelle'),
     ('Pour plus de dÃ©mocratie participative', 'Pour plus de démocratie participative'),
     ('Transparence de la vie public', 'Transparence de la vie public'),
     ('EgalitÃ© devant les infractions routiÃ¨res', 'Egalité devant les infractions routières')],)
def test_fix_bad_unicode(input_str, expected_str):
    result = fix_bad_unicode(input_str)
    np.testing.assert_string_equal(result, expected_str)


@pytest.mark.parametrize(
    "input_str, expected_str",
    [
        ('  foo  ', 'foo'),
        ('  foo   bar  ', 'foo bar')
    ],
)
def test_normalize_whitespace(input_str, expected_str):
    result = normalize_whitespace(input_str)
    np.testing.assert_equal(result, expected_str)


@pytest.mark.parametrize(
    "input_str, expected_str",
    [
        ("I can't tell how we've done.", 'I can not tell how we have done.'),
        ("You're fired. She's nice.", "You are fired. She's nice."),
        ("Let's go!", 'Let us go!'),
        ("You've been missing", 'You have been missing'),
        ("I'm sure you're leaving", 'I am sure you are leaving'),
        ("We'll survive.", "We will survive.")
    ]
)
def test_unpack_english_contractions(input_str, expected_str):
    result = unpack_english_contractions(input_str)
    np.testing.assert_equal(result, expected_str)


@pytest.mark.parametrize(
    "input_str, expected_str",
    [(
        "Wan't to contribute to NLPretext? read https://github.com/artefactory/NLPretext/blob/master/CONTRIBUTING.md"\
            " first",
        "Wan't to contribute to NLPretext? read *URL* first"),
     ("If you go to http://internet.org, you will find a website hosted by FB.",
      "If you go to *URL*, you will find a website hosted by FB."),
     ("Ishttps://internet.org/ available?", 'Is*URL* available?'),
     ("mailto:john.doe@artefact.com", '*URL*')])
def test_replace_urls(input_str, expected_str):
    result = replace_urls(input_str)
    np.testing.assert_equal(result, expected_str)


@pytest.mark.parametrize(
    "input_str, expected_str",
    [
        ("my email:john.doe@artefact.com", "my email:*EMAIL*"),
        ("v543143@nwytg.net is a temporary email", "*EMAIL* is a temporary email"),
        ("our emails used to be name.surname@artefact.is", "our emails used to be *EMAIL*")
    ]
)
def test_replace_emails(input_str, expected_str):
    result = replace_emails(input_str)
    np.testing.assert_equal(result, expected_str)


@pytest.mark.parametrize(
    "input_str, expected_str",
    [
        ("mon 06: 0601020304", "mon 06: *PHONE*"),
        ("mon 06: 06.01.02.03.04", "mon 06: *PHONE*"),
        ("call me at +33601020304", "call me at *PHONE*"),
        ("call me at +33 6 01 02 03 04", "call me at *PHONE*"),
        ("call me at +33 601 020 304", "call me at *PHONE*"),
        ("if this unit test doesn't work, call 3615 and says 'HELP'",
         "if this unit test doesn't work, call *PHONE* and says 'HELP'"),
        ('(541) 754-0000 is a US. Phone', '*PHONE* is a US. Phone'),
        ('+1-541-754-0000 is an international Phone', '*PHONE* is an international Phone'),
        ('+1-541-754-0000 Dialed in the US', '*PHONE* Dialed in the US'),
        ('+1-541-754-0000 Dialed from Germany', '*PHONE* Dialed from Germany')
    ]
)
def test_replace_phone_numbers(input_str, expected_str):
    result = replace_phone_numbers(
        input_str,
        replace_with="*PHONE*",
        method="detection",
        country_to_detect=phone.SUPPORTED_COUNTRY)
    np.testing.assert_equal(result, expected_str)


@pytest.mark.parametrize(
    "input_str, expected_str",
    [
        ("123, 3 petits chats", "*NUMBER*, *NUMBER* petits chats"),
        ("Give me 45bucks!", "Give me *NUMBER*bucks!"),
        ("call me at +33601020304", "call me at *NUMBER*")
    ]
)
def test_replace_numbers(input_str, expected_str):
    result = replace_numbers(input_str)
    np.testing.assert_equal(result, expected_str)


@pytest.mark.parametrize(
    "input_str, param, expected_str",
    [
        ("Give me 23$", None, "Give me 23USD"),
        ("Give me 23£", None, "Give me 23GBP"),
        ("Give me 23 £", None, "Give me 23 GBP"),
        ("Give me 23 €", None, "Give me 23 EUR"),
        ("¥ is both japanese yen and Chinese Renminbi", "*CUR*", "*CUR* is both japanese yen and Chinese Renminbi")
    ]
)
def test_replace_currency_symbols(input_str, param, expected_str):
    result = replace_currency_symbols(input_str, replace_with=param)
    np.testing.assert_equal(result, expected_str)


@pytest.mark.parametrize(
    "input_str, param, expected_str",
    [
        ("Seriously...", None, "Seriously   "),
        ("Seriously?", None, "Seriously "),
        ("Seriously ?", None, "Seriously  "),
        ("Seriously???", None, "Seriously   "),
        ("Seriously?!", None, "Seriously  "),
        ('"Seriously"', None, " Seriously "),
        ('Seriously:', None, "Seriously "),
        ('Seriously;', None, "Seriously "),
        ("'Seriously'", None, " Seriously "),
        ("'Seriously'", '.,;', "'Seriously'"),
        ("Seriously.,.", '.,;', "Seriously "),
        ("Seriously...", '.,;', "Seriously "),
        ("Seriously.!.", '.,;', "Seriously ! "),
        ("john.doe@artefact.com", '.,;', "john doe@artefact com"),
        ("john.doe@artefact.com", None, "john doe artefact com"),
        ("john-doe@artefact.com", None, "john doe artefact com")
    ]
)
def test_remove_punct(input_str, param, expected_str):
    result = remove_punct(input_str, marks=param)
    np.testing.assert_equal(result, expected_str)


@pytest.mark.parametrize(
    "input_str, expected_str",
    [
        ("⚽👌", ""),
        ("🎅🏿⌚", ""),
        ("🥖🍷🇫🇷", ""),
        ("✊", ""),
        ("Save 🐼 and 🐟",
         "Save  and "),
    ]
)
def test_remove_emoji(input_str, expected_str):
    result = remove_emoji(input_str)
    assert len(result) == len(expected_str)
    assert result == expected_str


@pytest.mark.parametrize(
    "input_str, expected_str",
    [
        ("⚽️👌", ":soccer_ball::OK_hand:"),
        ("🎅🏿⌚", ":Santa_Claus_dark_skin_tone::watch:"),
        ("🥖🍷🇫🇷", ":baguette_bread::wine_glass::France:"),
        ("✊", ":raised_fist:")
    ]
)
def test_convert_emoji_to_text(input_str, expected_str):
    result = convert_emoji_to_text(input_str)
    np.testing.assert_equal(result, expected_str)


def test_custom_preprocess():
    # Given
    text = "Some text with @mentions and #hashtags"

    preprocessor = Preprocessor()
    preprocessor.pipe(remove_hashtag)
    preprocessor.pipe(remove_mentions)
    expected_result = remove_hashtag(text)
    expected_result = remove_mentions(expected_result)

    # When
    result = preprocessor.run(text)

    # Then
    assert expected_result == result

def test_apply_preprocessor():
    # Given
    text = "Some text with @mentions and whitespaces    and #hashtags"
    operations = (remove_html_tags, remove_mentions, remove_emoji, remove_hashtag,
                  remove_eol_characters, fix_bad_unicode, normalize_whitespace)

    preprocessor = Preprocessor()

    expected_result = text
    for function in operations:
        expected_result = function(expected_result)

    # When
    result = preprocessor.run(text)

    # Then
    assert expected_result == result
