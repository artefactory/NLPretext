from nautilus_nlp.models.biterm_model import BitermModel
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
