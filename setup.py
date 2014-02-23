from os import path

from setuptools import find_packages
from setuptools import setup

HERE = path.abspath(path.dirname(__file__))
VERSION = open(path.join(HERE, "VERSION.txt")).readline().rstrip()

setup(
    name="pyrecord",
    version=VERSION,
    packages=find_packages(),
    url="https://pypi.python.org/pypi/pyrecord",
    author="Gustavo Narea",
    author_email="me@gustavonarea.net",
    )
