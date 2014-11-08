# Copyright 2013-2014, Gustavo Narea.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from os import path

from setuptools import find_packages
from setuptools import setup

_HERE = path.abspath(path.dirname(__file__))
_VERSION = open(path.join(_HERE, "VERSION.txt")).readline().rstrip()
_README = open(path.join(_HERE, "README.rst")).readline().strip()


setup(
    name="pyrecord",
    version=_VERSION,
    description="Pythonic Record Types",
    long_description=_README,
    packages=find_packages(),
    url="http://pythonhosted.org/pyrecord/",
    author="Gustavo Narea",
    author_email="me@gustavonarea.net",
    test_suite="nose.collector",
    )
