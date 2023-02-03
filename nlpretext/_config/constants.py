# Copyright (C) 2020 Artefact
# licence-information@artefact.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License
# mypy: disable-error-code="attr-defined"

"""
Collection of regular expressions and other (small, generally useful) constants.
Credits to textacy for some of them: https://github.com/chartbeat-labs/textacy
"""
import re
import sys
import unicodedata

import regex

NUMERIC_NE_TYPES = {
    "ORDINAL",
    "CARDINAL",
    "MONEY",
    "QUANTITY",
    "PERCENT",
    "TIME",
    "DATE",
}
SUBJ_DEPS = {"agent", "csubj", "csubjpass", "expl", "nsubj", "nsubjpass"}
OBJ_DEPS = {"attr", "dobj", "dative", "oprd"}
AUX_DEPS = {"aux", "auxpass", "neg"}

REPORTING_VERBS = {
    "according",
    "accuse",
    "acknowledge",
    "add",
    "admit",
    "agree",
    "allege",
    "announce",
    "argue",
    "ask",
    "assert",
    "believe",
    "blame",
    "charge",
    "cite",
    "claim",
    "complain",
    "concede",
    "conclude",
    "confirm",
    "contend",
    "criticize",
    "declare",
    "decline",
    "deny",
    "describe",
    "disagree",
    "disclose",
    "estimate",
    "explain",
    "fear",
    "hope",
    "insist",
    "maintain",
    "mention",
    "note",
    "observe",
    "order",
    "predict",
    "promise",
    "recall",
    "recommend",
    "reply",
    "report",
    "say",
    "state",
    "stress",
    "suggest",
    "tell",
    "testify",
    "think",
    "urge",
    "warn",
    "worry",
    "write",
}

CURRENCIES = {
    "$": "USD",
    "zł": "PLN",
    "£": "GBP",
    "¥": "JPY",
    "฿": "THB",
    "₡": "CRC",
    "₦": "NGN",
    "₩": "KRW",
    "₪": "ILS",
    "₫": "VND",
    "€": "EUR",
    "₱": "PHP",
    "₲": "PYG",
    "₴": "UAH",
    "₹": "INR",
}

POS_REGEX_PATTERNS = {
    "en": {
        "NP": r"<DET>? <NUM>* (<ADJ> <PUNCT>? <CONJ>?)* (<NOUN>|<PROPN> <PART>?)+",
        "PP": r"<ADP> <DET>? <NUM>* (<ADJ> <PUNCT>? <CONJ>?)* (<NOUN> <PART>?)+",
        "VP": r"<AUX>* <ADV>* <VERB>",
    }
}

PUNCT_TRANSLATE_UNICODE = dict.fromkeys(
    (i for i in range(sys.maxunicode) if unicodedata.category(chr(i)).startswith("P")),
    " ",
)


ACRONYM_REGEX = re.compile(
    r"(?:^|(?<=\W))(?:(?:(?:(?:[A-Z]\.?)+[a-z0-9&/-]?)+(?:[A-Z][s.]?|[0-9]s?))|(?:[0-9](?:\-?[A-Z])+))(?:$|(?=\W))",
    flags=re.UNICODE,
)
EMAIL_REGEX = re.compile(
    r"(?:^|(?<=[^\w@.)]))([\w+-](\.(?!\.))?)*?[\w+-]@(?:\w-?)*?\w+(\.([a-z]{2,})){1,3}(?:$|(?=\b))",
    flags=re.IGNORECASE | re.UNICODE,
)
PHONE_REGEX = re.compile(
    r"(?:^|(?<=[^\w)]))(\+?1[ .-]?)?(\(?\d{3}\)?[ .-]?)?(\d{3}[ .-]?\d{4})(\s?(?:ext\.?|[#x-])\s?\d{2,6})?(?:$|(?=\W))"
)
NUMBERS_REGEX = re.compile(
    r"(?:^|(?<=[^\w,.]))[+–-]?(([1-9]\d{0,2}(,\d{3})+(\.\d*)?)|([1-9]\d{0,2}([ .]\d{3})+(,\d*)?)|"
    r"(\d*?[.,]\d+)|\d+)(?:|(?=\b))"
)
CURRENCY_REGEX = re.compile("({})+".format("|".join(re.escape(c) for c in CURRENCIES)))
LINEBREAK_REGEX = re.compile(r"((\r\n)|[\n\v])+")
NONBREAKING_SPACE_REGEX = re.compile(r"(?!\n)\s+")
URL_REGEX = re.compile(
    r"(?:|(?<![\w/.]))"
    # protocol identifier
    # r"(?:(?:https?|ftp)://)"  <-- alt?
    r"(?:(?:https?://|mailto:|ftp://|www\d{0,3}\.))"
    # user:pass authentication
    r"(?:\S+(?::\S*)?@)?" r"(?:"
    # IP address exclusion
    # private & local networks
    r"(?!(?:10|127)(?:\.\d{1,3}){3})"
    r"(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})"
    r"(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})"
    # IP address dotted notation octets
    # excludes loopback network 0.0.0.0
    # excludes reserved space >= 224.0.0.0
    # excludes network & broadcast addresses
    # (first & last IP address of each class)
    r"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
    r"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
    r"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
    r"|"
    # host name
    r"(?:(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)"
    # domain name
    r"(?:\.(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)*"
    # TLD identifier
    r"(?:\.(?:[a-z\u00a1-\uffff]{2,}))" r")"
    # port number
    r"(?::\d{2,5})?"
    # resource path
    r"(?:/\S*)?" r"(?:$|(?![\w?!+&/]))",
    flags=re.UNICODE | re.IGNORECASE,
)  # source: https://gist.github.com/dperini/729294
SHORT_URL_REGEX = re.compile(
    r"(?:^|(?<![\w/.]))"
    # optional scheme
    r"(?:(?:https?://)?)"
    # domain
    r"(?:\w-?)*?\w+(?:\.[a-z]{2,12}){1,3}" r"/"
    # hash
    r"[^\s.,?!'\"|+]{2,12}" r"(?:$|(?![\w?!+&/]))",
    flags=re.IGNORECASE,
)

