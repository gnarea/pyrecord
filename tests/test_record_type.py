from inspect import isabstract

from nose.tools import assert_not_equals
from nose.tools import assert_raises
from nose.tools import assert_raises_regexp
from nose.tools import eq_
from nose.tools import ok_

from pyrecord import Record
from pyrecord import RecordTypeError


def test_abstract():
    ok_(isabstract(Record))


def test_creation():
    Point = Record.create_type("Point", "coordinate_x", "coordinate_y")
    eq_("Point", Point.__name__)
    ok_(issubclass(Point, Record))
    assert_not_equals(Point, Record)


def test_subtype_creation():
    Point = Record.create_type("Point", "coordinate_x", "coordinate_y")
    Circle = Point.extend_type("Circle", "radius")
    eq_("Circle", Circle.__name__)
    ok_(issubclass(Circle, Point))
    assert_not_equals(Circle, Point)


def test_creation_with_ilegal_type_name():
    # Supertype
    assert_raises(RecordTypeError, Record.create_type, "Invalid-Name")
    
    # Subtype
    Point = Record.create_type("Point", "coordinate_x", "coordinate_y")
    assert_raises(RecordTypeError, Point.extend_type, "Invalid-Name")


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
    assert_raises(RecordTypeError, Point.extend_type, "Circle", "Invalid-Field")


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
    
    # Same field duplicated by position and name
    assert_raises_regexp(
        RecordTypeError,
        "^The following field names are duplicated: coordinate_x$",
        Record.create_type,
        "Point",
        "coordinate_x",
        coordinate_x=2,
        )
    
    # Multiple fields duplicated
    assert_raises_regexp(
        RecordTypeError,
        "^The following field names are duplicated: " \
            "coordinate_y, coordinate_x$",
        Record.create_type,
        "Point",
        "coordinate_x",
        "coordinate_y",
        coordinate_x=2,
        coordinate_y=2,
        )
    
    # Subtype
    Point = Record.create_type("Point", "coordinate_x", "coordinate_y")
    assert_raises_regexp(
        RecordTypeError,
        "^The following field names are duplicated: radius$",
        Point.extend_type,
        "Circle",
        "radius",
        "radius",
        )
    
    # Subtype redefining field
    Point = Record.create_type("Point", "coordinate_x", "coordinate_y")
    assert_raises_regexp(
        RecordTypeError,
        "^The following field names are duplicated: coordinate_x$",
        Point.extend_type,
        "Circle",
        "radius",
        "coordinate_x",
        )
