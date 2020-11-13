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
import pandas as pd
import pytest
from nautilus_nlp.topic_modeling.biterm_model import BitermModel

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

NB_TOPICS = 5
NB_WORD_PER_CLUSTER = 5
NB_ITERATION = 100
LANGUAGE = 'english'


@pytest.mark.parametrize(
    "input_text, input_nb_topic , input_nb_iteration , input_language",
    [
        (TEXT, -1, NB_ITERATION, LANGUAGE),
        (TEXT, "Panzani", NB_ITERATION, LANGUAGE),
        (TEXT, 3.4, NB_ITERATION, LANGUAGE),
        (TEXT, (3, 5), NB_ITERATION, LANGUAGE),
        (TEXT, [3, 5], NB_ITERATION, LANGUAGE),
        (TEXT, NB_TOPICS, (2, 4), LANGUAGE),
        (TEXT, NB_TOPICS, [1, 3], LANGUAGE),
        (TEXT, NB_TOPICS, -1, LANGUAGE),
        (TEXT, NB_TOPICS, "Panzani", LANGUAGE),
        (TEXT, NB_TOPICS, 2.4, LANGUAGE),
        (3, NB_TOPICS, NB_ITERATION, LANGUAGE),
        ("Panzani", NB_TOPICS, NB_ITERATION, LANGUAGE),
        (("Panzani", "Rustichella"), NB_TOPICS, NB_ITERATION, LANGUAGE),
        ([], NB_TOPICS, NB_ITERATION, LANGUAGE),
        (["Panzani", "Rustichella", 3], NB_TOPICS, NB_ITERATION, LANGUAGE)
    ]
)
def text_input_parameter_error_handling(input_text
                                        , input_nb_topic
                                        , input_nb_iteration
                                        , input_language):
    with pytest.raises(TypeError):
        BitermModel(data=input_text, nb_topics=input_nb_topic, nb_iteration=input_nb_iteration, lang=input_language)


def test_number_topic_correct():
    biterm_model = BitermModel(data=TEXT
                               , nb_topics=NB_TOPICS
                               , nb_iteration=NB_ITERATION
                               , lang=LANGUAGE)
    clusters = biterm_model.compute_topics(nb_word_per_cluster=NB_WORD_PER_CLUSTER)
    assert len(pd.DataFrame(clusters)) == NB_TOPICS


def test_no_initialisation():
    with pytest.raises(ValueError):
        biter_model = BitermModel(data=TEXT,
                                  nb_topics=NB_TOPICS,
                                  nb_iteration=NB_ITERATION,
                                  lang=LANGUAGE)
        biter_model.get_document_topic(2)
