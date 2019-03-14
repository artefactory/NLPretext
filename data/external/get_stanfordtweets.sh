#!/bin/bash 
wget -O trainingandtestdata.zip http://cs.stanford.edu/people/alecmgo/trainingandtestdata.zip trainingandtestdata.zip
mkdir -p  tweets_sentiment && cp trainingandtestdata.zip tweets_sentiment && cd tweets_sentiment && unzip trainingandtestdata.zip
