from pyrecord._validation.instance_validators import validate_generalization
from pyrecord._validation.instance_validators import validate_initialization
from pyrecord._validation.instance_validators import validate_field_access
from pyrecord._validation.instance_validators import validate_specialization
from pyrecord._validation.type_validators import validate_type_definition


__all__ = ["Record"]


class Record(object):
    
    field_names = ()
    
    _default_values_by_field_name = {}
    
    def __init__(self, *values_by_field_order, **values_by_field_name):
        validate_initialization(
            self.__class__,
            values_by_field_order,
            values_by_field_name,
            )
        
        super(Record, self).__init__()
        
        self._field_values = self._merge_field_values(
            values_by_field_order,
            values_by_field_name,
            )
    
    @classmethod
    def init_from_specialization(cls, specialized_record):
        validate_generalization(cls, specialized_record)
        
        field_values = specialized_record._get_selected_field_values(
            cls.field_names,
            )
        generalized_record = cls(**field_values)
        return generalized_record
    
    @classmethod
    def init_from_generalization(
        cls,
        generalized_record,
        **field_values
        ):
        validate_specialization(cls, generalized_record, field_values)
        
        generalized_record_field_values = generalized_record.get_field_values()
        field_values.update(generalized_record_field_values)
        specialized_record = cls(**field_values)
        return specialized_record
    
    def copy(self):
        record_type = self.__class__
        field_values = self.get_field_values()
        record_copy = record_type(**field_values)
        return record_copy
    
    def get_field_values(self):
        return self._get_selected_field_values(self.field_names)
    
    def _get_selected_field_values(self, selected_field_names):
        field_values = {}
        for field_name in selected_field_names:
            field_values[field_name] = self._field_values[field_name]
        return field_values
    
    def __getattr__(self, name):
        validate_field_access(name, self.__class__)
        
        field_value = self._field_values[name]
        return field_value
     
    def __setattr__(self, name, value):
        if name in self.field_names:
            self._field_values[name] = value
        else:
            super(Record, self).__setattr__(name, value)
    
    def __eq__(self, other):
        have_same_type = self.__class__ == other.__class__
        if have_same_type:
            are_equivalent = self._field_values == other._field_values
        else:
            are_equivalent = False
        return are_equivalent
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __repr__(self):
        field_assignments = []
        for field_name in self.field_names:
            field_value = self._field_values[field_name]
            field_assignment = "{}={}".format(field_name, repr(field_value))
            field_assignments.append(field_assignment)
        
        record_repr = "{record_type_name}({field_assignments})".format(
            record_type_name=self.__class__.__name__,
            field_assignments=", ".join(field_assignments),
            )
        return record_repr
    
    @classmethod
    def _merge_field_values(cls, values_by_field_order, values_by_field_name):
        field_values = cls._default_values_by_field_name.copy()
        field_values.update(zip(cls.field_names, values_by_field_order))
        field_values.update(values_by_field_name)
        return field_values
    
    #{ Record type API
    
    @staticmethod
    def create_type(type_name, *field_names, **default_values_by_field_name):
        record_type = Record.extend_type(
             type_name,
             *field_names,
             **default_values_by_field_name
             )
        return record_type
    
    @classmethod
    def extend_type(
        cls,
        subtype_name,
        *field_names,
        **default_values_by_field_name
        ):
        validate_type_definition(
            cls,
            subtype_name,
            field_names,
            default_values_by_field_name,
            )
        record_subtype = cls._create_type(
            subtype_name,
            field_names,
            default_values_by_field_name,
            )
        return record_subtype
    
    @classmethod
    def _create_type(cls, type_name, field_names, default_values_by_field_name):
        record_type = type(type_name, (cls, ), {})
        record_type.field_names = cls.field_names + field_names
        record_type._default_values_by_field_name = dict(
             cls._default_values_by_field_name,
             **default_values_by_field_name
             )
        return record_type
    
    #}
