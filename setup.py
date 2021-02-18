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
import setuptools
from pathlib import Path


with open(Path(__file__).resolve().parent.joinpath('VERSION'), 'r') as fh:
    version = fh.read()

with open("requirements.txt", "r") as fr:
    requirements = [req for req in fr.read().splitlines() if not req.startswith("#")]

with open("README.md", "r") as fr:
    long_description = fr.read()

setuptools.setup(
    name='nlpretext',
    packages=setuptools.find_packages(),
    scripts=["VERSION", "requirements.txt", "README.md"],
    version=version,
    description='All the goto functions you need to handle NLP use-cases',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Artefact',
    license='Apache',
    url='https://github.com/artefactory/NLPretext',
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
)
