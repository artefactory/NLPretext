#!/bin/bash

echo 'Which Language do you want to use: en/fr?'
read lang
echo "Now downloading spacy models for language $lang"
python -m spacy download $lang
python -m spacy download xx

wget https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.$lang.300.bin.gz 
cp cc.$lang.300.bin.gz data/  && gunzip data/cc.$lang.300.bin.gz
