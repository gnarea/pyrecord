from nose.tools import assert_not_equals
from nose.tools import assert_raises_regexp
from nose.tools import eq_
from nose.tools import ok_

from pyrecord import Record
from pyrecord.exceptions import RecordTypeError


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
    assert_raises_regexp(
        RecordTypeError,
        r"^'Invalid-Name' is not a valid identifier for a record type$",
        Record.create_type,
        "Invalid-Name",
        )
    
    # Subtype
    Point = Record.create_type("Point", "coordinate_x", "coordinate_y")
    assert_raises_regexp(
        RecordTypeError,
        r"^'Invalid-Name' is not a valid identifier for a record type$$",
        Point.extend_type,
        "Invalid-Name",
        )


def test_creation_with_ilegal_field_name():
    # Supertype
    assert_raises_regexp(
        RecordTypeError,
        r"^'coordinate-x' is not a valid field name$",
        Record.create_type,
        "Point",
        "coordinate-x",
        )
    
    # Subtype
    Point = Record.create_type("Point", "coordinate_x", "coordinate_y")
    assert_raises_regexp(
        RecordTypeError,
        r"^'Invalid-Field' is not a valid field name$",
        Point.extend_type,
        "Point3D",
        "Invalid-Field",
        )


def test_creation_with_duplicated_field_names():
    # Same field duplicated by position
    assert_raises_regexp(
        RecordTypeError,
        "^The following field names are duplicated: coordinate_x$",
        Record.create_type,
        "Point",
        "coordinate_x",
        "coordinate_x",
        )
    
    # Multiple fields duplicated
    assert_raises_regexp(
        RecordTypeError,
        "^The following field names are duplicated: " \
            "coordinate_x, coordinate_y$",
        Record.create_type,
        "Point",
        "coordinate_x",
        "coordinate_y",
        "coordinate_x",
        "coordinate_y",
        )
    
    # Subtype
    Point = Record.create_type("Point", "coordinate_x", "coordinate_y")
    assert_raises_regexp(
        RecordTypeError,
        "^The following field names are duplicated: coordinate_z$",
        Point.extend_type,
        "Point3D",
        "coordinate_z",
        "coordinate_z",
        )
    
    # Subtype redefining field in supertype
    Point = Record.create_type("Point", "coordinate_x", "coordinate_y")
    assert_raises_regexp(
        RecordTypeError,
        "^The following field names are duplicated: coordinate_x$",
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
    assert_raises_regexp(
        RecordTypeError,
        '^Unknown field "weight"$',
        Record.create_type,
        "Point",
        "coordinate_x",
        weight=3,
        )
    
    # Subtype
    Point = Record.create_type("Point", "coordinate_x", "coordinate_y")
    assert_raises_regexp(
        RecordTypeError,
        '^Unknown field "weight"$',
        Point.extend_type,
        "Point3D",
        "coordinate_z",
        weight=3,
        )
    
