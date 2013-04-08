from inspect import isabstract

from nose.tools import assert_not_equals
from nose.tools import assert_raises
from nose.tools import assert_raises_regexp
from nose.tools import eq_
from nose.tools import ok_

from pyrecord import Record
from pyrecord.exceptions import RecordTypeError


def test_abstract():
    ok_(isabstract(Record))


def test_creation():
    Point = Record.create_type("Point", "coordinate_x", "coordinate_y")
    eq_("Point", Point.__name__)
    ok_(issubclass(Point, Record))
    assert_not_equals(Point, Record)


def test_subtype_creation():
    Point = Record.create_type("Point", "coordinate_x", "coordinate_y")
    Circle = Point.create_type("Circle", "radius")
    eq_("Circle", Circle.__name__)
    ok_(issubclass(Circle, Point))
    assert_not_equals(Circle, Point)


def test_creation_with_ilegal_type_name():
    # Supertype
    assert_raises(RecordTypeError, Record.create_type, "Invalid-Name")
    
    # Subtype
    Point = Record.create_type("Point", "coordinate_x", "coordinate_y")
    assert_raises(RecordTypeError, Point.create_type, "Invalid-Name")


def test_creation_with_ilegal_field_name():
    # Supertype
    assert_raises(
        RecordTypeError,
        Record.create_type,
        "Point",
        "coordinate-x",
        )
    
    # Subtype
    Point = Record.create_type("Point", "coordinate_x", "coordinate_y")
    assert_raises(RecordTypeError, Point.create_type, "Circle", "Invalid-Field")


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
        "^The following field names are duplicated: radius$",
        Point.create_type,
        "Circle",
        "radius",
        "radius",
        )
    
    # Subtype redefining field in supertype
    Point = Record.create_type("Point", "coordinate_x", "coordinate_y")
    assert_raises_regexp(
        RecordTypeError,
        "^The following field names are duplicated: coordinate_x$",
        Point.create_type,
        "Circle",
        "radius",
        "coordinate_x",
        )


def test_getting_field_names():
    # Supertype
    Point = Record.create_type("Point", "coordinate_x", "coordinate_y")
    eq_(("coordinate_x", "coordinate_y"), Point.field_names)
    
    # Subtype
    Circle = Point.create_type("Circle", "radius")
    eq_(("coordinate_x", "coordinate_y", "radius"), Circle.field_names)


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
        Point.create_type,
        "Circle",
        "radius",
        weight=3,
        )
    
