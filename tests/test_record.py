from nose.plugins.skip import SkipTest
from nose.tools import assert_raises_regexp
from nose.tools import eq_
from nose.tools import ok_

from pyrecord import Record
from pyrecord import RecordInstanceError


Point = Record.create_type("Point", "coordinate_x", "coordinate_y")
Circle = Point.create_type("Circle", "radius")


class TestInitialization(object):
    
    def test_initialization(self):
        my_point = Point(1, 3)
        ok_(isinstance(my_point, Point))
        eq_(my_point.coordinate_x, 1)
        eq_(my_point.coordinate_y, 3)
    
    def test_initialization_by_name(self):
        my_point = Point(coordinate_x=1, coordinate_y=3)
        eq_(my_point.coordinate_x, 1)
        eq_(my_point.coordinate_y, 3)
    
    def test_subtype(self):
        my_circle = Circle(1, 3, 5)
        eq_(my_circle.coordinate_x, 1)
        eq_(my_circle.coordinate_y, 3)
        eq_(my_circle.radius, 5)
    
    def test_overriding_default_field_value(self):
        Point = Record.create_type("Point", "coordinate_x", coordinate_x=2)
        my_point = Point(1)
        eq_(my_point.coordinate_x, 1)
    
    def test_skipping_field_with_default_value(self):
        Point = Record.create_type("Point", "coordinate_x", coordinate_x=2)
        my_point = Point()
        eq_(my_point.coordinate_x, 2)
    
    def test_skipping_field_without_default_value(self):
        assert_raises_regexp(
            RecordInstanceError,
            '^Field "coordinate_x" is undefined$',
            Point,
            )
    
    def test_setting_unknown_field(self):
        # By position
        assert_raises_regexp(
            RecordInstanceError,
            "^Too many field values: Cannot map 2 values to fields$",
            Point,
            1,
            3,
            0,
            -1,
            )
        # By name
        assert_raises_regexp(
            RecordInstanceError,
            '^Unknown field "coordinate_z"$',
            Point,
            1,
            3,
            coordinate_z=0,
            )
    
    def test_field_value_set_multiple_times(self):
        assert_raises_regexp(
            RecordInstanceError,
            '^Value of field "coordinate_x" is already set$',
            Point,
            1,
            3,
            coordinate_x=2,
            )
    
    def test_copy(self):
        original_point = Point(1, 3)
        
        derived_point = original_point.copy()
        derived_point.coordinate_y = 5
        
        eq_(original_point.coordinate_x, derived_point.coordinate_x)
        eq_(3, original_point.coordinate_y)
        eq_(5, derived_point.coordinate_y)
    
    def test_generalization(self):
        my_circle = Circle(1, 3, 5)
        my_point = Point.init_from_specialization(my_circle)
        ok_(isinstance(my_point, Point))
        eq_(my_point.coordinate_x, my_circle.coordinate_x)
        eq_(my_point.coordinate_y, my_circle.coordinate_y)
    
    def test_invalid_generalization(self):
        my_point = Point(1, 3)
        assert_raises_regexp(
            RecordInstanceError,
            "^Record type Point is not a subtype of Circle$",
            Circle.init_from_specialization,
            my_point,
            )
    
    def test_specialization(self):
        my_point = Point(1, 3)
        my_circle = Circle.init_from_generalization(my_point, radius=5)
        ok_(isinstance(my_circle, Circle))
        eq_(my_circle.coordinate_x, my_point.coordinate_x)
        eq_(my_circle.coordinate_y, my_point.coordinate_y)
        eq_(my_circle.radius, 5)
    
    def test_invalid_specialization(self):
        my_circle = Circle(1, 3, 5)
        assert_raises_regexp(
            RecordInstanceError,
            "^Record type Point is not a subtype of Circle$",
            Point.init_from_generalization,
            my_circle,
            )
    
    def test_incomplete_specialization(self):
        my_point = Point(1, 3)
        assert_raises_regexp(
            RecordInstanceError,
            '^Field "radius" is undefined$',
            Circle.init_from_generalization,
            my_point,
            )
    
    def test_specialization_overriding_field_values(self):
        my_point = Point(1, 3)
        assert_raises_regexp(
            RecordInstanceError,
            '^Field "coordinate_y" is not specific to Circle$',
            Circle.init_from_generalization,
            my_point,
            radius=2,
            coordinate_y=5,
            )


class TestComparison(object):
    
    def test_same_type_and_same_field_values(self):
        raise SkipTest
    
    def test_same_type_and_different_field_values(self):
        raise SkipTest
    
    def test_specialization(self):
        raise SkipTest
    
    def test_copy(self):
        raise SkipTest


class TestFieldAccess(object):
    
    def test_getting_valid_field(self):
        raise SkipTest
    
    def test_getting_invalid_field(self):
        raise SkipTest
    
    def test_getting_valid_attribute_but_not_field(self):
        # e.g., __dict__
        raise SkipTest
    
    def test_getting_all_field_values(self):
        raise SkipTest
    
    def test_setting_valid_field(self):
        raise SkipTest
    
    def test_setting_invalid_field(self):
        raise SkipTest
    
    def test_deleting_field(self):
        raise SkipTest


def test_representation():
    raise SkipTest   # repr()
