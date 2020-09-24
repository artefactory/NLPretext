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
from nautilus_nlp.topic_modeling.biterm_model import BitermModel
import pandas as pd
import pytest

text = ['Cola 1.5L Carrefour',
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

nb_topics = 5
nb_word_per_cluster = 5
nb_iteration = 100
language = 'english'


@pytest.mark.parametrize(
    "input_text, input_nb_topic , input_nb_iteration , input_language",
    [
        (text, -1, nb_iteration, language),
        (text, "Panzani", nb_iteration, language),
        (text, 3.4, nb_iteration, language),
        (text, (3, 5), nb_iteration, language),
        (text, [3, 5], nb_iteration, language),
        (text, nb_topics, (2, 4), language),
        (text, nb_topics, [1, 3], language),
        (text, nb_topics, -1, language),
        (text, nb_topics, "Panzani", language),
        (text, nb_topics, 2.4, language),
        (3, nb_topics, nb_iteration, language),
        ("Panzani", nb_topics, nb_iteration, language),
        (("Panzani", "Rustichella"), nb_topics, nb_iteration, language),
        ([], nb_topics, nb_iteration, language),
        (["Panzani", "Rustichella", 3], nb_topics, nb_iteration, language)
    ]
)
def text_input_parameter_error_handling(input_text
                                        , input_nb_topic
                                        , input_nb_iteration
                                        , input_language):
    with pytest.raises(ValueError):
        BitermModel(data=input_text, nb_topics=input_nb_topic, nb_iteration=input_nb_iteration, lang=input_language)


def test_number_topic_correct():
    biterm_model = BitermModel(data=text
                               , nb_topics=nb_topics
                               , nb_iteration=nb_iteration
                               , lang=language)
    clusters = biterm_model.compute_topics(nb_word_per_cluster=nb_word_per_cluster)
    assert len(pd.DataFrame(clusters)) == nb_topics


def test_no_initialisation():
    with pytest.raises(ValueError):
        biter_model = BitermModel(data=text
                                  , nb_topics=nb_topics
                                  , nb_iteration=nb_iteration,
                                  lang=language)
        biter_model.get_document_topic(2)
