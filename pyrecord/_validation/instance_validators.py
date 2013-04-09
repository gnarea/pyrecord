from pyrecord.exceptions import RecordInstanceError


def require_type_inheritance(subtype, supertype):
    if not issubclass(subtype, supertype):
        raise RecordInstanceError(
            "Record type {} is not a subtype of {}".format(
                subtype.__name__,
                supertype.__name__,
                )
            )


def require_existing_field_names(record_type, field_names):
    for field_name in field_names:
        if field_name not in record_type.field_names:
            raise RecordInstanceError(
                'Unknown field "{}"'.format(field_name),
                )
