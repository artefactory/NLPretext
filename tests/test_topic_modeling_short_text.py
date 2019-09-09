from nautilus_nlp.models.topic_modeling_short_text import prepare_data, \
    __build_cooccurence_matrix, train_nmf_model, prepare_data_pyldavis, \
    show_dominant_topic, get_assigned_topics
import numpy as np

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


def test_prepare_data():

    expected1 = [['1.5L', 4],['Coca-Cola', 3],['Cola', 4],['Light', 5],['Pepsi', 2],['bio', 3],['de', 2],['sans', 3]]
    expected2 = [['1.5L', 4], ['Coca-Cola', 3], ['Cola', 4], ['Light', 5], ['bio', 3], ['sans', 3]]
    _,_,output1 = prepare_data(text)
    _,_,output2 = prepare_data(text, vocab_min_count=2)

    assert output1 == expected1
    assert output2 == expected2


def test_build_cooccurence_matrix():
    # The co-occurence matrix is an array with the list of vocab in rows and in columns
    # The weights denote the occurrences of a word i with a word j in same sentence for i != j and 0 elsewhere

    case_1 = [[1, 3, 3, 2, 2, 0], [1, 3], [3, 0, 0]]
    case_2 = [[0, 1, 2, 3, 4], [5, 6], [1]]

    mat_1 = __build_cooccurence_matrix(4, case_1)
    mat_2 = __build_cooccurence_matrix(7, case_2)

    expected_1 =np.array(
      [[0., 1., 2., 4.],
       [1., 0., 2., 3.],
       [2., 2., 0., 4.],
       [4., 3., 4., 0.]])


    expected_2 = np.array(
      [[0., 1., 1., 1., 1., 0., 0.],
       [1., 0., 1., 1., 1., 0., 0.],
       [1., 1., 0., 1., 1., 0., 0.],
       [1., 1., 1., 0., 1., 0., 0.],
       [1., 1., 1., 1., 0., 0., 0.],
       [0., 0., 0., 0., 0., 0., 1.],
       [0., 0., 0., 0., 0., 1., 0.]])

    assert np.array_equal(mat_1, expected_1)
    assert np.array_equal(mat_2, expected_2)


def test_show_dominant_topic():
    encoded_text_id, vocab_list, vocab_arr = prepare_data(text)
    n_topics = 3
    n_topKeyword = 2
    model = train_nmf_model(encoded_text_id, vocab_list, n_topics=n_topics)
    topics, pmi_score = show_dominant_topic(model, encoded_text_id, vocab_list, n_topKeyword = n_topKeyword)

    assert len(pmi_score) == n_topics
    assert len(topics) == n_topics
    for i in topics.values():
        assert len(i) == n_topKeyword


def test_get_assigned_topics():
    encoded_text_id, vocab_list, vocab_arr = prepare_data(text)
    n_topics = 3
    model = train_nmf_model(encoded_text_id, vocab_list, n_topics=n_topics)
    topics_list = get_assigned_topics(model)

    assert len(topics_list) == len(text)
    for topic_num in topics_list:
        assert topic_num<n_topics


def test_prepare_data_pyldavis():

    encoded_text_id, vocab_list, vocab_arr = prepare_data(text)
    n_topics = 3
    model = train_nmf_model(encoded_text_id, vocab_list, n_topics=n_topics)
    data = prepare_data_pyldavis(model, encoded_text_id, vocab_arr)
    phi= data['topic_term_dists']
    theta= data['doc_topic_dists']
    doc_length_values = data['doc_lengths']
    list_vocab=data['vocab']
    freq_vocab = data['term_frequency']

    assert phi.shape == (n_topics, len(list_vocab))
    assert theta.shape == (len(text), n_topics)
    assert len(doc_length_values) == len(text)
    assert len(list_vocab) == len(freq_vocab)


