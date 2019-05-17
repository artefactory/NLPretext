import pytest
import numpy as np
from nautilus_nlp.preprocessing.preprocess import (
    remove_multiple_spaces_and_strip_text,
    remove_accents,
    fix_bad_unicode,
    remove_EOL_characters,
    remove_tokens_with_nonletters,
    remove_special_caracters_from_tokenslist,
    get_stopwords,
    remove_stopwords,
    normalize_whitespace,
    unpack_english_contractions,
    replace_urls,
    replace_emails,
    replace_phone_numbers,
    replace_numbers,
    replace_currency_symbols,
    remove_punct,
    remove_emoji
)


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
def test_remove_EOL_characters(input_str, expected_str):
    result = remove_EOL_characters(input_str)
    np.testing.assert_string_equal(result, expected_str)    


def test_remove_tokens_with_nonletters():
    input_tokens = ['foo','bar','124','34euros']
    expected_output = ['foo','bar']
    result = remove_tokens_with_nonletters(input_tokens)
    np.testing.assert_array_equal(result,expected_output)


def test_remove_special_caracters_from_tokenslist():
    input_tokens = ['foo','bar','---',"'s",'#']
    expected_output = ['foo','bar',"'s"]
    result = remove_tokens_with_nonletters(input_tokens)
    np.testing.assert_array_equal(result, expected_output)


def test_get_stopwords():
    languages_to_test = ['fr','en','ga','zh']
    for lang in languages_to_test:
        result = get_stopwords(lang)
        assert len(result) > 0 and type(result) == list


@pytest.mark.parametrize(
    "input_tokens, expected_output",
    [
        (['I','like','when','you','move','your','body','!'], ['I', 'move', 'body', '!']),
        ('I like when you move your body !', ['I', 'move', 'body', '!']),
    ],
)    
def test_remove_stopwords(input_tokens, expected_output):
    stopwords = get_stopwords('en')
    result = remove_stopwords(input_tokens, stopwords)
    np.testing.assert_array_equal(result, expected_output)


def test_remove_accents():
    input_str = "éèëêàù"
    expected_str = "eeeeau"

    result = remove_accents(input_str)
    np.testing.assert_string_equal(result, expected_str)


@pytest.mark.parametrize(
    "input_str, expected_str",
    [
    ('Les augmentations de rÃ©munÃ©rations',
  'Les augmentations de rémunérations'),
 ("rÃ©nover l'enquÃªte publique pour en faire un vrai outil  d'amÃ©nagement du territoire et de dialogue social",
  "rénover l'enquête publique pour en faire un vrai outil  d'aménagement du territoire et de dialogue social"),
 ('Limitations de vitesse et sÃ©curitÃ© routiÃ¨re',
  'Limitations de vitesse et sécurité routière'),
 ('Pour un nouveau contrat citoyen', 'Pour un nouveau contrat citoyen'),
 ('DÃ©velopper les dÃ©marches de budget participatif dans les collectivitÃ©s et associer les citoyens dans la rÃ©alisation des projets',
  'Développer les démarches de budget participatif dans les collectivités et associer les citoyens dans la réalisation des projets'),
 ('proportienelle', 'proportienelle'),
 ('Pour plus de dÃ©mocratie participative',
  'Pour plus de démocratie participative'),
 ('Transparence de la vie public', 'Transparence de la vie public'),
 ('18 mois de trop....ca suffit macron',
  '18 mois de trop....ca suffit macron'),
 ('EgalitÃ© devant les infractions routiÃ¨res',
  'Egalité devant les infractions routières')
    ],
)
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
        ("Let's go!",'Let us go!'),
        ("You've been missing",'You have been missing'),
        ("I'm sure you're leaving",'I am sure you are leaving'),
        ("We'll survive.","We will survive.")
    ]
    )
def test_unpack_english_contractions(input_str, expected_str):
    result = unpack_english_contractions(input_str)
    np.testing.assert_equal(result, expected_str)

@pytest.mark.parametrize(
    "input_str, expected_str",
    [
        ("Wan't to contribute to Nautilus? read https://github.com/artefactory/nautilus-nlp/blob/docs/CONTRIBUTING.md first",
         "Wan't to contribute to Nautilus? read *URL* first"),
        ("The ip address of my VM is http://34.76.182.5:8888", "The ip address of my VM is *URL*"),
        ("If you go to http://internet.org, you will find a website hosted by FB.",
         "If you go to *URL*, you will find a website hosted by FB."),
        ("Ishttps://waaaou.com/ available?",'Is*URL* available?'),
        ("mailto:hugo.vasselin@artefact.com",'*URL*')
    ]
    )
def test_replace_urls(input_str, expected_str):
    result = replace_urls(input_str)
    np.testing.assert_equal(result, expected_str)


