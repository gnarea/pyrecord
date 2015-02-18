# Copyright 2013-2015, Gustavo Narea.
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

from sys import _getframe as get_frame_from_call_stack

from pyrecord._validation.instance_validators import validate_field_access
from pyrecord._validation.instance_validators import validate_generalization
from pyrecord._validation.instance_validators import validate_initialization
from pyrecord._validation.instance_validators import validate_specialization
from pyrecord._validation.type_validators import validate_type_definition


__all__ = ["Record"]


class Record(object):
    """
    Base class for record types.

    .. versionchanged:: 1.0rc2
        Class attribute ``__module__`` is set to the name of the module
        creating the record type, making it possible to pickle records.

    """

    field_names = ()
    """
    Ordered collection of field names in the current record type.

    This is populated by :meth:`create_type` and :meth:`extend_type`.

    """

    _default_values_by_field_name = {}

    def __init__(self, *values_by_field_order, **values_by_field_name):
        """

        :raises pyrecord.exceptions.RecordInstanceError: If too few or too
            many arguments are passed, or unknown field names are referenced.

        Field values can be passed by position, name or both. When passed by
        position, the order of the fields in the current record type is used.

        """
        validate_initialization(
            self.__class__,
            values_by_field_order,
            values_by_field_name,
            )

        super(Record, self).__init__()

        self._field_values = self._merge_field_values(
            values_by_field_order,
            values_by_field_name,
            )

    @classmethod
    def init_from_specialization(cls, specialized_record):
        """
        Generalize ``specialized_record`` to an instance of the current
        record type.

        :raises pyrecord.exceptions.RecordInstanceError: If
            ``specialized_record`` is not a specialization of the current type.

        """
        validate_generalization(cls, specialized_record)

        field_values = specialized_record._get_selected_field_values(
            cls.field_names,
            )
        generalized_record = cls(**field_values)
        return generalized_record

    @classmethod
    def init_from_generalization(
        cls,
        generalized_record,
        **field_values
        ):
        """
        Specialize ``generalized_record`` to an instance of the current
        record type.

        :raises pyrecord.exceptions.RecordInstanceError: If
            ``generalized_record`` is not a generalization of the current type
            or ``field_values`` is incomplete.

        Values for any fields specific to the specialization must be passed by
        name.

        """
        validate_specialization(cls, generalized_record, field_values)

        generalized_record_field_values = generalized_record.get_field_values()
        field_values.update(generalized_record_field_values)
        specialized_record = cls(**field_values)
        return specialized_record

    def copy(self):
        """
        Return a shallow copy of the current record.

        :rtype: :class:`Record`

        """
        record_type = self.__class__
        field_values = self.get_field_values()
        record_copy = record_type(**field_values)
        return record_copy

    def get_field_values(self):
        """
        Return the current field values by name.

        :rtype: :class:`dict`

        """
        return self._get_selected_field_values(self.field_names)

    def _get_selected_field_values(self, selected_field_names):
        field_values = {}
        for field_name in selected_field_names:
            field_values[field_name] = self._field_values[field_name]
        return field_values

    def __getattr__(self, name):
        validate_field_access(name, self.__class__)

        field_value = self._field_values[name]
        return field_value

    def __setattr__(self, name, value):
        if name in self.field_names:
            self._field_values[name] = value
        else:
            super(Record, self).__setattr__(name, value)

    def __eq__(self, other):
        have_same_type = self.__class__ == other.__class__
        if have_same_type:
            are_equivalent = self._field_values == other._field_values
        else:
            are_equivalent = False
        return are_equivalent

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        field_assignments = []
        for field_name in self.field_names:
            field_value = self._field_values[field_name]
            field_assignment = "{}={}".format(field_name, repr(field_value))
            field_assignments.append(field_assignment)

        record_repr = "{record_type_name}({field_assignments})".format(
            record_type_name=self.__class__.__name__,
            field_assignments=", ".join(field_assignments),
            )
        return record_repr

    @classmethod
    def _merge_field_values(cls, values_by_field_order, values_by_field_name):
        field_values = cls._default_values_by_field_name.copy()
        field_values.update(zip(cls.field_names, values_by_field_order))
        field_values.update(values_by_field_name)
        return field_values

    #{ Record type API

    @staticmethod
    def create_type(type_name, *field_names, **default_values_by_field_name):
        """
        Return a new record type of name ``type_name``.

        :param str type_name: The name of the new record type.
        :raises pyrecord.exceptions.RecordTypeError: If ``type_name`` or some
            ``field_names`` are not valid Python identifiers, some
            ``field_names`` are duplicated or ``default_values_by_field_name``
            refers to an unknown field name.
        :rtype: A sub-class of :class:`Record`

        All the field names must be passed by position. Any default values
        for them must be passed by name.

        """
        record_type = Record.extend_type(
             type_name,
             *field_names,
             **default_values_by_field_name
             )
        return record_type

    @classmethod
    def extend_type(
        cls,
        subtype_name,
        *field_names,
        **default_values_by_field_name
        ):
        """
        Return a new sub-type of name ``type_name`` for the current record type.

        :param str subtype_name: The name of the new record sub-type.
        :raises pyrecord.exceptions.RecordTypeError: If ``subtype_name`` or some
            ``field_names`` are not valid Python identifiers, some
            ``field_names`` are duplicated, some ``field_names`` clash with
            fields in a super-type or ``default_values_by_field_name``
            refers to an unknown field name.
        :rtype: A sub-class of the current class

        All the field names must be passed by position. Any default values
        for them must be passed by name.

        """
        validate_type_definition(
            cls,
            subtype_name,
            field_names,
            default_values_by_field_name,
            )
        record_subtype = cls._create_type(
            subtype_name,
            field_names,
            default_values_by_field_name,
            )
        return record_subtype

    @classmethod
    def _create_type(cls, type_name, field_names, default_values_by_field_name):
        record_type = type(type_name, (cls,), {})
        record_type.field_names = cls.field_names + field_names
        record_type._default_values_by_field_name = dict(
             cls._default_values_by_field_name,
             **default_values_by_field_name
             )

        # Make instances pickable
        record_type.__module__ = _get_client_module_name()

        return record_type

    #}


def _get_client_module_name():
    client_module_name = None
    for stack_index in range(1, 5):
        frame = get_frame_from_call_stack(stack_index)
        module_name = frame.f_globals.get("__name__")
        if module_name != __name__:
            client_module_name = module_name
            break

    assert client_module_name, "Could not find name of module using PyRecord"
    return client_module_name
