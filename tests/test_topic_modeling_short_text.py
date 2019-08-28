import pytest
from nautilus_nlp.models.topic_modeling_short_text import prepare_data


def test_prepare_data():

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

    expected1 = [['1.5L', 4],['Coca-Cola', 3],['Cola', 4],['Light', 5],['Pepsi', 2],['bio', 3],['de', 2],['sans', 3]]
    expected2 = [['1.5L', 4], ['Coca-Cola', 3], ['Cola', 4], ['Light', 5], ['bio', 3], ['sans', 3]]
    _,_,output1 = prepare_data(text)
    _,_,output2 = prepare_data(text, vocab_min_count=2)

    assert output1 == expected1
    assert output2 == expected2
