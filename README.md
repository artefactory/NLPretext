# NLPretext

<div align="center">

[![CI status](https://github.com/artefactory/NLPretext/actions/workflows/ci.yml/badge.svg?branch%3Amain&event%3Apush)](https://github.com/artefactory/NLPretext/actions/workflows/ci.yml?query=branch%3Amain)
[![CD status](https://github.com/artefactory/NLPretext/actions/workflows/cd.yml/badge.svg?event%3Arelease)](https://github.com/artefactory/NLPretext/actions/workflows/cd.yml?query=event%3Arelease)
[![Python Version](https://img.shields.io/badge/Python-3.7-informational.svg)](#supported-python-versions)
[![Dependencies Status](https://img.shields.io/badge/dependabots-active-informational.svg)](https://github.com/artefactory/NLPretext}/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-informational.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-informational?logo=pre-commit&logoColor=white)](https://github.com/artefactory/NLPretext}/blob/main/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%F0%9F%9A%80-semantic%20versions-informational.svg)](https://github.com/artefactory/NLPretext/releases)
[![Documentation](https://img.shields.io/badge/doc-sphinx-informational.svg)](https://github.com/artefactory/NLPretext}/tree/main/docs)
[![License](https://img.shields.io/badge/License-Apache%20Software%20License%202.0-informational.svg)](https://github.com/artefactory/NLPretext}/blob/main/LICENSE)

All the goto functions you need to handle NLP use-cases, integrated in NLPretext

</div>

## TL;DR

```bash
pip install git+ssh://git@github.com/artefactory/NLPretext.git@main
```

## Supported Python Versions

Main version supported : `3.7`

Other supported versions :


## Installation

### Public Package

Install the package from PyPi if it is publicly available :

```bash
pip install -U nlpretext
```

or with `Poetry`

```bash
poetry add nlpretext
```

### Private Package

Install the package from a private Github repository from the main branch:

```bash
pip install git+ssh://git@github.com/artefactory/NLPretext.git@main
```

Or from a known tag:

```bash
pip install git+ssh://git@github.com/artefactory/NLPretext.git@v0.1.0
```

Or from the latest Github Release using [personal access tokens](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token)

```bash
# Set the GITHUB_TOKEN environment variable to your personal access token
latest_release_tag=$(curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/repos/artefactory/NLPretext/releases/latest | jq -r ".tag_name")
pip install git+ssh://git@github.com/artefactory/NLPretext.git@${latest_release_tag}
```

## Usage

Once installed, you can run commands like :

```bash
nlpretext --help
```

```bash
nlpretext dialogs hello --name Roman
```

```bash
nlpretext dialogs clock --color blue
```

or if installed with `Poetry`:

```bash
poetry run nlpretext --help
```

```bash
poetry run nlpretext dialogs hello --name Roman
```

## Local setup

If you want to contribute to the development of this package, 

1. Clone the repository :

```bash
git clone git@github.com:artefactory/NLPretext.git
```

2. If you don't have `Poetry` installed, run:

```bash
make download-poetry; export PATH="$HOME/.poetry/bin:$PATH"
```

3. Initialize poetry and install `pre-commit` hooks:

```bash
make install
```

And you are ready to develop !

### Initial Github setting up

Can be automatically done directly after using the [`cookiecutter` template](https://github.com/artefactory/ppt) :

```bash
make github-install
```

Otherwise, see :- [Dependabot](https://docs.github.com/en/github/administering-a-repository/enabling-and-disabling-version-updates#enabling-github-dependabot-version-updates) to ensure you have the latest dependencies.
- [Stale bot](https://github.com/apps/stale) for automatic issue closing.
- [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) to deploy your documentation from the `gh-pages` branch.
- [GitHub Branch Protection](https://docs.github.com/en/github/administering-a-repository/about-protected-branches) to secure your `main` branch.

### Poetry

All manipulations with dependencies are executed through Poetry. If you're new to it, look through [the documentation](https://python-poetry.org/docs/).

<details>
<summary>Notes about Poetry commands</summary>
<p>

Here are some examples of Poetry [commands](https://python-poetry.org/docs/cli/#commands) :

- `poetry add numpy`
- `poetry run pytest`
- `poetry build`
- etc

</p>
</details>

### Building your package

Building a new version of the application contains steps:

- Bump the version of your package `poetry version <version>`. You can pass the new version explicitly, or a rule such as `major`, `minor`, or `patch`. For more details, refer to the [Semantic Versions](https://semver.org/) standard.
- Make a commit to `GitHub`.
- Create a `GitHub release`.
- And... publish  only if you want to make your package publicly available on PyPi 🙂 `poetry publish --build`

Packages:

- [`Typer`](https://github.com/tiangolo/typer) is great for creating CLI applications.
- [`Rich`](https://github.com/willmcgugan/rich) makes it easy to add beautiful formatting in the terminal.

## 🚀 Features

- Support for `Python 3.7`
- [`Poetry`](https://python-poetry.org/) as the dependencies manager. See configuration in [`pyproject.toml`](https://github.com/artefactory/NLPretext}/blob/main/pyproject.toml) and [`setup.cfg`](https://github.com/artefactory/NLPretext}/blob/main/setup.cfg).
- Power of [`black`](https://github.com/psf/black), [`isort`](https://github.com/timothycrosley/isort) and [`pyupgrade`](https://github.com/asottile/pyupgrade) formatters.
- Ready-to-use [`pre-commit`](https://pre-commit.com/) hooks with formatters above.
- Type checks with [`mypy`](https://mypy.readthedocs.io).
- Testing with [`pytest`](https://docs.pytest.org/en/latest/).
- Docstring checks with [`darglint`](https://github.com/terrencepreilly/darglint).
- Security checks with [`safety`](https://github.com/pyupio/safety), [`bandit`](https://github.com/PyCQA/bandit) and [`anchore`](https://github.com/anchore/scan-action).
- Secrets scanning with [`gitleaks`](https://github.com/zricethezav/gitleaks)
- Well-made [`.editorconfig`](https://github.com/artefactory/NLPretext}/blob/main/.editorconfig), [`.dockerignore`](https://github.com/artefactory/NLPretext}/blob/main/.dockerignore), and [`.gitignore`](https://github.com/artefactory/NLPretext}/blob/main/.gitignore). You don't have to worry about those things.

For building and deployment:

- `GitHub` integration.
- [`Makefile`](https://github.com/artefactory/NLPretext}/blob/main/Makefile#L89) for building routines. Everything is already set up for security checks, codestyle checks, code formatting, testing, linting, docker builds, etc. More details at [Makefile summary](#makefile-usage)).
- [Dockerfile](https://github.com/artefactory/NLPretext}/blob/main/docker/Dockerfile) for your package.
- `Github Actions` with predefined [build workflow](https://github.com/artefactory/NLPretext}/blob/main/.github/workflows/build.yml) as the default CI/CD.- `Github Pages` documentation built with Sphinx updated automatically when [releasing the package](https://github.com/artefactory/NLPretext}/blob/main/.github/workflows/cd.yml).
- `Github Packages` with Github Container Registry updated automatically when [releasing the package](https://github.com/artefactory/ppt/blob/main/%7B%7B%20cookiecutter.project_name.lower().replace('%20'%2C%20'_')%20%7D%7D/.github/workflows/cd.yml).- `Github Code Scanning` using [CodeQL]()- Always up-to-date dependencies with [`@dependabot`](https://dependabot.com/) (You will only need to [enable it](https://docs.github.com/en/github/administering-a-repository/enabling-and-disabling-version-updates#enabling-github-dependabot-version-updates)).
- Automatic drafts of new releases with [`Release Drafter`](https://github.com/marketplace/actions/release-drafter). It creates a list of changes based on labels in merged `Pull Requests`. You can see labels (aka `categories`) in [`release-drafter.yml`](https://github.com/artefactory/NLPretext}/blob/main/.github/release-drafter.yml). Works perfectly with [Semantic Versions](https://semver.org/) specification.

For creating your open source community:

- Ready-to-use [Pull Requests templates](https://github.com/artefactory/NLPretext}/blob/main/.github/PULL_REQUEST_TEMPLATE.md) and several [Issue templates](https://github.com/artefactory/NLPretext}/tree/main/.github/ISSUE_TEMPLATE).
- Files such as: `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and `SECURITY.md` are generated automatically.
- [`Stale bot`](https://github.com/apps/stale) that closes abandoned issues after a period of inactivity. (You will only [need to setup free plan](https://github.com/marketplace/stale)). Configuration is [here](https://github.com/artefactory/NLPretext}/blob/main/.github/.stale.yml).
- [Semantic Versions](https://semver.org/) specification with [`Release Drafter`](https://github.com/marketplace/actions/release-drafter).

### Makefile usage

[`Makefile`](https://github.com/artefactory/NLPretext}/blob/main/Makefile) contains many functions for fast assembling and convenient work.

<details>
<summary>1. Download Poetry</summary>
<p>

```bash
make download-poetry; export PATH="$HOME/.poetry/bin:$PATH"
```

</p>
</details>

<details>
<summary>2. Install all dependencies and pre-commit hooks</summary>
<p>

```bash
make install
```

If you do not want to install pre-commit hooks, run the command with the NO_PRE_COMMIT flag:

```bash
make install NO_PRE_COMMIT=1
```

</p>
</details>

<details>
<summary>3. Check the security of your code</summary>
<p>

```bash
make check-safety
```

This command launches a `Poetry` and `Pip` integrity check as well as identifies security issues with `Safety` and `Bandit`. By default, the build will crash if any of the items fail. But you can set `STRICT=0` for the entire build, and then you can configure strictness for each item separately.

```bash
make check-safety STRICT=0
```

or only for `safety`:

```bash
make check-safety STRICT=0 SAFETY_STRICT=1
```

multiple

```bash
make check-safety STRICT=0 PIP_STRICT=1 SAFETY_STRICT=1
```

> List of flags for `check-safety` (can be set to `1` or `0`): `STRICT`, `POETRY_STRICT`, `PIP_STRICT`, `SAFETY_STRICT`, `BANDIT_STRICT`.

</p>
</details>

<details>
<summary>4. Check the codestyle</summary>
<p>

The command is similar to `check-safety` but to check the code style, obviously. It uses `Black`, `Darglint`, `Isort`, and `Mypy` inside.

```bash
make check-style
```

It may also contain the `STRICT` flag.

```bash
make check-style STRICT=0
```

> List of flags for `check-style` (can be set to `1` or `0`): `STRICT`, `BLACK_STRICT`, `DARGLINT_STRICT`, `ISORT_STRICT`, `MYPY_STRICT`.

</p>
</details>

<details>
<summary>5. Run all the codestyle formatters</summary>
<p>

Codestyle uses `pre-commit` hooks, so ensure you've run `make install` before.

```bash
make format-code
```

</p>
</details>

<details>
<summary>6. Run tests</summary>
<p>

```bash
make test
```

</p>
</details>

<details>
<summary>7. Run all the linters</summary>
<p>

```bash
make lint
```

the same as:

```bash
make test && make check-safety && make check-style
```

> List of flags for `lint` (can be set to `1` or `0`): `STRICT`, `POETRY_STRICT`, `PIP_STRICT`, `SAFETY_STRICT`, `BANDIT_STRICT`, `BLACK_STRICT`, `DARGLINT_STRICT`, `PYUPGRADE_STRICT`, `ISORT_STRICT`, `MYPY_STRICT`.

</p>
</details>

<details>
<summary>8. Build docker</summary>
<p>

```bash
make docker
```

which is equivalent to:

```bash
make docker VERSION=latest
```

More information [here](https://github.com/artefactory/NLPretext}/tree/main/docker).

</p>
</details>

<details>
<summary>9. Cleanup docker</summary>
<p>

```bash
make clean_docker
```

or to remove all build

```bash
make clean
```

More information [here](https://github.com/artefactory/NLPretext}/tree/main/docker).

</p>
</details>


<details>
<summary>10. Activate virtualenv</summary>
<p>

```bash
poetry shell
```

To deactivate the virtual environment :

```bash
deactivate
```

</p>
</details>

## 📈 Releases

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

## Credits

This project was generated with [`ppt`](https://github.com/artefactory/ppt).


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
