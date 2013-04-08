__all__ = [
    "RecordException",
    "RecordInstanceError",
    "RecordTypeError",
    ]


class RecordException(Exception):
    pass


class RecordTypeError(RecordException):
    pass


class RecordInstanceError(RecordException):
    pass