# regexes for cleaning up crufty terms
DANGLING_PARENS_TERM_RE = re.compile(
    r"(?:\s|^)(\()\s{1,2}(.*?)\s{1,2}(\))(?:\s|$)", flags=re.UNICODE
)
LEAD_TAIL_CRUFT_TERM_RE = re.compile(r"^([^\w(-] ?)+|([^\w).!?] ?)+$", flags=re.UNICODE)
LEAD_HYPHEN_TERM_RE = re.compile(r"^-([^\W\d_])", flags=re.UNICODE)
NEG_DIGIT_TERM_RE = re.compile(r"(-) (\d)", flags=re.UNICODE)
WEIRD_HYPHEN_SPACE_TERM_RE = re.compile(r"(?<=[^\W\d]) (-[^\W\d])", flags=re.UNICODE)
WEIRD_APOSTR_SPACE_TERM_RE = re.compile(r"([^\W\d]+) ('[a-z]{1,2}\b)", flags=re.UNICODE)
LATIN_CHARACTERS_RE = regex.compile(r"[^\p{Latin}1-9]")

# ENGLISH CONTRACTIONS
CONTRACTION_NT_NOT = re.compile(
    r"(\b)(are|could|did|does|do|had|has|have|is|might|must|should|were|would)n't", re.IGNORECASE
)
CONTRACTION_LL_WILL = re.compile(r"(\b)(he|i|she|they|we|what|who|you)'ll", re.IGNORECASE)
CONTRACTION_RE_ARE = re.compile(r"(\b)(they|we|what|who|you)'re", re.IGNORECASE)
CONTRACTION_VE_HAVE = re.compile(r"(\b)(i|should|they|we|what|who|would|you)'ve", re.IGNORECASE)
CONTRACTION_CANT_CANNOT = re.compile(r"(\b)(ca)n't", re.IGNORECASE)
CONTRACTION_M_AM = re.compile(r"(\b)(i)'m", re.IGNORECASE)
CONTRACTION_LET_LETUS = re.compile(r"(\b)(let)'s", re.IGNORECASE)
CONTRACTION_WONT_WILLNOT = re.compile(r"(\b)(w)on't", re.IGNORECASE)
CONTRACTION_SHANT_SHALLNOT = re.compile(r"(\b)(s)han't", re.IGNORECASE)
CONTRACTION_YALL_YOUALL = re.compile(r"(\b)(y)(?:'all|a'll)", re.IGNORECASE)

# SOCIAL DATA
HASHTAG_PATTERN = re.compile(r"#\w*")
AT_PATTERN = re.compile(r"@\w*")
HTML_TAG_PATTERN = re.compile(r"<.*?>")

# TEXT LOADER
TEXT_FILE_FORMATS_PATTERN = re.compile(r"^.*\.(json|csv|txt|parquet)(\.gz|\.zip)*$")
