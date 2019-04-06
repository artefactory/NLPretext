

Welcome to Nautilus_nlp's documentation!
========================================

The Nautilus NLP library aimed to be a meta-library to be used to help you get started on handling your NLP use-case.

This library can help you with:

    1. Cleaning text data
    2. Normalizing your dataset
    3. Training automatically multiclass, multilabel classifier
    4. Help you discover topics and cluster your data


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

`pip install -r requirements.txt`

then you can install it via pip:

`pip install -e .`


.. toctree::
   :maxdepth: 2
   :caption: Preprocessing and utility functions:

   modules

.. toctree::
   :maxdepth: 2
   :caption: Preprocessing and utility functions:

   nautilus_nlp.utils


.. toctree::
   :maxdepth: 2
   :caption: Machine learning:

   nautilus_nlp.models

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

