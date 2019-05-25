from nautilus_nlp.preprocessing.keyword_extractor import extract_keywords

str_="""Les moteurs de recherche tels Google, Exalead ou Yahoo! sont
 des applications très connues de fouille de textes sur de grandes masses de données. 
 Cependant, les moteurs de recherche ne se basent pas uniquement sur le texte pour l'indexer, mais également sur la façon 
 dont les pages sont mises en valeur les unes par rapport aux autres. L'algorithme utilisé par Google est PageRank, et il est courant de voir HITS 
 dans le milieu académique"""

dict_extract={"US_Companies":['Yahoo','Google'],
 "French_Companies":['Exalead']
}
def test_keyword_extraction():
    assert extract_keywords(str_,['Google'])==['Google','Google']
    assert extract_keywords(str_,'Google')==['Google','Google']
    assert extract_keywords(str_,['Google','Yahoo'])==['Google','Yahoo','Google']
    assert extract_keywords(str_,dict_extract) == ['US_Companies', 'French_Companies', 'US_Companies', 'US_Companies']
