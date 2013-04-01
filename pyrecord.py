__all__ = [
    "Record",
    "RecordInitializationError",
    "RecordException",
    ]


class Record(object):
    
    @classmethod
    def create_type(cls, type_name, *field_names, **default_values_by_field_name):
        raise NotImplementedError


#{ Exceptions


class RecordException(Exception):
    pass


class RecordInitializationError(RecordException):
    pass


#}
