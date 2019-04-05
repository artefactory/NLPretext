from flashtext import KeywordProcessor

def extract_keywords(text,keyword,case_sensitive=True):
    """
    Extract Keywords from a document.
    args :
    text: Text to extract keywords from
    keyword : Single keyword (str) or list of keywords (list)

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
    
