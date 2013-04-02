from abc import ABCMeta
from abc import abstractmethod


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
        all_field_names = list(field_names) + default_values_by_field_name.keys()
        duplicated_field_names = _get_duplicated_iterable_items(all_field_names)
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


#{ Utilities


def _get_duplicated_iterable_items(iterable):
    iterable_with_unique_items = []
    iterable_with_duplicated_items = []
    for item in iterable:
        if item in iterable_with_unique_items:
            iterable_with_duplicated_items.append(item)
        else:
            iterable_with_unique_items.append(item)
    return iterable_with_duplicated_items


#}
