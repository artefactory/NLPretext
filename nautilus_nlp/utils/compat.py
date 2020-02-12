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
from __future__ import print_function

import sys

is_python2 = int(sys.version[0]) == 2
is_windows = sys.platform.startswith("win")
is_linux = sys.platform.startswith("linux")
is_osx = sys.platform == "darwin"


import csv
import pickle
from builtins import zip as zip_
from urllib.parse import urljoin

range_ = range

bytes_ = bytes
unicode_ = str
string_types = (bytes, str)
int_types = (int,)
chr_ = chr

def unicode_to_bytes(s, encoding="utf8", errors="strict"):
    return s.encode(encoding=encoding, errors=errors)

def bytes_to_unicode(b, encoding="utf8", errors="strict"):
    return b.decode(encoding=encoding, errors=errors)
