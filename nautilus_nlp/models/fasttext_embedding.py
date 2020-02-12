# GNU Lesser General Public License v3.0 only
# Copyright (C) 2020 Artefact
# licence-information@artefact.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
import fastText
import multiprocessing


class FasttextEmbedding(object):
    def __init__(self, path=None):
        try:
            self.model = fastText.load_model(path)
        except Exception as e:
            print(e)
            self.model = None

    def get_word_vector(self, word: str):
        """
        Return the wordvector of a word according to pretrained model

        Parameters
        ----------
        word : string
            the input document

        Returns
        -------
        array
        """

        return self.model.get_word_vector(word)

    def get_document_vector(self, document: str):
        """
        Return the wordvector of a full document according to pretrained model
        To build the vector,  each word-wordvector is divided by its norm, then the array of vector is averaged
        The document must be cleaned beforehand (no EOL)

        Parameters
        ----------
        Input document : string
            the input document

        Returns
        -------
        array
        """
        return self.model.get_sentence_vector(document)

    def train(
        self,
        input,
        model="skipgram",
        lr=0.05,
        dim=100,
        ws=5,
        epoch=5,
        minCount=5,
        minCountLabel=0,
        minn=3,
        maxn=6,
        neg=5,
        wordNgrams=1,
        loss="ns",
        bucket=2000000,
        thread=multiprocessing.cpu_count() - 1,
        lrUpdateRate=100,
        t=1e-4,
        label="__label__",
        verbose=2,
        pretrainedVectors="",
    ):
        """
        Train an unsupervised model and return a model object.
        input must be a filepath. The input text does not need to be tokenized
        as per the tokenize function, but it must be preprocessed and encoded
        as UTF-8. You might want to consult standard preprocessing scripts such
        as tokenizer.perl mentioned here: http://www.statmt.org/wmt07/baseline.html
        The input field must not contain any labels or use the specified label prefix
        unless it is ok for those words to be ignored. For an example consult the
        dataset pulled by the example script word-vector-example.sh, which is
        part of the fastText repository.
        """
        self.model.train_unsupervised(
            input=input,
            model=model,
            lr=lr,
            dim=dim,
            ws=ws,
            epoch=epoch,
            minCount=minCount,
            minCountLabel=minCountLabel,
            minn=minn,
            maxn=maxn,
            neg=neg,
            wordNgrams=wordNgrams,
            loss=loss,
            bucket=bucket,
            thread=thread,
            lrUpdateRate=lrUpdateRate,
            t=t,
            label=label,
            verbose=verbose,
            pretrainedVectors=pretrainedVectors,
        )
