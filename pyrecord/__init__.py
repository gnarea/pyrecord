from abc import ABCMeta

from pyrecord._validation.instance_validators import \
    require_existing_field_names
from pyrecord._validation.instance_validators import require_type_inheritance
from pyrecord._validation.type_validators import \
    require_default_value_correspondance_to_existing_field
from pyrecord._validation.type_validators import require_field_name_uniqueness
from pyrecord._validation.type_validators import require_field_name_validity
from pyrecord._validation.type_validators import require_type_name_validity
from pyrecord.exceptions import RecordInstanceError


__all__ = [
    "Record",
    ]


class Record(object):
    
    __metaclass__ = ABCMeta
    
    field_names = ()
    
    _default_values_by_field_name = {}
    
    def __init__(self, *values_by_field_order, **values_by_field_name):
        super(Record, self).__init__()
        
        self._validate_field_values(values_by_field_order, values_by_field_name)
        self._field_values = self._merge_field_values(
            values_by_field_order,
            values_by_field_name,
            )
    
    @classmethod
    def init_from_specialization(cls, specialized_record):
        require_type_inheritance(specialized_record.__class__, cls)
        
        field_values = specialized_record._get_selected_field_values(
            cls.field_names,
            )
        generalized_record = cls(**field_values)
        return generalized_record
    
    @classmethod
    def init_from_generalization(
        cls,
        generalized_record,
        **values_by_field_name
        ):
        generalized_record_type = generalized_record.__class__
        require_type_inheritance(cls, generalized_record_type)
        
        extra_specialization_field_names = set(cls.field_names) - \
            set(generalized_record_type.field_names)
        for field_name in values_by_field_name:
            if field_name not in extra_specialization_field_names:
                raise RecordInstanceError(
                    'Field "{}" is not specific to {}'.format(
                        field_name,
                        cls.__name__,
                        )
                    )
        
        generalized_record_field_values = generalized_record.get_field_values()
        values_by_field_name.update(generalized_record_field_values)
        
        specialized_record = cls(**values_by_field_name)
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
        if name in self.field_names:
            attribute_value = self._field_values[name]
        else:
            attribute_value = super(Record, self).__getattr__(name)
        return attribute_value
    
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
    def _validate_field_values(cls, values_by_field_order, values_by_field_name):
        unknown_field_values_count = \
            len(values_by_field_order) - len(cls.field_names)
        if 0 < unknown_field_values_count:
            raise RecordInstanceError(
                "Too many field values: Cannot map {} values to fields".format(
                    unknown_field_values_count,
                    )
                )
        
        require_existing_field_names(cls, values_by_field_name.keys())
        
        fields_set_by_position = cls.field_names[:len(values_by_field_order)]
        for field_name in values_by_field_name:
            if field_name in fields_set_by_position:
                raise RecordInstanceError(
                    'Value of field "{}" is already set'.format(field_name),
                    )
        
        fields_set = \
            fields_set_by_position + \
            tuple(values_by_field_name.keys()) + \
            tuple(cls._default_values_by_field_name.keys())
        for field_name in cls.field_names:
            if field_name not in fields_set:
                raise RecordInstanceError(
                    'Field "{}" is undefined'.format(field_name),
                    )
    
    @classmethod
    def _merge_field_values(cls, values_by_field_order, values_by_field_name):
        field_values = cls._default_values_by_field_name.copy()
        field_values.update(zip(cls.field_names, values_by_field_order))
        field_values.update(values_by_field_name)
        return field_values
    
    #{ Record type API
    
    @classmethod
    def create_type(
        cls,
        type_name,
        *field_names,
        **default_values_by_field_name
        ):
        
        cls._validate_type_definition(
            type_name,
            field_names,
            default_values_by_field_name,
            )
        
        record_type = cls._create_type(
            type_name,
            field_names,
            default_values_by_field_name,
            )
        return record_type
    
    @classmethod
    def _validate_type_definition(
        cls,
        type_name,
        field_names,
        default_values_by_field_name,
        ):
        require_type_name_validity(type_name)
        
        require_field_name_uniqueness(cls.field_names + field_names)
        require_field_name_validity(field_names)
        require_default_value_correspondance_to_existing_field(
            field_names,
            default_values_by_field_name,
            )
    
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
