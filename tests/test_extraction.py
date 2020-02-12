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
