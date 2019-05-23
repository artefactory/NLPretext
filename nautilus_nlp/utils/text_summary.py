from summa.summarizer import summarize


def is_list_of_strings(lst):
    """
    :param lst: list
    :return: boolean indicator
    """
    return bool(lst) and isinstance(lst, list) and all(isinstance(elem, str) for elem in lst)


def summarize_text(txt, ratio=0.2, words=None, language="english"):
    """
    :param txt: Sting or list of strings containing text to summarize
    :param ratio: Percentage giving the output text length in reference to the input length.
    :param words: number of words of the output text
    :param language: text language
    :return: string containing the summarized text
    """

    if is_list_of_strings(txt):
        txt = ' '.join(txt)
    elif isinstance(txt, str):
        pass
    else:
        raise ValueError("Text parameter must be a Unicode object (str) or list of str!")
    return summarize(txt, ratio, words, language)

