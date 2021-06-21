

Welcome to NLPretext's documentation!
========================================

The NLPretext library aimed to be a meta-library to be used to help you get started on handling your NLP use-case preprocessing.


# Installation

Beware, this package has been tested on Python **3.6** & **3.7** & **3.8**, and will probably not be working under python **2.7** as **Python2.7** EOL is scheduled for December 2019. 

To install this library you should first clone the repository:

pip install nlpretext

This library uses Spacy as tokenizer. Current models supported are `en_core_web_sm` and `fr_core_news_sm`. If not installed, run the following commands:

pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.3.1/en_core_web_sm-2.3.1.tar.gz

pip install https://github.com/explosion/spacy-models/releases/download/fr_core_news_sm-2.3.0/fr_core_news_sm-2.3.0.tar.gz



.. toctree::
   :maxdepth: 2
   :caption: Text Preprocessing Functions:

   modules

.. toctree::
   :maxdepth: 2
   :caption: Basic preprocessing:

   nlpretext.basic


.. toctree::
   :maxdepth: 2
   :caption: Social preprocessing:

   nlpretext.social

.. toctree::
   :maxdepth: 2
   :caption: Token preprocessing:

   nlpretext.token

.. toctree::
   :maxdepth: 2
   :caption: Text Augmentation:

   nlpretext.augmentation

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

