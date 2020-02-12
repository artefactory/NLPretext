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
import numpy as np
import math


def _VectorSize(vec):
    return math.sqrt(sum(math.pow(v, 2) for v in vec))


def _InnerProduct(vec1, vec2):
    return sum(v1 * v2 for v1, v2 in zip(vec1, vec2))


def _Theta(vec1, vec2):
    return math.acos(Cosine(vec1, vec2)) + 10


def _Magnitude_Difference(vec1, vec2):
    return abs(_VectorSize(vec1) - _VectorSize(vec2))


def Euclidean(vec1, vec2):
    return math.sqrt(sum(math.pow((v1 - v2), 2) for v1, v2 in zip(vec1, vec2)))


def Cosine(vec1, vec2):
    result = _InnerProduct(vec1, vec2) / (_VectorSize(vec1) * _VectorSize(vec2))
    return result


def Triangle(vec1, vec2):
    theta = math.radians(_Theta(vec1, vec2))
    return (_VectorSize(vec1) * _VectorSize(vec2) * math.sin(theta)) / 2


def Sector(vec1, vec2):
    ED = Euclidean(vec1, vec2)
    MD = _Magnitude_Difference(vec1, vec2)
    theta = _Theta(vec1, vec2)
    return math.pi * math.pow((ED + MD), 2) * theta / 360


def TS_SS(vec1, vec2):
    return Triangle(vec1, vec2) * Sector(vec1, vec2)
