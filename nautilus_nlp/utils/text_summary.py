from summa.summarizer import summarize


def is_list_of_strings(lst):
    """
    Parameters
    ----------    
    lst : list

    Returns
    -------
    book
        boolean indicator
    """      
    
    return bool(lst) and isinstance(lst, list) and all(isinstance(elem, str) for elem in lst)


def summarize_text(txt, ratio=0.2, words=None, language="english"):
    """
    Parameters
    ----------    
    txt : str
        Sting or list of strings containing text to summarize
    ratio : float
        Percentage giving the output text length in reference to the input length.
    words : 
        number of words of the output text
    language :
        text language. eg. "english"

    Returns
    -------
    string
        string containing the summarized text
    """      

    if is_list_of_strings(txt):
        txt = ' '.join(txt)
    elif isinstance(txt, str):
        pass
    else:
        raise ValueError("Text parameter must be a Unicode object (str) or list of str!")
    return summarize(txt, ratio, words, language)

