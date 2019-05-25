from flashtext import KeywordProcessor

def extract_keywords(text:str, keyword, case_sensitive=True) -> list:
    """
    Extract Keywords from a document.

    Parameters
    ----------
    text : str
        Text to extract keywords from
    keyword : str or list 
        Single keyword (str) or list of keywords (list)
    case_sensitive : bool
        If True, will be case-sensitive.

    Returns
    -------
    string
        return list of extracted keyworkds
    """
    processor=KeywordProcessor(case_sensitive=case_sensitive)
    if isinstance(keyword,list):
        processor.add_keywords_from_list(keyword)
    elif isinstance(keyword,str):
        processor.add_keyword(keyword)
    elif isinstance(keyword,dict):
        processor.add_keywords_from_dict(keyword)

    return processor.extract_keywords(text)
    
