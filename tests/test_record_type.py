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

from nose.tools import assert_not_equals
from nose.tools import eq_
from nose.tools import ok_

from pyrecord import Record
from pyrecord.exceptions import RecordTypeError

from tests._utils import assert_raises_string


def test_creation():
    Point = Record.create_type("Point", "coordinate_x", "coordinate_y")
    eq_("Point", Point.__name__)
    ok_(issubclass(Point, Record))
    assert_not_equals(Point, Record)


def test_subtype_creation():
    Point = Record.create_type("Point", "coordinate_x", "coordinate_y")
    Point3D = Point.extend_type("Point3D", "coordinate_z")
    eq_("Point3D", Point3D.__name__)
    ok_(issubclass(Point3D, Point))
    assert_not_equals(Point3D, Point)


def test_creation_with_ilegal_type_name():
    # Supertype
    assert_raises_string(
        RecordTypeError,
        "'Invalid-Name' is not a valid identifier for a record type",
        Record.create_type,
        "Invalid-Name",
        )

    # Subtype
    Point = Record.create_type("Point", "coordinate_x", "coordinate_y")
    assert_raises_string(
        RecordTypeError,
        "'Invalid-Name' is not a valid identifier for a record type",
        Point.extend_type,
        "Invalid-Name",
        )


def test_creation_with_ilegal_field_name():
    # Supertype
    assert_raises_string(
        RecordTypeError,
        "'coordinate-x' is not a valid field name",
        Record.create_type,
        "Point",
        "coordinate-x",
        )

    # Subtype
    Point = Record.create_type("Point", "coordinate_x", "coordinate_y")
    assert_raises_string(
        RecordTypeError,
        "'Invalid-Field' is not a valid field name",
        Point.extend_type,
        "Point3D",
        "Invalid-Field",
        )


def test_creation_with_duplicated_field_names():
    # Same field duplicated by position
    assert_raises_string(
        RecordTypeError,
        "The following field names are duplicated: coordinate_x",
        Record.create_type,
        "Point",
        "coordinate_x",
        "coordinate_x",
        )

    # Multiple fields duplicated
    assert_raises_string(
        RecordTypeError,
        "The following field names are duplicated: coordinate_x, coordinate_y",
        Record.create_type,
        "Point",
        "coordinate_x",
        "coordinate_y",
        "coordinate_x",
        "coordinate_y",
        )

    # Subtype
    Point = Record.create_type("Point", "coordinate_x", "coordinate_y")
    assert_raises_string(
        RecordTypeError,
        "The following field names are duplicated: coordinate_z",
        Point.extend_type,
        "Point3D",
        "coordinate_z",
        "coordinate_z",
        )

    # Subtype redefining field in supertype
    Point = Record.create_type("Point", "coordinate_x", "coordinate_y")
    assert_raises_string(
        RecordTypeError,
        "The following field names are duplicated: coordinate_x",
        Point.extend_type,
        "Point3D",
        "coordinate_z",
        "coordinate_x",
        )


def test_getting_field_names():
    # Supertype
    Point = Record.create_type("Point", "coordinate_x", "coordinate_y")
    eq_(("coordinate_x", "coordinate_y"), Point.field_names)

    # Subtype
    Point3D = Point.extend_type("Point3D", "coordinate_z")
    eq_(("coordinate_x", "coordinate_y", "coordinate_z"), Point3D.field_names)


def test_default_value_for_undefined_field():
    # Supertype
    assert_raises_string(
        RecordTypeError,
        'Unknown field "weight"',
        Record.create_type,
        "Point",
        "coordinate_x",
        weight=3,
        )

    # Subtype
    Point = Record.create_type("Point", "coordinate_x", "coordinate_y")
    assert_raises_string(
        RecordTypeError,
        'Unknown field "weight"',
        Point.extend_type,
        "Point3D",
        "coordinate_z",
        weight=3,
        )


def test_module_name():
    # Supertype
    Point = Record.create_type("Point", "coordinate_x")
    eq_(__name__, Point.__module__)

    # Subtype
    Point3D = Point.extend_type("Point3D", "coordinate_z")
    eq_(__name__, Point3D.__module__)
