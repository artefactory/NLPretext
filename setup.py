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


with open(Path(__file__).resolve().parent.joinpath('requirements.txt'), 'r') as fh:
    requirements = [r.split('#', 1)[0].strip() for r in fh.read().split('\n')]
    print(requirements)
with open(Path(__file__).resolve().parent.joinpath('VERSION'), 'r') as fh:
    version = fh.read()

setup(
    name='nautilus_nlp',
    packages=find_packages(),
    version=version,
    description='All the goto functions you need to handle NLP use-cases',
    author='Robin Doumerc',
    license='MIT',
    url='https://github.com/artefactory/nautilus-nlp',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=requirements,
    cmdclass={
        'install': PostInstallCommand,
    },
)
