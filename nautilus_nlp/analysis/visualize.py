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
from collections import Counter

import matplotlib.pyplot as plt
import wordcloud

plt.rcParams["figure.figsize"] = [16, 9]


def make_word_cloud(text_or_counter, stop_words=None):
    if isinstance(text_or_counter, str):
        word_cloud = wordcloud.WordCloud(stopwords=stop_words).generate(text_or_counter)
    else:
        if stop_words is not None:
            text_or_counter = Counter(word for word in text_or_counter if word not in stop_words)
        word_cloud = wordcloud.WordCloud(stopwords=stop_words).generate_from_frequencies(text_or_counter)
    plt.imshow(word_cloud)
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
        if n_results is None:
            n_results = len(results)
        print('{} matches for "{}":'.format(len(results), query_word))
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
        print('No match for "{}"'.format(query_word))
