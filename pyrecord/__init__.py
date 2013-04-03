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
    
    @abstractmethod
    def __init__(self):
        super(Record, self).__init__()
    
    @classmethod
    def create_type(cls, type_name, *field_names, **default_values_by_field_name):
        if not is_valid_python_identifier(type_name):
            raise RecordTypeError(
                "{} is not a valid identifier for a record type".format(
                    repr(type_name),
                    ),
                )
        
        all_field_names = list(field_names) + default_values_by_field_name.keys()
        
        for field_name in all_field_names:
            if not is_valid_python_identifier(field_name):
                raise RecordTypeError(
                    "{} is not a valid field name".format(repr(field_name)),
                    )
        
        duplicated_field_names = get_duplicated_iterable_items(all_field_names)
        if duplicated_field_names:
            duplicated_field_names_as_string = ", ".join(duplicated_field_names)
            exception_message = "The following field names are duplicated: {}" \
                .format(duplicated_field_names_as_string)
            raise RecordTypeError(exception_message)
        
        record_type = type(type_name, (cls, ), {})
        return record_type


#{ Exceptions


class RecordException(Exception):
    pass


class RecordTypeError(RecordException):
    pass


class RecordInitializationError(RecordException):
    pass


#}
