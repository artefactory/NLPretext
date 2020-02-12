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
from nautilus_nlp.utils.text_summary import summarize_text

case1 = """Automatic summarization is the process of reducing a text document with a \
computer program in order to create a summary that retains the most important points \
of the original document. As the problem of information overload has grown, and as \
the quantity of data has increased, so has interest in automatic summarization. \
Technologies that can make a coherent summary take into account variables such as \
length, writing style and syntax. An example of the use of summarization technology \
is search engines such as Google. Document summarization is another."""

case2 = ["Automatic summarization is the process of reducing a text document with a " \
"computer program in order to create a summary that retains the most important points " \
"of the original document. ", "As the problem of information overload has grown, and as" \
"the quantity of data has increased, so has interest in automatic summarization. "\
"Technologies that can make a coherent summary take into account variables such as "\
"length, writing style and syntax." ,"An example of the use of summarization technology "\
"is search engines such as Google.", "Document summarization is another."]

result = """Automatic summarization is the process of reducing a text document with a computer \
program in order to create a summary that retains the most important points of the original document."""


def test_summarize_text():
    # Single string containing all text
    assert summarize_text(case1) == result
    # Text split in many sentences (list of strings)
    assert summarize_text(case2) == result
