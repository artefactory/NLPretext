Insert new lib name here
==============================

**Insert new logo here**

:tired_face: Working on an NLP project and tired of always looking for the same silly preprocessing functions on the web? 

:disappointed_relieved: Need to efficiently extract email adresses from a document? Hashtags from tweets? Remove accents from a French post? 

**Insert new lib name here** got you covered! :rocket:

**Insert new lib name here** packages in a unique library all the text preprocessing functions you need to ease your NLP project. 

:mag: Quickly explore below our functions referential.

* [Replacing emails](#replace_emails)
* [Replacing phone numbers](#replace_phone_numbers)
* [Removing hashtags](#remove_hashtags)
* [Extracting emojis](#extract_emojis)


Cannot find a new one? Feel free to open an [issue]((https://github.com/artefactory/nautilus-nlp/issues) )).



# Installation

This package has been tested on Python **3.7**.

To install this library you should first clone the repository:

```bash
git clone git@github.com:artefactory/nautilus-nlp.git && cd nautilus_nlp/
```

We strongly advise you to do the remaining steps in a virtual environnement.

First install the required files:

```bash
pip install -r requirements.txt
```

then install the library with pip:

```bash
pip install -e .
```

This library uses Spacy as tokenizer. Current models supported are `en_core_web_sm` and `fr_core_news_sm`.


# Functions

## Replacing emails <a name="replace_emails"></a>

```python
example = "I have forwarded this email to obama@whitehouse.gov"
example = replace_emails(replace_with="*EMAIL*")
print(example)
# "I have forwarded this email to *EMAIL*"
```

## Replacing phone numbers <a name="replace_phone_numbers"></a>

```python
Insert example here
```

## Removing Hashtags <a name="remove_hashtags"></a>

```python
Insert example here
```

## Extracting emojis <a name="extract_emojis"></a>

```python
Insert example here
```

# Make HTML documentation

**à updater**

In order to make the html Sphinx documentation, you need to run at the nautilus_nlp root path:
`sphinx-apidoc -f nautilus_nlp -o docs/`
This will generate the .rst files.
You can generate the doc with
`cd docs && make html`

You can now open the file index.html located in the build folder.

# Project Organization
------------
**à updater**

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
    ├── nautilus_nlp        <- Main Nautilus Package. This is where the code lives
    │   ├── preprocessor.py <- Main preprocessing script
    │   ├── augmentation    <- Text augmentation script
    │   ├── classic         <- Classic text preprocessing 
    │   ├── social          <- Social text preprocessing
    │   └── token           <- Token preprocessing
    ├── utils               <- Where preprocessing utils scripts lives
    ├── tests               <- Where the tests lives
    ├── setup.py            <- makes project pip installable (pip install -e .) so nautilus_nlp can be imported
    ├── requirements.txt    <- The requirements file for reproducing the analysis environment, e.g.
                              generated with `pip freeze > requirements.txt`    
