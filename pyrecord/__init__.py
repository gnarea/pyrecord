from abc import ABCMeta

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
    
    def __init__(self, *field_values, **values_by_field_name):
        super(Record, self).__init__()
        
        self._validate_field_values(field_values, values_by_field_name)
        self._values_by_field_name = self._get_all_values_by_field_name(
            field_values,
            values_by_field_name,
            )
    
    @classmethod
    def init_from_specialization(cls, specialized_record):
        specialized_record_type = specialized_record.__class__
        require_type_inheritance(specialized_record_type, cls)
        
        values_by_field_name = {}
        for field_name in cls.field_names:
            values_by_field_name[field_name] = getattr(
                specialized_record,
                field_name,
                )
        generalized_record = cls(**values_by_field_name)
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
        
        for field_name in generalized_record.field_names:
            values_by_field_name[field_name] = getattr(
                generalized_record,
                field_name,
                )
        specialized_record = cls(**values_by_field_name)
        return specialized_record
    
    def copy(self):
        field_values = {field_name: getattr(self, field_name) for field_name in self.field_names}
        record_copy = self.__class__(**field_values)
        return record_copy
    
    def __getattr__(self, name):
        if name in self.field_names:
            attribute_value = self._values_by_field_name[name]
        else:
            attribute_value = super(Record, self).__getattr__(name)
        return attribute_value
    
    def __eq__(self, other):
        have_same_type = self.__class__ == other.__class__
        if have_same_type:
            are_equivalent = \
                self._values_by_field_name == other._values_by_field_name
        else:
            are_equivalent = False
        return are_equivalent
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    @classmethod
    def _validate_field_values(cls, field_values, values_by_field_name):
        unknown_field_values_count = len(field_values) - len(cls.field_names)
        if 0 < unknown_field_values_count:
            raise RecordInstanceError(
                "Too many field values: Cannot map {} values to fields".format(
                    unknown_field_values_count,
                    )
                )
        
        for field_name in values_by_field_name:
            if field_name not in cls.field_names:
                raise RecordInstanceError(
                    'Unknown field "{}"'.format(field_name),
                    )
        
        fields_set_by_position = cls.field_names[:len(field_values)]
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
    def _get_all_values_by_field_name(cls, field_values, values_by_field_name):
        all_values_by_field_name = cls._default_values_by_field_name.copy()
        all_values_by_field_name.update(values_by_field_name)
        
        for field_name, field_value in zip(cls.field_names, field_values):
            all_values_by_field_name[field_name] = field_value
        
        return all_values_by_field_name
    
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
