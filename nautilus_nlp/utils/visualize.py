'''
import matplotlib
import numpy as np

'''
import matplotlib.pyplot as plt
import wordcloud
plt.rcParams["figure.figsize"] = [16,9]


def make_word_cloud(text_or_counter, stop_words=[]):

    if type(text_or_counter) is str:
        myWordcloud = wordcloud.WordCloud(stopwords=stop_words).generate(text_or_counter)
    else:
        for w in stop_words:
            del text_or_counter[w]
        myWordcloud = wordcloud.WordCloud(stopwords=stop_words).generate_from_frequencies(text_or_counter)
    plt.imshow(myWordcloud)
    plt.axis("off")
    plt.show()


def print_concordance(tokens, query_word, width=110, n_results=None):
    '''
    Inputs a list of token and a query word, outputs all the sentences that 
    contains the query word, display in a nice way. 
    width = Integer. Number of caracters to display per text chunk
    n_results = Integer. If not null, filters the number of results displayed.
    This function is an adaptation of NLTK's print_concordance function. 
    Source: http://www.nltk.org/_modules/nltk/text.html
    '''
    half_width = (width - len(query_word) - 2) // 2
    context = width // 4  # approx number of words of context
    
    results = [i for i, j in enumerate(tokens) if j == query_word]
    if len(results) > 0:
        if n_results == None:
            n_results = len(results)
        print('{} matches for "{}":'.format(len(results),query_word)) 
        for i in results[:n_results]:
            
            # Find the context of query word.
            left_context = tokens[max(0, i - context) : i]
            right_context = tokens[i + 1 : i + context]
            # Create the pretty lines with the query_word in the middle.
            left_print = ' '.join(left_context)[-half_width:]
            right_print = ' '.join(right_context)[:half_width]
            # The WYSIWYG line of the concordance.
            line_print = ' '.join([left_print, query_word, right_print])
            before = tokens[:]
            print(line_print)
    else:
        print('No match for "{}"'.format(query_word))