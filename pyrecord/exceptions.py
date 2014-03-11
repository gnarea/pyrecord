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

__all__ = [
    "RecordException",
    "RecordInstanceError",
    "RecordTypeError",
    ]


class RecordException(Exception):
    """Abstract base class for all the exceptions raised by PyRecord."""
    pass


class RecordTypeError(RecordException):
    """Exception for errors at the record type-level."""
    pass


class RecordInstanceError(RecordException):
    """Exception for errors at the record instance-level."""
    pass
