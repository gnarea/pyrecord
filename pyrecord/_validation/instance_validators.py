# Copyright 2013-2014, Gustavo Narea.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pyrecord.exceptions import RecordInstanceError


__all__ = [
    "validate_generalization",
    "validate_initialization",
    "validate_field_access",
    "validate_specialization",
    ]


def validate_initialization(
    record_type,
    values_by_field_order,
    values_by_field_name,
    ):
    _require_existing_fields_number(record_type, values_by_field_order)
    _require_existing_field_names(record_type, values_by_field_name.keys())
    _require_one_value_per_field(
        record_type,
        values_by_field_order,
        values_by_field_name,
        )


def validate_generalization(record_type, specialized_record):
    _require_type_inheritance(specialized_record.__class__, record_type)


def validate_specialization(record_type, generalized_record, field_values):
    generalized_record_type = generalized_record.__class__
    _require_type_inheritance(record_type, generalized_record_type)
    _require_field_names_missing_in_supertype(
        generalized_record_type,
        field_values,
        )


def validate_field_access(field_name, record_type):
    if field_name not in record_type.field_names:
        raise AttributeError(
            '"{}" has no field "{}"'.format(record_type.__name__, field_name),
            )


def _require_type_inheritance(subtype, supertype):
    if not issubclass(subtype, supertype):
        raise RecordInstanceError(
            "Record type {} is not a subtype of {}".format(
                subtype.__name__,
                supertype.__name__,
                )
            )


def _require_existing_field_names(record_type, field_names):
    for field_name in field_names:
        if field_name not in record_type.field_names:
            raise RecordInstanceError(
                'Unknown field "{}"'.format(field_name),
                )


def _require_existing_fields_number(record_type, values_by_field_order):
    unknown_field_values_count = \
        len(values_by_field_order) - len(record_type.field_names)
    if 0 < unknown_field_values_count:
        raise RecordInstanceError(
            "Too many field values: Cannot map {} values to fields".format(
                unknown_field_values_count,
                )
            )


def _require_one_value_per_field(
    record_type,
    values_by_field_order,
    values_by_field_name,
    ):
    fields_set_by_position = \
        record_type.field_names[:len(values_by_field_order)]
    
    # Check there's at most one value per field
    for field_name in values_by_field_name:
        if field_name in fields_set_by_position:
            raise RecordInstanceError(
                'Value of field "{}" is already set'.format(field_name),
                )
    
    # Check there's at least one value per field
    fields_set_by_name = values_by_field_name.keys()
    fields_with_default_value = record_type._default_values_by_field_name.keys()
    fields_set = \
        fields_set_by_position + \
        tuple(fields_set_by_name) + \
        tuple(fields_with_default_value)
    for field_name in record_type.field_names:
        if field_name not in fields_set:
            raise RecordInstanceError(
                'Field "{}" is undefined'.format(field_name),
                )


def _require_field_names_missing_in_supertype(supertype, subtype_field_names):
    for field_name in supertype.field_names:
        if field_name in subtype_field_names:
            raise RecordInstanceError(
                'Field "{}" is already defined in "{}"'.format(
                    field_name,
                    supertype.__name__,
                    )
                )
