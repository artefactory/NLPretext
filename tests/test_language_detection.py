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
from nautilus_nlp.models import language_detector
import pytest
import numpy as np

model = language_detector.LangDetector()

TEXT_1 = """Кипрская война (итал. Guerra di Cipro; тур. Kıbrıs Savaşı) — одна из нескольких войн между Османской империей и Венецианской республикой за господство в Восточном Средиземноморье. Сначала Венеция воевала с османами одна. Затем, когда сформировалась Священная лига (в которую помимо Венеции входили Испания с Неаполем и Сицилией, Республика Генуя, Герцогство Савойское, госпитальеры, Великое герцогство Тосканское и другие итальянские государства), Османская империя воевала уже против Лиги."""
TEXT_2 = """
Wiborada († 1. Mai 926 in St. Gallen) war eine Einsied­lerin, geweihte Jung­frau und Märtyrin der katho­lischen Kirche. Sie lebte als Inklusin in St. Gallen und wurde wäh­rend eines Ungarn­einfalls getötet. Ihre letzte Ruhe­stätte, deren genaue Lage bei der Kirche St. Mangen heute nicht mehr be­kannt ist, war über Jahr­hunderte hinweg Ziel vieler Wall­fahrer. Sie wurde im Jahr 1047 von Papst Cle­mens II. heilig­gespro­chen und gilt als Schutz­patronin der Pfarr­haus­hälte­rinnen, Köchin­nen, Biblio­theken und Bücher­freunde. In der Ikono­grafie wird Wiborada im Habit darge­stellt; als ikono­grafische Heiligen­attri­bute sind ihr eine Helle­barde als Ver­weis auf das Marty­rium und ein Buch beige­geben."""
TEXT_3 = """De geschiedenis van het werelddeel Europa valt ruwweg chronologisch in te delen in de prehistorie, de klassieke oudheid, de middeleeuwen, de nieuwe tijd, de moderne tijd en de eigentijdse tijd."""
TEXT_4 = """
The absolute difference between At and Ft is divided by half the sum of absolute values of the actual value At and the forecast value Ft. The value of this calculation is summed for every fitted point t and divided again by the number of fitted points n.
"""
TEXT_5 = """Joseph Athanase Doumerc dit Paul Doumer est un homme d'État français né le 22 mars 1857 à Aurillac (Cantal) et mort assassiné le 7 mai 1932 à Paris. Il a été président de la République du 13 juin 1931 à sa mort."""
TEXT_6 = """1997年加延地震是于5月10日协调世界时7時57分发生在伊朗北部呼罗珊的一起重大地震，是该地区自1990年以来最大的一次地震，矩震级为7.3，中心位于马什哈德以南约270公里的一个名叫阿德库尔的乡村。这也是该国1997年所发生的第三场地震，造成严重的灾情，比尔詹德－加延地区变得满目疮痍，有1,567人丧生，超过2,300人受伤，5万人无家可归，超过15,000幢房屋遭到破坏或损毁，美国地质调查局形容这是1997年最致命的一场地震。其后还发生了约155次余震造成进一步的破坏并迫使幸存者离开。最终估计此次灾害的损失约为1亿美元。围绕地震震中的地区几乎全部被毁，这与乡村地区建筑质量不佳有很大关系，联合国建议调整相应建筑法规。按死亡人数计算，自进入20世纪以来，伊朗平均每3,000人就有1人在地震相关事件中遇难，一位美国地球物理学家建议为了解决持续的公共安全隐患，需要有一个全国范围的重建方案。"""


@pytest.mark.parametrize(
    "text, lang",
    [
        (TEXT_1, "ru"),
        (TEXT_2, "de"),
        (TEXT_3, "nl"),
        (TEXT_4, "en"),
        (TEXT_5, "fr"),
        (TEXT_6, "zh"),
    ],
)
def test_detect_language(text, lang):
    result = model.detect_language(text)[0]
    np.testing.assert_string_equal(result, lang)
