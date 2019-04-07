# Text Processing

## Introduction & Best practice

## Encoding / Decoding

In our python programming lives,  pretty much everyone working with text data encountered one day the terrible:

    `UnicodeDecodeError: 'machine' codec can't decode character 'somethingsomething' in position x: ordinal not in range(z)`
And you probably spend the next hour trying to figure out to get out of this mess.

Usually, most of programming language automatically infer the encoding of the text. However, Python does not, and this can lead to a ton of problem.

Encoding is the table of representation between the binary code understood by the computer and the letters as we see them. Therefore, everytime you see text on a screen, it is encoded in a way.
The problem is, pretty much every country in the world had his own way of encoding and these encodings still persist: The encoding module of python can understand around 100 different encoding.

So, how do we get out of this mess?


### **The Absolute Rule:**
Use 'UTF-8' as default encoding for your processes.

### If you are still in Python2.7
*And you want to use it until its end of life(December 2019)*



### If you are in Python 3


## Stemmatization / Lemmatization

## Vector Representation

### Bag of Word & TF-IDF

### Word Embeddings
