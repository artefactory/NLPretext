NLPretext
==============================

<p align="center">
    <img src="/references/logo_nlpretext.png" />
</p>

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

This package has been tested on Python **3.6**, **3.7** and **3.8**.

We strongly advise you to do the remaining steps in a virtual environnement.

To install this library you just have to run the following command:

```bash
pip install nlpretext
```



This library uses Spacy as tokenizer. Current models supported are `en_core_web_sm` and `fr_core_news_sm`. If not installed, run the following commands:
```bash
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.3.1/en_core_web_sm-2.3.1.tar.gz
```

```bash
pip install https://github.com/explosion/spacy-models/releases/download/fr_core_news_sm-2.3.0/fr_core_news_sm-2.3.0.tar.gz
```

To use our TextLoader class, you'll need to install Dask as well:
```bash
pip install dask[complete]==2021.3.0
```

# Preprocessing pipeline

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


# Load text data

Pre-processing text data is useful only if you have loaded data to process! Importing text data as strings in your code can be really simple if you have short texts contained in a local .txt, but it can quickly become difficult if you want to load a lot of texts, stored in multiple formats and divided in multiple files. Hopefully, you can use NLPretext's TextLoader class to easily import text data.
Our TextLoader class makes use of Dask, so be sure to install the library if you want to use it, as mentioned above.

```python
from nlpretext.textloader import TextLoader
files_path = "local_folder/texts/text.txt"
text_loader = TextLoader()
text_dataframe = text_loader.read_text(files_path)
print(text_dataframe.text.values.tolist())
# ["I just got the best dinner in my life!!!",  "I recommend", "It was awesome"]
```

As TextLoader uses dask to load data, file path can be provided as string, list of strings, with or without wildcards. It also supports imports from cloud providers, if your machine is authentified on a project.

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



# Individual Functions

## Replacing emails <a name="replace_emails"></a>

```python
from nlpretext.basic.preprocess import replace_emails
example = "I have forwarded this email to obama@whitehouse.gov"
example = replace_emails(example, replace_with="*EMAIL*")
print(example)
# "I have forwarded this email to *EMAIL*"
```

## Replacing phone numbers <a name="replace_phone_numbers"></a>

```python
from nlpretext.basic.preprocess import replace_phone_numbers
example = "My phone number is 0606060606"
example = replace_phone_numbers(example, country_to_detect=["FR"], replace_with="*PHONE*")
print(example)
# "My phone number is *PHONE*"
```

## Removing Hashtags <a name="remove_hashtags"></a>

```python
from nlpretext.social.preprocess import remove_hashtag
example = "This restaurant was amazing #food #foodie #foodstagram #dinner"
example = remove_hashtag(example)
print(example)
# "This restaurant was amazing"
```

## Extracting emojis <a name="extract_emojis"></a>

```python
from nlpretext.social.preprocess import extract_emojis
example = "I take care of my skin 😀"
example = extract_emojis(example)
print(example)
# [':grinning_face:']
```

# Data augmentation <a name="data_augmentation"></a>

The augmentation module helps you to **generate new texts** based on your given examples by modifying some words in the initial ones and to **keep associated entities unchanged**, if any, in the case of **NER tasks**. If you want words other than entities to remain unchanged, you can specify it within the `stopwords` argument. Modifications depend on the chosen method, the ones currently supported by the module are **substitutions with synonyms** using Wordnet or BERT from the [`nlpaug`](https://github.com/makcedward/nlpaug) library. 

```python
from nlpretext.augmentation.text_augmentation import augment_text
example = "I want to buy a small black handbag please."
entities = [{'entity': 'Color', 'word': 'black', 'startCharIndex': 22, 'endCharIndex': 27}]
example = augment_text(example, method=”wordnet_synonym”, entities=entities)
print(example)
# "I need to buy a small black pocketbook please."
```


# Make HTML documentation

In order to make the html Sphinx documentation, you need to run at the nlpretext root path:
`sphinx-apidoc -f nlpretext -o docs/`
This will generate the .rst files.
You can generate the doc with
`cd docs && make html`

You can now open the file index.html located in the build folder.

# Project Organization
------------

    ├── LICENSE
    ├── VERSION
    ├── CONTRIBUTING.md     <- Contribution guidelines
    ├── README.md           <- The top-level README for developers using this project.
    ├── .github/workflows   <- Where the CI lives
    ├── datasets/external   <- Bash scripts to download external datasets
    ├── docs                <- Sphinx HTML documentation
    ├── nlpretext           <- Main Package. This is where the code lives
    │   ├── preprocessor.py <- Main preprocessing script
    │   ├── augmentation    <- Text augmentation script
    │   ├── basic           <- Basic text preprocessing 
    │   ├── social          <- Social text preprocessing
    │   ├── token           <- Token text preprocessing
    │   ├── _config         <- Where the configuration and constants live
    │   └── _utils          <- Where preprocessing utils scripts lives
    ├── tests               <- Where the tests lives
    ├── setup.py            <- makes project pip installable (pip install -e .) so the package can be imported
    ├── requirements.txt    <- The requirements file for reproducing the analysis environment, e.g.
    │                          generated with `pip freeze > requirements.txt`
    └── pylintrc            <- The linting configuration file


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

