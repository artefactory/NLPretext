#!/bin/bash
wget -O wili.zip https://zenodo.org/record/841984/files/wili-2018.zip?download=1
mkdir -p wili && cp wili.zip wili && cd wili && unzip wili.zip && cd ..

