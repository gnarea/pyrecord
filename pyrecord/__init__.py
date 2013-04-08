from abc import ABCMeta

from pyrecord._generic_utilities import get_duplicated_iterable_items
from pyrecord._generic_utilities import is_valid_python_identifier


__all__ = [
    "Record",
    "RecordInitializationError",
    "RecordException",
    "RecordTypeError",
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
        field_values = {
            field_name: getattr(specialized_record, field_name) for field_name in cls.field_names}
        return cls(**field_values)
    
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
    
    @classmethod
    def _validate_field_values(cls, field_values, values_by_field_name):
        unknown_field_values_count = len(field_values) - len(cls.field_names)
        if 0 < unknown_field_values_count:
            raise RecordInitializationError(
                "Too many field values: Cannot map {} values to fields".format(
                    unknown_field_values_count,
                    )
                )
        
        for field_name in values_by_field_name:
            if field_name not in cls.field_names:
                raise RecordInitializationError(
                    'Unknown field "{}"'.format(field_name),
                    )
        
        fields_set_by_position = cls.field_names[:len(field_values)]
        for field_name in values_by_field_name:
            if field_name in fields_set_by_position:
                raise RecordInitializationError(
                    'Value of field "{}" is already set'.format(field_name),
                    )
        
        fields_set = \
            fields_set_by_position + \
            tuple(values_by_field_name.keys()) + \
            tuple(cls._default_values_by_field_name.keys())
        for field_name in cls.field_names:
            if field_name not in fields_set:
                raise RecordInitializationError(
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
        _enforce_type_name_validity(type_name)
        
        _enforce_field_name_uniqueness(cls.field_names + field_names)
        _enforce_field_name_validity(field_names)
        _enforce_default_value_correspondance_to_existing_field(
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


#{ Exceptions


class RecordException(Exception):
    pass


class RecordTypeError(RecordException):
    pass


class RecordInitializationError(RecordException):
    pass


#{ Validators


def _enforce_type_name_validity(type_name):
    if not is_valid_python_identifier(type_name):
        raise RecordTypeError(
            "{} is not a valid identifier for a record type".format(
                repr(type_name),
                ),
            )


def _enforce_field_name_validity(field_names):
    for field_name in field_names:
        if not is_valid_python_identifier(field_name):
            raise RecordTypeError(
                "{} is not a valid field name".format(repr(field_name)),
                )


def _enforce_field_name_uniqueness(field_names):
    duplicated_field_names = get_duplicated_iterable_items(field_names)
    if duplicated_field_names:
        duplicated_field_names_as_string = ", ".join(duplicated_field_names)
        exception_message = "The following field names are duplicated: {}" \
            .format(duplicated_field_names_as_string)
        raise RecordTypeError(exception_message)


def _enforce_default_value_correspondance_to_existing_field(
    field_names,
    default_values_by_field_name
    ):
    for field_name in default_values_by_field_name:
        if field_name not in field_names:
            raise RecordTypeError('Unknown field "{}"'.format(field_name))


#}
