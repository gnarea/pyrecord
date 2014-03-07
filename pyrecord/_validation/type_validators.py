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

from pyrecord._validation._generic_utils import get_duplicated_iterable_items
from pyrecord._validation._generic_utils import is_valid_python_identifier
from pyrecord.exceptions import RecordTypeError


__all__ = [
    "validate_type_definition",
    ]


def validate_type_definition(
    supertype,
    type_name,
    field_names,
    default_values_by_field_name,
    ):
    _require_type_name_validity(type_name)
    
    _require_field_name_uniqueness(supertype.field_names + field_names)
    _require_field_name_validity(field_names)
    _require_default_value_correspondance_to_existing_field(
        field_names,
        default_values_by_field_name,
        )


def _require_type_name_validity(type_name):
    if not is_valid_python_identifier(type_name):
        raise RecordTypeError(
            "{} is not a valid identifier for a record type".format(
                repr(type_name),
                ),
            )


def _require_field_name_validity(field_names):
    for field_name in field_names:
        if not is_valid_python_identifier(field_name):
            raise RecordTypeError(
                "{} is not a valid field name".format(repr(field_name)),
                )


def _require_field_name_uniqueness(field_names):
    duplicated_field_names = get_duplicated_iterable_items(field_names)
    if duplicated_field_names:
        duplicated_field_names_as_string = ", ".join(duplicated_field_names)
        exception_message = "The following field names are duplicated: {}" \
            .format(duplicated_field_names_as_string)
        raise RecordTypeError(exception_message)


def _require_default_value_correspondance_to_existing_field(
    field_names,
    default_values_by_field_name
    ):
    for field_name in default_values_by_field_name:
        if field_name not in field_names:
            raise RecordTypeError('Unknown field "{}"'.format(field_name))
