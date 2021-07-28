import pytest
import spacy
from nlpretext.token.tokenizer import SpacyModel, LanguageNotInstalledError

@pytest.mark.parametrize(
    "fake_input, expected_model_in_message",
    [
        ("en", "en_core_web_sm"),
        ("fr", "fr_core_news_sm")
    ]
)
def test_get_spacy_tokenizer_when_model_not_downloaded(monkeypatch, fake_input, expected_model_in_message):

    def mock_spacy_load(lang):
        raise OSError(
            "[E050] Can't find model 'en_core_web_sm'. It doesn't seem to be ..."
        )

    monkeypatch.setattr(spacy, "load", mock_spacy_load)
    with pytest.raises(LanguageNotInstalledError) as e:
        SpacyModel.SingletonSpacyModel(fake_input)
    assert expected_model_in_message in str(e.value)
