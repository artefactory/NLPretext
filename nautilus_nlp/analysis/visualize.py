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
from typing import List, Optional, Union
from collections import Counter

import matplotlib.pyplot as plt
import wordcloud
import warnings

plt.rcParams["figure.figsize"] = [16, 9]


def make_word_cloud(text_or_counter: Union[str, list], stop_words: Optional[List[str]] = None):
    '''
    Prints a word cloud from a text, or a word count. 

    Parameters
    ----------
    text_or_counter : Union[str, list]
        The text or the Counter to be ploted as wordcloud. 
        Example of counter: [('cat', 2), ('dog', 1)]
    stop_words: List[str], optional
        List of words to be ignored
    '''    
    if isinstance(text_or_counter, str):
        word_cloud = wordcloud.WordCloud(stopwords=stop_words).generate(text_or_counter)
    else:
        if stop_words is not None:
            text_or_counter = Counter(word for word in text_or_counter if word not in stop_words)
        word_cloud = wordcloud.WordCloud(stopwords=stop_words).generate_from_frequencies(text_or_counter)
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.show()


def print_concordance(
        tokens: List[str], query_word: str, width: int = 110, n_results: Optional[int] = None):
    '''
    Inputs a list of token and a query word, and print all the sentences that contains the query\
    word, display in a nice way. This function is an adaptation of NLTK's print_concordance\
    function. Source: http://www.nltk.org/_modules/nltk/text.html

    Parameters
    ----------
    tokens : list
        list of words
    query_word : str
        the word to be searched for in the list of tokens
    width : int
        Number of caracters to be display per text chunk
    n_results : int, optional
        If specified, will print only the N results
    '''
    half_width = (width - len(query_word) - 2) // 2
    context = width // 4  # approx number of words of context

    results = [i for i, j in enumerate(tokens) if j == query_word]
    nb_results = len(results)
    if nb_results > 0:
        if n_results is None:
            n_results = nb_results
        print(f'{nb_results} matches for "{query_word}":')
        for i in results[:n_results]:
            # Find the context of query word.
            left_context = tokens[max(0, i - context): i]
            right_context = tokens[i + 1: i + context]
            # Create the pretty lines with the query_word in the middle.
            left_print = ' '.join(left_context)[-half_width:]
            right_print = ' '.join(right_context)[:half_width]
            # The WYSIWYG line of the concordance.
            line_print = ' '.join([left_print, query_word, right_print])
            print(line_print)
    else:
        warnings.warn(f'No match for "{query_word}"')
