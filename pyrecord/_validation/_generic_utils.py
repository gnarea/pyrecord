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

import re


__all__ = [
    "get_duplicated_iterable_items",
    "is_valid_python_identifier",
    ]


_VALID_PYTHON_IDENTIFIER_RE = re.compile(r"^[a-z_]\w*$", re.IGNORECASE)


def get_duplicated_iterable_items(iterable):
    unique_items = []
    duplicated_items = []
    for item in iterable:
        if item in duplicated_items:
            continue
        
        if item in unique_items:
            duplicated_items.append(item)
        else:
            unique_items.append(item)
    
    return duplicated_items


def is_valid_python_identifier(identifier):
    """
    Report whether ``identifier`` is a valid string for an identifier in Python.
    
    The syntax for a valid Python identifier is officially described on the
    following URL:
    http://docs.python.org/2/reference/lexical_analysis.html#identifiers
    
    """
    is_valid = bool(_VALID_PYTHON_IDENTIFIER_RE.match(identifier))
    return is_valid
