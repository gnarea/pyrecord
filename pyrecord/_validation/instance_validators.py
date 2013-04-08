from pyrecord.exceptions import RecordInstanceError


def require_type_inheritance(subtype, supertype):
    if not issubclass(subtype, supertype):
        raise RecordInstanceError(
            "Record type {} is not a subtype of {}".format(
                subtype.__name__,
                supertype.__name__,
                )
            )
