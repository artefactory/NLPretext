NLPretext
==============================

### **No more pretext for dirty text** :pencil:


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


Cannot find what you were looking for? Feel free to open an [issue]((https://github.com/artefactory/nlpretext/issues) ).



# Installation

This package has been tested on Python **3.6**, **3.7** and **3.8**.

To install this library you just have to run the following command:

```bash
pip install git+https://github.com/artefactory/NLPretext.git
```

We strongly advise you to do the remaining steps in a virtual environnement.


This library uses Spacy as tokenizer. Current models supported are `en_core_web_sm` and `fr_core_news_sm`. If not installed, run the following commands:
```bash
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.3.1/en_core_web_sm-2.3.1.tar.gz
```

```bash
pip install https://github.com/explosion/spacy-models/releases/download/fr_core_news_sm-2.3.0/fr_core_news_sm-2.3.0.tar.gz
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
# "I just got the best dinner in my life !!! I recommend"
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

Take a look at all the functions that are available [here](https://github.com/artefactory/NLPretext/tree/feature/readme/nlpretext) in the ```preprocess.py``` scripts in the different folders: basic, social, token.


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
    ├── Makefile            <- Makefile with commands like `make data` or `make train`
    ├── README.md           <- The top-level README for developers using this project.
    ├── config              <- Where the configuration and constants live
    ├── datasets/external   <- Bash scripts to download external datasets
    ├── docker              <- Where to build a docker image using this lib
    ├── docs                <- Sphinx HTML documentation
    │   ├── _build
    │   │   └── html
    │   ├── source
    ├── nlpretext           <- Main Package. This is where the code lives
    │   ├── preprocessor.py <- Main preprocessing script
    │   ├── augmentation    <- Text augmentation script
    │   ├── basic           <- Basic text preprocessing 
    │   ├── social          <- Social text preprocessing
    │   └── token           <- Token preprocessing
    ├── utils               <- Where preprocessing utils scripts lives
    ├── tests               <- Where the tests lives
    ├── setup.py            <- makes project pip installable (pip install -e .) so the package can be imported
    ├── requirements.txt    <- The requirements file for reproducing the analysis environment, e.g.
                              generated with `pip freeze > requirements.txt`    
