# NLPretext

<p align="center">
    <img src="/references/logo_nlpretext.png" />
</p>

<div align="center">

[![CI status](https://github.com/artefactory/NLPretext/actions/workflows/ci.yml/badge.svg?branch%3Amain&event%3Apush)](https://github.com/artefactory/NLPretext/actions/workflows/ci.yml?query=branch%3Amain)
[![CD status](https://github.com/artefactory/NLPretext/actions/workflows/cd.yml/badge.svg?event%3Arelease)](https://github.com/artefactory/NLPretext/actions/workflows/cd.yml?query=event%3Arelease)
[![Python Version](https://img.shields.io/badge/Python-3.8-informational.svg)](#supported-python-versions)
[![Dependencies Status](https://img.shields.io/badge/dependabots-active-informational.svg)](https://github.com/artefactory/NLPretext}/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-informational.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-informational?logo=pre-commit&logoColor=white)](https://github.com/artefactory/NLPretext}/blob/main/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%F0%9F%9A%80-semantic%20versions-informational.svg)](https://github.com/artefactory/NLPretext/releases)
[![Documentation](https://img.shields.io/badge/doc-sphinx-informational.svg)](https://github.com/artefactory/NLPretext}/tree/main/docs)
[![License](https://img.shields.io/badge/License-Apache%20Software%20License%202.0-informational.svg)](https://github.com/artefactory/NLPretext}/blob/main/LICENSE)

All the goto functions you need to handle NLP use-cases, integrated in NLPretext

</div>

# TL;DR


> *Working on an NLP project and tired of always looking for the same silly preprocessing functions on the web?*  :tired_face: 

> *Need to efficiently extract email adresses from a document? Hashtags from tweets? Remove accents from a French post?* :disappointed_relieved:


**NLPretext got you covered!** :rocket:

NLPretext packages in a **unique** library all the text **preprocessing** functions you need to **ease** your NLP project. 


:mag: Quickly explore below our preprocessing pipelines and individual functions referential.

* [Default preprocessing pipeline](#default_pipeline)
* [Custom preprocessing pipeline](#custom_pipeline)
* [Replacing phone numbers](#replace_phone_numbers)
* [Removing hashtags](#remove_hashtags)
* [Extracting emojis](#extract_emojis)
* [Data augmentation](#data_augmentation)


Cannot find what you were looking for? Feel free to open an [issue]((https://github.com/artefactory/nlpretext/issues) ).



# Installation

### Supported Python Versions

- Main version supported : `3.8`
- Other supported versions : `3.9`, `3.10`


We strongly advise you to do the remaining steps in a virtual environnement.

To install this library from PyPi, run the following command:

```bash
pip install nlpretext
```

or with `Poetry`

```bash
poetry add nlpretext
```


# Usage

## Default pipeline <a name="default_pipeline"></a>

Need to preprocess your text data but no clue about what function to use and in which order? The default preprocessing pipeline got you covered:

```python
from nlpretext import Preprocessor
text = "I just got the best dinner in my life @latourdargent !!! I  recommend 😀 #food #paris \n"
preprocessor = Preprocessor()
text = preprocessor.run(text)
print(text)
# "I just got the best dinner in my life!!! I recommend"
```

## Create your custom pipeline <a name="custom_pipeline"></a>

Another possibility is to create your custom pipeline if you know exactly what function to apply on your data, here's an example:

```python
from nlpretext import Preprocessor
from nlpretext.basic.preprocess import (normalize_whitespace, remove_punct, remove_eol_characters,
remove_stopwords, lower_text)
from nlpretext.social.preprocess import remove_mentions, remove_hashtag, remove_emoji
text = "I just got the best dinner in my life @latourdargent !!! I  recommend 😀 #food #paris \n"
preprocessor = Preprocessor()
preprocessor.pipe(lower_text)
preprocessor.pipe(remove_mentions)
preprocessor.pipe(remove_hashtag)
preprocessor.pipe(remove_emoji)
preprocessor.pipe(remove_eol_characters)
preprocessor.pipe(remove_stopwords, args={'lang': 'en'})
preprocessor.pipe(remove_punct)
preprocessor.pipe(normalize_whitespace)
text = preprocessor.run(text)
print(text)
# "dinner life recommend"
```

Take a look at all the functions that are available [here](https://github.com/artefactory/NLPretext/tree/master/nlpretext) in the ```preprocess.py``` scripts in the different folders: basic, social, token.


## Load text data

Pre-processing text data is useful only if you have loaded data to process! Importing text data as strings in your code can be really simple if you have short texts contained in a local .txt, but it can quickly become difficult if you want to load a lot of texts, stored in multiple formats and divided in multiple files. Hopefully, you can use NLPretext's TextLoader class to easily import text data.
while it is not mandatory our textLoader work best with dask, make sure to have the librairy installed if you want the best performances.

```python
from nlpretext.textloader import TextLoader
files_path = "local_folder/texts/text.txt"
text_loader = TextLoader(use_dask=True)
text_dataframe = text_loader.read_text(files_path)
print(text_dataframe.text.values.tolist())
# ["I just got the best dinner in my life!!!",  "I recommend", "It was awesome"]
```

File path can be provided as string, list of strings, with or without wildcards. It also supports imports from cloud providers, if your machine is authentified on a project.

```python
text_loader = TextLoader(text_column="name_of_text_column_in_your_data")

local_file_path = "local_folder/texts/text.csv" # File from local folder
local_corpus_path = ["local_folder/texts/text_1.csv", "local_folder/texts/text_2.csv", "local_folder/texts/text_3.csv"] # Multiple files from local folder

gcs_file_path = "gs://my-bucket/texts/text.json" # File from GCS
s3_file_path = "s3://my-bucket/texts/text.json" # File from S3
hdfs_file_path = "hdfs://folder/texts/text.txt" # File from HDFS
azure_file_path = "az://my-bucket/texts/text.parquet" # File from Azure

gcs_corpus_path = "gs://my-bucket/texts/text_*.json" # Multiple files from GCS with wildcard

text_dataframe_1 = text_loader.read_text(local_file_path)
text_dataframe_2 = text_loader.read_text(local_corpus_path)
text_dataframe_3 = text_loader.read_text(gcs_file_path)
text_dataframe_4 = text_loader.read_text(s3_file_path)
text_dataframe_5 = text_loader.read_text(hdfs_file_path)
text_dataframe_6 = text_loader.read_text(azure_file_path)
text_dataframe_7 = text_loader.read_text(gcs_corpus_path)

```

You can also specify a Preprocessor if you want your data to be directly pre-processed when loaded.
```python
text_loader = TextLoader(text_column="text_col")
preprocessor = Preprocessor()

file_path = "local_folder/texts/text.csv" # File from local folder

raw_text_dataframe = text_loader.read_text(local_file_path)
preprocessed_text_dataframe = text_loader.read_text(local_file_path, preprocessor=preprocessor)

print(raw_text_dataframe.text_col.values.tolist())
# ["These   texts are not preprocessed",  "This is bad ## "]

print(preprocessed_text_dataframe.text_col.values.tolist())
# ["These texts are not preprocessed",  "This is bad"]
```


## Individual Functions

### Replacing emails <a name="replace_emails"></a>

```python
from nlpretext.basic.preprocess import replace_emails
example = "I have forwarded this email to obama@whitehouse.gov"
example = replace_emails(example, replace_with="*EMAIL*")
print(example)
# "I have forwarded this email to *EMAIL*"
```

### Replacing phone numbers <a name="replace_phone_numbers"></a>

```python
from nlpretext.basic.preprocess import replace_phone_numbers
example = "My phone number is 0606060606"
example = replace_phone_numbers(example, country_to_detect=["FR"], replace_with="*PHONE*")
print(example)
# "My phone number is *PHONE*"
```

### Removing Hashtags <a name="remove_hashtags"></a>

```python
from nlpretext.social.preprocess import remove_hashtag
example = "This restaurant was amazing #food #foodie #foodstagram #dinner"
example = remove_hashtag(example)
print(example)
# "This restaurant was amazing"
```

### Extracting emojis <a name="extract_emojis"></a>

```python
from nlpretext.social.preprocess import extract_emojis
example = "I take care of my skin 😀"
example = extract_emojis(example)
print(example)
# [':grinning_face:']
```

## Data augmentation <a name="data_augmentation"></a>

The augmentation module helps you to **generate new texts** based on your given examples by modifying some words in the initial ones and to **keep associated entities unchanged**, if any, in the case of **NER tasks**. If you want words other than entities to remain unchanged, you can specify it within the `stopwords` argument. Modifications depend on the chosen method, the ones currently supported by the module are **substitutions with synonyms** using Wordnet or BERT from the [`nlpaug`](https://github.com/makcedward/nlpaug) library. 

```python
from nlpretext.augmentation.text_augmentation import augment_text
example = "I want to buy a small black handbag please."
entities = [{'entity': 'Color', 'word': 'black', 'startCharIndex': 22, 'endCharIndex': 27}]
example = augment_text(example, method=”wordnet_synonym”, entities=entities)
print(example)
# "I need to buy a small black pocketbook please."
```




# 📈 Releases

You can see the list of available releases on the [GitHub Releases](https://github.com/artefactory/NLPretext}/releases) page.

We follow [Semantic Versions](https://semver.org/) specification.

We use [`Release Drafter`](https://github.com/marketplace/actions/release-drafter). As pull requests are merged, a draft release is kept up-to-date listing the changes, ready to publish when you’re ready. With the categories option, you can categorize pull requests in release notes using labels.

For Pull Requests, these labels are configured, by default:

|               **Label**               |  **Title in Releases**  |
| :-----------------------------------: | :---------------------: |
|       `enhancement`, `feature`        |       🚀 Features       |
| `bug`, `refactoring`, `bugfix`, `fix` | 🔧 Fixes & Refactoring  |
|       `build`, `ci`, `testing`        | 📦 Build System & CI/CD |
|              `breaking`               |   💥 Breaking Changes   |
|            `documentation`            |    📝 Documentation     |
|            `dependencies`             | ⬆️ Dependencies updates |


GitHub creates the `bug`, `enhancement`, and `documentation` labels automatically. Dependabot creates the `dependencies` label. Create the remaining labels on the Issues tab of the GitHub repository, when needed.## 🛡 License

[![License](https://img.shields.io/github/license/artefactory/NLPretext)](https://github.com/artefactory/NLPretext}/blob/main/LICENSE)

This project is licensed under the terms of the `Apache Software License 2.0` license. See [LICENSE](https://github.com/artefactory/NLPretext}/blob/main/LICENSE) for more details.## 📃 Citation

```
@misc{nlpretext,
  author = {artefactory},
  title = {All the goto functions you need to handle NLP use-cases, integrated in NLPretext},
  year = {2021},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/artefactory/NLPretext}}}
}
```


# Project Organization
------------

    ├── LICENSE
    ├── CONTRIBUTING.md     <- Contribution guidelines
    ├── CODE_OF_CONDUCT.md  <- Code of conduct guidelines
    ├── Makefile
    ├── README.md           <- The top-level README for developers using this project.
    ├── .github/workflows   <- Where the CI and CD lives
    ├── datasets/external   <- Bash scripts to download external datasets
    ├── docker              <- All you need to build a Docker image from that package
    ├── docs                <- Sphinx HTML documentation
    ├── nlpretext           <- Main Package. This is where the code lives
    │   ├── preprocessor.py <- Main preprocessing script
    │   ├── text_loader.py  <- Main loading script
    │   ├── augmentation    <- Text augmentation script
    │   ├── basic           <- Basic text preprocessing
    │   ├── cli             <- Command lines that can be used
    │   ├── social          <- Social text preprocessing
    │   ├── token           <- Token text preprocessing
    │   ├── textloader      <- File loading
    │   ├── _config         <- Where the configuration and constants live
    │   └── _utils          <- Where preprocessing utils scripts lives
    ├── tests               <- Where the tests lives
    ├── pyproject.toml      <- Package configuration
    ├── poetry.lock         
    └── setup.cfg           <- Configuration for plugins and other utils

# Credits

- [textacy](https://github.com/chartbeat-labs/textacy) for the following basic preprocessing functions:
    - `fix_bad_unicode`
    - `normalize_whitespace`
    - `unpack_english_contractions`
    - `replace_urls`
    - `replace_emails`
    - `replace_numbers`
    - `replace_currency_symbols`
    - `remove_punct`
    - `remove_accents`
    - `replace_phone_numbers` *(with some modifications of our own)*
