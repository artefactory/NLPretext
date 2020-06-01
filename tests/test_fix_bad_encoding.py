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

import pytest
import numpy as np
from nautilus_nlp.preprocessing.text_preprocess import TextPreprocessor



@pytest.mark.parametrize(
    "input_str, expected_str",
    [
    ('Les augmentations de rÃ©munÃ©rations',
  'Les augmentations de rémunérations'),
 ("rÃ©nover l'enquÃªte publique pour en faire un vrai outil  d'amÃ©nagement du territoire et de dialogue social",
  "rénover l'enquête publique pour en faire un vrai outil  d'aménagement du territoire et de dialogue social"),
 ('Limitations de vitesse et sÃ©curitÃ© routiÃ¨re',
  'Limitations de vitesse et sécurité routière'),
 ('Pour un nouveau contrat citoyen', 'Pour un nouveau contrat citoyen'),
 ('DÃ©velopper les dÃ©marches de budget participatif dans les collectivitÃ©s et associer les citoyens dans la rÃ©alisation des projets',
  'Développer les démarches de budget participatif dans les collectivités et associer les citoyens dans la réalisation des projets'),
 ('proportienelle', 'proportienelle'),
 ('Pour plus de dÃ©mocratie participative',
  'Pour plus de démocratie participative'),
 ('Transparence de la vie public', 'Transparence de la vie public'),
 ('18 mois de trop....ca suffit macron',
  '18 mois de trop....ca suffit macron'),
 ('EgalitÃ© devant les infractions routiÃ¨res',
  'Egalité devant les infractions routières')
    ],
)
def test_remove_multiple_spaces_and_strip_text(input_str, expected_str):
    preprocessor = TextPreprocessor(input_str)
    result = preprocessor.fix_bad_unicode()
    np.testing.assert_string_equal(result, expected_str)
