Nautilus_NLP [![Build Status](https://travis-ci.com/artefactory/nautilus-nlp.svg?token=Ssg4shz5pz9qGnYCybSj&branch=master)](https://travis-ci.com/artefactory/nautilus-nlp)
==============================

The Nautilus NLP library aimed to be a meta-library to be used to help you get started on handling your NLP use-case.

This library can help you with:

    1. Cleaning text data
    2. Normalizing your dataset
    3. Training automatically multiclass, multilabel classifier
    4. Help you discover topics and cluster your data

You can find a list of the available features [in this article.](https://artefactory.atlassian.net/wiki/spaces/CK/pages/822837299/Nautilus+NLP+-+key+features)

# Feature Request

As an Artefact user, you might be working on a NLP use case, and wish to use Nautilus.

 However, if you think Nautilus is lacking features that can be useful not only to your use case but also others, feel free to to fill up an issue with the label "Feature-request".

 We will try to put it in the roadmap and implement it as soon as possible.

# Installation

Beware, this package has been tested on Python **3.6** & **3.7**, and will probably not be working under python **2.7** as **Python2.7** EOL is scheduled for December 2019. 

To install this library you should first clone the repository:

`git clone https://github.com/artefactory/nautilus_nlp/ && cd nautilus_nlp`

**If you don't use the docker container, we strongly advise you to do these steps in a virtual environnement**

First you need to install the required files:

```pip install -r requirements.txt```

then you can install it via pip:

```pip install -e .```

## Handling installation errors

### command 'gcc' failed with exit status 1

While runing `pip install -r requirements.txt` you might get the following error message:
```
command 'gcc' failed with exit status 1 
```

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

# Quick start 
### Install Mallet

1) Install Mallet file
run:

`bash nautilus_nlp/scripts/install_mallet.sh`

2) Install Java JDK (required to implement mallet)
run:

`bash nautilus_nlp/scripts/install_java.sh`

# Notebooks

The [notebook](notebooks/) folder contains various notebook on how to use this library.

Here is a quick example:

```

```

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    ├── tests              <- Where the tests lives
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so nautilus_nlp can be imported
    ├── nautilus_nlp                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes nautilus_nlp a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │
    │   ├── utils       <- Scripts to turn raw data into features for modeling
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.testrun.org
