# Copyright 2015, Gustavo Narea.
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

from re import escape as escape_regex

from nose.tools import assert_raises_regexp


def assert_raises_string(exception_class, exception_message, *args, **kwargs):
    exception_message_escaped = escape_regex(exception_message)
    exception_message_regex = "^{}$".format(exception_message_escaped)
    assert_raises_regexp(
        exception_class,
        exception_message_regex,
        *args,
        **kwargs
    )
