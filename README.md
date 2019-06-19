Nautilus_NLP [![Build Status](https://travis-ci.com/artefactory/nautilus-nlp.svg?token=Ssg4shz5pz9qGnYCybSj&branch=master)](https://travis-ci.com/artefactory/nautilus-nlp)
==============================
![Nautilus-NLP](/references/nautilus_nlp_logo.png)

The Nautilus NLP library aimed to be a meta-library to be used to help you get started on handling your NLP use-case.

This library can help you with:

    1. Cleaning text data
    2. Normalizing your dataset
    3. Training automatically multiclass, multilabel classifier
    4. Help you discover topics and cluster your data

You can find a list of the available features [in this article.](https://artefactory.atlassian.net/wiki/spaces/CK/pages/822837299/Nautilus+NLP+-+key+features)

# Feature Request

As an Artefact user, you might be working on a NLP use case, and wish to use Nautilus.

However, if you think Nautilus is lacking features that can be useful not only to your use case but also others, feel free to to [fill up an issue](https://github.com/artefactory/nautilus-nlp/issues) with the label "Feature-request".

We will try to put it in the roadmap and implement it as soon as possible.

# Installation

Beware, this package has been tested on Python **3.6** & **3.7**, and will probably not be working under python **2.7** as **Python2.7** EOL is scheduled for December 2019. 

To install this library you should first clone the repository:

```
git clone https://github.com/artefactory/nautilus_nlp/ && cd nautilus_nlp
```

**If you don't use the docker container, we strongly advise you to do these steps in a virtual environnement**

First you need to install the required files:

```
pip install -r requirements.txt
```

then you can install it via pip:

```
pip install -e .
```

## Handling installation errors


### Problem when building FastText on MACOS:

If you see this errorwhen building Fasttext:

    clang: warning: libstdc++ is deprecated; move to libc++ with a minimum deployment target of OS X 10.9 [-Wdeprecated]
    ld: library not found for -lstdc++
    clang: error: linker command failed with exit code 1 (use -v to see invocation)
    error: command 'g++' failed with exit status 1
Then you should type this command in your terminal:

    export MACOSX_DEPLOYMENT_TARGET=10.9

### command 'gcc' failed with exit status 1

While runing `pip install -r requirements.txt` you might get the following error message:

`command 'gcc' failed with exit status 1`

To solve it, run the following command before installing requirements.txt:

```
conda install pyemd
```

### Cannot uninstall 'package_name'

You might get the following error message while installing the library:
`Cannot uninstall 'PACKAGE_NAME'. It is a distutils installed project and thus we cannot accurately determine which files belong to it which would lead to only a partial uninstall.`

To fix this, just type `pip install -e . --ignore-installed PACKAGE_NAME` instead. 

### Installing nautilus-nlp on a linux-based VM

If you are installing nautilus on a linux-powered Virtual Machine (VM), you might want to install essentials first. If you don't, you might experience some issues to install Cython-based libraries, such as spaCy, becode the C compiler will be missing. 

On a Ubuntu VM (tested on 16.04), you can run the following command before following the classic installation process above:

```
# install compilators and required softwares
sudo apt-get update && sudo apt-get install -y build-essential unzip git wget
# install conda
wget https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh
bash Anaconda3-2019.03-Linux-x86_64.sh
```

## Installation of additional required libraries

If you want to leverage all the features of nautilus-nlp, you need to **install others required libraries** (such as FastText).

### Install spaCy language models

Installing additional spaCy models will give you the possibility to handle a lot of new language for text processing feature (such as lemmatization or tokenization). 

To do so, run: *(on your virtual environment if you are using one)*

`bash nautilus_nlp/scripts/download_spacy_models.sh`

### Install FastText 

run: 

`bash nautilus_nlp/scripts/install_fasttext.sh`

### Install Lang Detect

run: 

`bash nautilus_nlp/scripts/download_ft_langdetect.sh`

### Install Mallet

1) Install Mallet file
run:

`bash nautilus_nlp/scripts/install_mallet.sh`

2) Install Java JDK (required to implement mallet)
run:

`bash nautilus_nlp/scripts/install_java.sh`

# Quick start

The [notebook](notebooks/) folder contains various notebook on how to use this library.

Here is a quick example:

```
>>> from nautilus_nlp.preprocessing.preprocess import preprocess_text
>>> from nautilus_nlp.preprocessing.tokenizer import tokenize
>>> from nautilus_nlp.preprocessing.lemmatization import lemmatize_english_tokens
[nltk_data] Downloading package wordnet to /Users/hugo/nltk_data...
[nltk_data]   Package wordnet is already up-to-date!
>>> text = """Tropical Storm Nicole was a short-lived and unusually asymmetric tropical cyclone that caused extensive flooding in Jamaica during the 2010 Atlantic hurricane season.\nSource:https://en.wikipedia.org/wiki/Tropical_Storm_Nicole_(2010)"""
>>> clean_text = preprocess_text(text, lowercase=True,
...                                         no_punct=True,
...                                         no_numbers=True,
...                                         no_stopwords='en',
...                                         no_urls=True,
...                                         replace_with='')
>>> clean_text
'tropical storm nicole short lived unusually asymmetric tropical cyclone caused extensive flooding jamaica atlantic hurricane season source'
>>> tokenized_text = tokenize(clean_text)
>>> tokenized_text
['tropical', 'storm', 'nicole', 'short', 'lived', 'unusually', 'asymmetric', 'tropical', 'cyclone', 'caused', 'extensive', 'flooding', 'jamaica', 'atlantic', 'hurricane', 'season', 'source']
>>> lemma_text = lemmatize_english_tokens(tokenized_text)
>>> lemma_text
['tropical', 'storm', 'nicole', 'short', 'live', 'unusually', 'asymmetric', 'tropical', 'cyclone', 'cause', 'extensive', 'flooding', 'jamaica', 'atlantic', 'hurricane', 'season', 'source']
```


# Make HTML documentation

In order to make the html Sphinx documentation, you need to run at the nautilus_nlp root path:
`sphinx-apidoc -f nautilus_nlp -o docs/`
This will generate the .rst files.
You can generate the doc with
`cd docs && make html`

You can now open the file index.html located in the build folder.
# Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data               <- Scripts & bits to download datasets to try nautilus
    │   ├── external
    │   ├── interim
    │   ├── processed
    │   └── raw
    ├── docker             <- Where to build a docker image using this lib
    ├── docs               <- Sphinx HTML documentation
    │   ├── _build
    │   │   └── html
    │   ├── source
    ├── models
    ├── nautilus_nlp       <- Main Nautilus Package. This is where the code lives
    │   ├── config
    │   ├── data
    │   ├── models
    │   ├── preprocessing
    │   ├── scripts
    │   └── utils
    ├──notebooks           <- Various notebooks explaining how to use Nautilus_NLP library
    ├── tests <- Where the tests lives
    │   └── testfolder_fileloader
    ├── wiki               <- Where the Markdown for the Wiki lives
    ├── setup.py           <- makes project pip installable (pip install -e .) so nautilus_nlp can be imported
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
                              generated with `pip freeze > requirements.txt`    