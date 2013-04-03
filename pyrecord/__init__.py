from abc import ABCMeta
from abc import abstractmethod

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
    
    @abstractmethod
    def __init__(self):
        super(Record, self).__init__()
    
    @classmethod
    def create_type(cls, type_name, *field_names, **default_values_by_field_name):
        _enforce_type_name_validity(type_name)
        
        # Validate field names
        new_field_names = field_names + \
            tuple(default_values_by_field_name.keys())
        all_field_names = cls.field_names + new_field_names
        _enforce_field_name_uniqueness(all_field_names)
        _enforce_field_name_validity(new_field_names)
        
        # Create the record type
        record_type = type(type_name, (cls, ), {})
        record_type.field_names = all_field_names
        record_type._default_values_by_field_name = dict(
             cls._default_values_by_field_name,
             **default_values_by_field_name
             )
        return record_type


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


#}
