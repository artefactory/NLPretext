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
import numpy as np
import pytest
from nautilus_nlp.topic_modeling.topic_modeling_short_text import (
    __build_cooccurence_matrix, get_assigned_topics, prepare_data,
    prepare_data_pyldavis, show_dominant_topic, train_shorttext_model)

TEXT = ['Cola 1.5L Carrefour',
        'Pepsi Cola Light 1.5L',
        'Pepsi Cola Twist Light',
        'Cola 1.5L CRF DISC',
        'Coca-Cola Light 1.5L',
        'Coca-Cola Light 4x0.5L',
        'Coca-Cola Light 6x0.3L',
        'Panzani 200g x 4 bio',
        'Rustichella 150g bio',
        'De Cecco - Fusilli bio',
        'Gerblé sans Gluten50g',
        'Penne de riz 100g sans gluten',
        'Spaghetti de maïs 50g sans Glute']


@pytest.mark.parametrize("input_text,  expected_output",
                         [(TEXT,
                           [['1.5L', 4],
                            ['Coca-Cola', 3],
                            ['Cola', 4],
                            ['Light', 5],
                            ['Pepsi', 2],
                            ['bio', 3],
                            ['de', 2],
                            ['sans', 3]]),
                          ([],
                           []),
                          (['', ''],
                           []), ],)
def test_prepare_data(input_text, expected_output):
    assert prepare_data(input_text), expected_output


@pytest.mark.parametrize("model_name", ['nmf', 'seanmf'])
@pytest.mark.parametrize("n_topics", [3, 0])
@pytest.mark.parametrize("n_keywords", [2, 0])
def test_show_dominant_topic(model_name, n_topics, n_keywords):

    encoded_text_id, vocab_list, _ = prepare_data(TEXT)

    model = train_shorttext_model(model_name, encoded_text_id, vocab_list, n_topics=n_topics)
    topics, pmi_score = show_dominant_topic(model, encoded_text_id, vocab_list, n_topKeyword=n_keywords)

    assert len(pmi_score) == n_topics
    assert len(topics) == n_topics
    for i in topics.values():
        assert len(i) == n_keywords


@pytest.mark.parametrize("model_name", ['nmf', 'seanmf'])
@pytest.mark.parametrize("n_topics", [3])
def test_get_assigned_topics(model_name, n_topics):
    encoded_text_id, vocab_list, _ = prepare_data(TEXT)
    model = train_shorttext_model(model_name, encoded_text_id, vocab_list, n_topics=n_topics)
    topics_list = get_assigned_topics(model)

    assert len(topics_list) == len(TEXT)
    for topic_num in topics_list:
        assert topic_num < n_topics


@pytest.mark.parametrize("model_name", ['nmf', 'seanmf'])
@pytest.mark.parametrize("n_topics", [0, 3])
def test_prepare_data_pyldavis(model_name, n_topics):
    encoded_text_id, vocab_list, vocab_arr = prepare_data(TEXT)
    model = train_shorttext_model(model_name, encoded_text_id, vocab_list, n_topics=n_topics)

    data = prepare_data_pyldavis(model, encoded_text_id, vocab_arr)
    phi = data['topic_term_dists']
    theta = data['doc_topic_dists']
    doc_length_values = data['doc_lengths']
    list_vocab = data['vocab']
    freq_vocab = data['term_frequency']

    assert phi.shape == (n_topics, len(list_vocab))
    assert theta.shape == (len(TEXT), n_topics)
    assert len(doc_length_values) == len(TEXT)
    assert len(list_vocab) == len(freq_vocab)


@pytest.mark.parametrize(
    "input_coded,  expected_output",
    [
        ([[1, 3, 3, 2, 2, 0], [1, 3], [3, 0, 0]],
         [[5., 1., 2., 4.],
          [1., 2., 2., 3.],
          [2., 2., 4., 4.],
          [4., 3., 4., 6.]]),

        ([[0, 1, 2, 3, 4], [5, 6], [1]],
         [[1., 1., 1., 1., 1., 0., 0.],
          [1., 2., 1., 1., 1., 0., 0.],
          [1., 1., 1., 1., 1., 0., 0.],
          [1., 1., 1., 1., 1., 0., 0.],
          [1., 1., 1., 1., 1., 0., 0.],
          [0., 0., 0., 0., 0., 1., 1.],
          [0., 0., 0., 0., 0., 1., 1.]]
         )
    ],
)
def test_build_cooccurence_matrix(input_coded, expected_output):
    # The co-occurence matrix is an array with the list of vocab in rows and in columns
    # The weights denote the occurrences of a word i with a word j in same sentence.

    flat_list = [item for sublist in input_coded for item in sublist]
    nb_vocab = len(set(flat_list))  # number of distinct words
    mat = __build_cooccurence_matrix(nb_vocab, input_coded)

    assert np.array_equal(mat, np.array(expected_output))
