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