@pytest.mark.parametrize(
    "input_str, expected_str",
    [
        ("my email:hugo.vasselin@artefact.com","my email:*EMAIL*"),
        ("v543143@nwytg.net is a temporary email", "*EMAIL* is a temporary email"),
        ("our emails used to be name.surname@artefact.is","our emails used to be *EMAIL*"),
        ("chaudasse_du_13@hotmail.frC ton email bb?",'*EMAIL*C ton email bb?')
    ]
    )
def test_replace_emails(input_str, expected_str):
    result = replace_emails(input_str)
    np.testing.assert_equal(result, expected_str)


@pytest.mark.parametrize(
    "input_str, expected_str",
    [
        ("mon 06 bb: 0625093267","mon 06 bb: *NUMBER*"),
        ("mon 06 bb: 06.25.09.32.67","mon 06 bb: *NUMBER*"),
        ("call me at +33625093267","call me at *NUMBER*"),
        ("call me at +33 6 25 09 32 67","call me at *NUMBER*"),
        ("call me at +33 625 093 267","call me at *NUMBER*"),
        ("if this unit test doesn't work, call 3615 and says 'ROBIN'",
         "if this unit test doesn't work, call *NUMBER* and says 'ROBIN'"),
        ('(541) 754-3010 is a US. Phone','*NUMBER* is a US. Phone'),
        ('+1-541-754-3010 is an international Phone','*NUMBER* is an international Phone'),
        ('+1-541-754-3010 Dialed in the US','*NUMBER* Dialed in the US'),
        ('+1-541-754-3010 Dialed from Germany','*NUMBER* Dialed from Germany'),
        ('191 541 754 3010 Dialed from France','*NUMBER* Dialed from France')
    ]
    )
def test_replace_phone_numbers(input_str, expected_str):
    result = replace_phone_numbers(input_str)
    np.testing.assert_equal(result, expected_str)


@pytest.mark.parametrize(
    "input_str, expected_str",
    [
        ("123, 3 petits chats","*NUMBER*, *NUMBER* petits chats"),
        ("l0ve 2 twa <3","l*NUMBER*ve *NUMBER* twa <*NUMBER*"),
        ("Give me 45bucks!","Give me *NUMBER*bucks!"),
        ("call me at +33625093267","call me at +*NUMBER*")
    ]
    )
def test_replace_numbers(input_str, expected_str):
    result = replace_numbers(input_str)
    np.testing.assert_equal(result, expected_str)


@pytest.mark.parametrize(
    "input_str, param, expected_str",
    [
        ("Give me 23$",None,"Give me 23USD"),
        ("Give me 23£",None,"Give me 23GBP"),
        ("Give me 23 £",None,"Give me 23 GBP"),
        ("Give me 23 €",None,"Give me 23 EUR"),
        ('¥ is both japanese yen and Chinese Renminbi',"*CUR*","*CUR* is both japanese yen and Chinese Renminbi")
    ]
    )
def test_replace_currency_symbols(input_str, param, expected_str):
    result = replace_currency_symbols(input_str, replace_with=param)
    np.testing.assert_equal(result, expected_str)

@pytest.mark.parametrize(
    "input_str, param, expected_str",
    [
        ("Seriously...",None,"Seriously "),
        ("Seriously?",None,"Seriously "),
        ("Seriously ?",None,"Seriously  "),
        ("Seriously???",None,"Seriously   "),
        ("Seriously?!",None,"Seriously  "),
        ('"Seriously"',None," Seriously "),
        ('Seriously:',None,"Seriously "),
        ('Seriously;',None,"Seriously "),
        ("'Seriously'",None," Seriously "),
        ("'Seriously'",'.,;','Seriously'),
        ("Seriously...",'.,;','Seriously   '),
        ("Seriously.,.",'.,;','Seriously   '),
        ("Seriously.!.",'.,;','Seriously ! '),
        ("hugo.vasselin@artefact.com",'.,;','hugo vasselin@artefact com'),
        ("hugo.vasselin@artefact.com",None,'hugo vasselin@artefact com'),
        ("hugo-vasselin@artefact.com",None,'hugo vasselin@artefact com')
    ]
    )
def test_remove_punct(input_str, param, expected_str):
    result = remove_punct(input_str, marks=param)
    np.testing.assert_equal(result, expected_str)


@pytest.mark.parametrize(
    "input_str, expected_str",
    [
        ("👉👌",""),
        ("🎅🏿",""),
        ("🥖✊💦",""),
        ("J'espère que les 🚓 vont pas lire ce test",
        "J'espère que les  vont pas lire ce test")
    ]
    )
def test_remove_emoji(input_str, expected_str):
    result = remove_emoji(input_str)
    np.testing.assert_equal(result, expected_str)    