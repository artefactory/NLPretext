"""
Testing for textpipe doc.py
"""
import pytest
import random
import spacy
from nautilus_nlp.models.Language_detector import LangDetector
from nautilus_nlp.doc import Doc, NautilusMissingModelException

TEXT_1 = """
Google was founded in 1998 by Larry Page and Sergey Brin while they were Ph.D. students at Stanford University in California. Together they own about 14 percent of its shares and control 56 percent of the stockholder voting power through supervoting stock. They incorporated Google as a privately held company on September 4, 1998. An initial public offering (IPO) took place on August 19, 2004, and Google moved to its headquarters in Mountain View, California, nicknamed the Googleplex. In August 2015, Google announced plans to reorganize its various interests as a conglomerate called Alphabet Inc. Google is Alphabet's leading subsidiary and will continue to be the umbrella company for Alphabet's Internet interests. Sundar Pichai was appointed CEO of Google, replacing Larry Page who became the CEO of Alphabet.
"""

TEXT_2 = """Les moteurs de recherche tels Google, Exalead ou Yahoo! sont des applications très connues de fouille de textes sur de grandes masses de données.
            Cependant, les moteurs de recherche ne se basent pas uniquement sur le texte pour l'indexer,
            mais également sur la façon dont les pages sont mises en valeur les unes par rapport aux autres.
            L'algorithme utilisé par Google est PageRank, et il est courant de voir HITS dans le milieu académique  
"""

TEXT_3 = ""

TEXT_4 = """this is a paragraph
this is a paragraph
"""

TEXT_5 = """Mark Zuckerberg is sinds de oprichting van Facebook de directeur van het bedrijf."""

TEXT_6 = """
မြန်မာဘာသာစကားသည် တိဘက်-ဗမာနွယ် ဘာသာစကားများ အုပ်စုတွင် ပါဝင်သည်။
တိဘက်-ဗမာနွယ် ဘာသာစကားများ အုပ်စုသည် တရုတ်-တိဗက်နွယ် ဘာသာစကားများ
မိသားစု ထဲတွင် ပါသည်။ မြန်မာဘာသာသည် တက်ကျသံရှိသော
၊နိမ့်မြင့်အမှတ်အသားရှိ ဖြစ်သော၊ ဧကဝဏ္ဏစကားလုံး အလွန်များသော ဘာသာစကား
ဖြစ်သည်။ ကတ္တား-ကံ-တြိယာ စကားလုံးအစီအစဉ်ဖြင့် ရေးသော သရုပ်ခွဲဘာသာစကား
လည်းဖြစ်သည်။ မြန်မာအက္ခရာများသည် ဗြာဟ္မီအက္ခရာ သို့မဟုတ် ဗြာဟ္မီအက္ခရာမှ
ဆက်ခံထားသောမွန်အက္ခရာတို့မှ ဆင်းသက်လာသည်။
"""

TEXT_7 = """\nHi <<First Name>>\nthis is filler text \xa325 more filler.\nadditilnal 
filler.\nyet more\xa0still more\xa0filler.\n\xa0\nmore\nfiller.\x03\n\t\t\t\t\t\t    
almost there \n\\n\nthe end\n"""

ents_model = spacy.blank("nl")
custom_spacy_nlps = {"nl": {"ents": ents_model}}
detector = LangDetector()

DOC_1 = Doc(TEXT_1, language="en")
DOC_2 = Doc(TEXT_2, language="fr")
DOC_4 = Doc(TEXT_4, "en")
DOC_5 = Doc(TEXT_5, language="nl", spacy_nlps=custom_spacy_nlps)
DOC_6 = Doc(TEXT_6, langdetect=detector)
DOC_7 = Doc(TEXT_7, "en")


def test_load_custom_model():
    """
    The custom spacy language modules should be correctly loaded into the doc.
    """
    model_mapping = {"nl": "ents"}
    lang = DOC_5.language
    assert lang == "nl"
    assert sorted(DOC_5.find_entities()) == sorted(
        [("Mark Zuckerberg", "PER"), ("Facebook", "PER")]
    )
    assert DOC_5.find_entities(model_mapping[lang]) == []


def test_nwords_nsents():
    assert DOC_1.n_words == 145
    assert DOC_2.n_words == 83
    assert DOC_1.n_sentences == 7
    assert DOC_2.n_sentences == 3


def test_entities():
    assert sorted(DOC_1.entities) == sorted(
        [
            ("1998", "DATE"),
            ("56 percent", "PERCENT"),
            ("Alphabet", "GPE"),
            ("Alphabet", "ORG"),
            ("Alphabet Inc. Google", "ORG"),
            ("August 19, 2004", "DATE"),
            ("August 2015", "DATE"),
            ("California", "GPE"),
            ("Google", "ORG"),
            ("Googleplex", "ORG"),
            ("IPO", "ORG"),
            ("Larry Page", "PERSON"),
            ("Mountain View", "GPE"),
            ("Ph.D.", "PERSON"),
            ("September 4, 1998", "DATE"),
            ("Sergey Brin", "PERSON"),
            ("Stanford University", "ORG"),
            ("Sundar Pichai", "PERSON"),
            ("about 14 percent", "PERCENT"),
        ]
    )
    assert sorted(DOC_2.entities) == sorted(
        [
            ("Exalead", "ORG"),
            ("Google", "ORG"),
            ("HITS", "MISC"),
            ("PageRank", "MISC"),
            ("Yahoo!", "ORG"),
        ]
    )


def test_complexity():
    assert DOC_1.complexity == 48.06961538461539
    assert DOC_2.complexity == 78.634_035_087_719_3


def test_clean():
    assert len(TEXT_1) >= len(DOC_1.clean)
    assert len(TEXT_2) >= len(DOC_2.clean)


def test_clean_newlines():
    assert " ".join(TEXT_4.split()) == DOC_4.clean


def test_extract_keyterms():
    non_ranker = "bulthaup"
    rankers = ["textrank", "sgrank", "singlerank"]
    with pytest.raises(
        ValueError,
        message=f'algorithm "{non_ranker}" not ' f"available; use one of {rankers}",
    ):
        DOC_1.extract_keyterms(ranker=non_ranker)
    assert len(DOC_1.extract_keyterms()) == 10
    # limits number of keyterms
    assert len(DOC_1.extract_keyterms(n_terms=2)) == 2
    # works with other rankers
    assert isinstance(DOC_2.extract_keyterms(ranker=random.choice(rankers)), list)


def test_missing_language_model():
    with pytest.raises(NautilusMissingModelException):
        DOC_6.n_words


def test_non_utf_chars():
    assert DOC_7.language == "en"
