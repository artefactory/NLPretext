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
from setuptools import find_packages, setup
import setuptools
import setuptools.command.install
from pathlib import Path

class PostInstallCommand(setuptools.command.install.install):
    """Post-installation command."""
    def run(self):
        setuptools.command.install.install.run(self)
        try:
            import spacy
            spacy.cli.validate()
        except ModuleNotFoundError:
            pass


with open(Path(__file__).resolve().parent.joinpath('VERSION'), 'r') as fh:
    version = fh.read()

setup(
    name='nautilus_nlp',
    packages=find_packages(),
    version=version,
    description='All the goto functions you need to handle NLP use-cases',
    author='Artefact',
    license='MIT',
    url='https://github.com/artefactory/nautilus-nlp',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    cmdclass={
        'install': PostInstallCommand,
    },
)
