from nose.tools import assert_false
from nose.tools import assert_not_in
from nose.tools import assert_raises_regexp
from nose.tools import eq_
from nose.tools import ok_

from pyrecord import Record
from pyrecord.exceptions import RecordInstanceError


Point = Record.create_type("Point", "coordinate_x", "coordinate_y")
Point3D = Point.extend_type("Point3D", "coordinate_z")


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
        my_point_3d = Point3D(1, 3, 5)
        eq_(my_point_3d.coordinate_x, 1)
        eq_(my_point_3d.coordinate_y, 3)
        eq_(my_point_3d.coordinate_z, 5)
    
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
        my_point_3d = Point3D(1, 3, 5)
        my_point = Point.init_from_specialization(my_point_3d)
        ok_(isinstance(my_point, Point))
        eq_(my_point.coordinate_x, my_point_3d.coordinate_x)
        eq_(my_point.coordinate_y, my_point_3d.coordinate_y)
    
    def test_invalid_generalization(self):
        my_point = Point(1, 3)
        assert_raises_regexp(
            RecordInstanceError,
            "^Record type Point is not a subtype of Point3D$",
            Point3D.init_from_specialization,
            my_point,
            )
    
    def test_specialization(self):
        my_point = Point(1, 3)
        my_point_3d = Point3D.init_from_generalization(my_point, coordinate_z=5)
        ok_(isinstance(my_point_3d, Point3D))
        eq_(my_point_3d.coordinate_x, my_point.coordinate_x)
        eq_(my_point_3d.coordinate_y, my_point.coordinate_y)
        eq_(my_point_3d.coordinate_z, 5)
    
    def test_invalid_specialization(self):
        my_point_3d = Point3D(1, 3, 5)
        assert_raises_regexp(
            RecordInstanceError,
            "^Record type Point is not a subtype of Point3D$",
            Point.init_from_generalization,
            my_point_3d,
            )
    
    def test_incomplete_specialization(self):
        my_point = Point(1, 3)
        assert_raises_regexp(
            RecordInstanceError,
            '^Field "coordinate_z" is undefined$',
            Point3D.init_from_generalization,
            my_point,
            )
    
    def test_specialization_overriding_field_values(self):
        my_point = Point(1, 3)
        assert_raises_regexp(
            RecordInstanceError,
            '^Field "coordinate_y" is already defined in "Point"$',
            Point3D.init_from_generalization,
            my_point,
            coordinate_z=2,
            coordinate_y=5,
            )


class TestComparison(object):
    
    def test_same_type_and_same_field_values(self):
        point1 = Point(1, 3)
        point2 = Point(1, 3)
        self.assert_equals(point1, point2)
    
    def test_same_type_and_different_field_values(self):
        point1 = Point(2, 4)
        point2 = Point(6, 8)
        self.assert_not_equals(point1, point2)
    
    def test_different_type_and_same_field_values(self):
        point = Point(2, 4)
        
        AlternativePoint = Record.create_type(
            "AlternativePoint",
            "coordinate_x",
            "coordinate_y",
            )
        alternative_point = AlternativePoint(2, 4)
        
        self.assert_not_equals(point, alternative_point)
    
    def test_specialization(self):
        point = Point(2, 4)
        point_3d = Point3D(2, 4, 8)
        self.assert_not_equals(point, point_3d)
    
    def test_non_record(self):
        point = Point(1, 3)
        self.assert_not_equals(point, object())
    
    #{ Check equality in all possible ways
    
    # In Python, "a == b = True" DOESN'T necessarily mean that "a != b = False"
    # nor "b == a = True".
    
    @staticmethod
    def assert_equals(item1, item2):
        ok_(item1 == item2)
        ok_(item2 == item1)
        assert_false(item1 != item2)
        assert_false(item2 != item1)
    
    @staticmethod
    def assert_not_equals(item1, item2):
        ok_(item1 != item2)
        ok_(item2 != item1)
        assert_false(item1 == item2)
        assert_false(item2 == item1)
    
    #}


class TestFieldAccess(object):
    
    def test_getting_valid_field(self):
        point = Point(1, 3)
        eq_(1, point.coordinate_x)
    
    def test_getting_invalid_field(self):
        point = Point(1, 3)
        assert_raises_regexp(
            AttributeError,
            '^"Point" has no field "coordinate_z"$',
            getattr,
            point,
            "coordinate_z",
            )
    
    def test_getting_all_field_values(self):
        point = Point(1, 3)
        expected_values = {'coordinate_x': 1, 'coordinate_y': 3}
        actual_values = point.get_field_values()
        eq_(expected_values, actual_values)
        
        actual_values['coordinate_x'] = 7
        eq_(1, point.coordinate_x, "The field values must've been copied")
    
    def test_setting_valid_field(self):
        point = Point(1, 3)
        point.coordinate_x = 5
        
        # Ensure it wasn't just set on __dict__
        field_values = point.get_field_values()
        eq_(5, field_values['coordinate_x'])
    
    def test_setting_invalid_field(self):
        point = Point(1, 3)
        point.coordinate_z = 5
        
        # Ensure it wasn't set on __dict__
        field_values = point.get_field_values()
        assert_not_in("coordinate_z", field_values)


def test_representation():
    point_3d = Point3D(1, 3, "20")
    expected_repr = "Point3D(coordinate_x=1, coordinate_y=3, coordinate_z='20')"
    eq_(expected_repr, repr(point_3d))
