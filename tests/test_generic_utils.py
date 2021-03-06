# Copyright 2013-2015, Gustavo Narea.
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

from nose.tools import assert_false
from nose.tools import eq_
from nose.tools import ok_

from pyrecord._validation._generic_utils import get_duplicated_iterable_items
from pyrecord._validation._generic_utils import is_valid_python_identifier


class TestDuplicatedIterableItems(object):

    def test_no_items(self):
        original_iterable = []
        duplicated_items = get_duplicated_iterable_items(original_iterable)
        eq_(0, len(duplicated_items))

    def test_unique_items(self):
        original_iterable = [1, 2, 3]
        duplicated_items = get_duplicated_iterable_items(original_iterable)
        eq_(0, len(duplicated_items))

    def test_one_duplicate(self):
        original_iterable = [1, 2, 2]
        duplicated_items = get_duplicated_iterable_items(original_iterable)
        eq_(1, len(duplicated_items))
        ok_(2 in duplicated_items)

    def test_two_duplicates_of_same_item(self):
        original_iterable = [1, 2, 2, 2]
        duplicated_items = get_duplicated_iterable_items(original_iterable)
        eq_(1, len(duplicated_items))
        ok_(2 in duplicated_items)

    def test_duplicates_of_various_items(self):
        original_iterable = [1, 1, 2, 2]
        duplicated_items = get_duplicated_iterable_items(original_iterable)
        eq_(2, len(duplicated_items))
        ok_(1 in duplicated_items)
        ok_(2 in duplicated_items)


class TestPythonIdentifierCheck(object):

    def test_valid_identifiers(self):
        valid_identifiers = (
            "_",
            "_var",
            "_3",
            "variable",
            "VARIABLE",
            "variable1",
            "variable_1",
            )
        for identifier in valid_identifiers:
            ok_(is_valid_python_identifier(identifier), identifier)

    def test_invalid_identifiers(self):
        invalid_identifiers = (
            "",
            "1variable",
            "variable-1",
            "variable.1",
            )
        for identifier in invalid_identifiers:
            assert_false(is_valid_python_identifier(identifier), identifier)
