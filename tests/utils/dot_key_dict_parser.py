#!/usr/bin/env python
# /*************************************************************************
# * Copyright 2025 Karthick Jaganathan
# *
# * Licensed under the Apache License, Version 2.0 (the "License");
# * you may not use this file except in compliance with the License.
# * You may obtain a copy of the License at
# *
# * https://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
# **************************************************************************/


"""
Re-Structuring dot-separated key-value pairs as a dictionary.

This module helps in re-structuring Gherkin table headers defined using
dot-separated keys to define inner keys and their values, converting
them into a dictionary.

Usage:
------
* Gherkin table values are always read as strings. Use the following
  conventions to define values:
    - To define boolean values, use bool(true)/bool(false).
    - An integer/float/string can be defined as int(1)/float(1.00)/str(1.23).
* If a value starts with '[' and ends with ']', it will be converted to a list.
* If a value starts with '{' and ends with '}', it will be converted to a dict.
* If a value is 'none' or 'null', it will be converted to None.
* if a value is '--na--', it will be ignored.

Example:
    >>> a_dict = {
    ...     'a.b.c': '1',
    ...     'a.b.d': 2,
    ...     'a.e': '3',
    ...     'f': '4',
    ...     'g': 'bool(true)',
    ...     'h': 'int(1)',
    ...     'i': 'float(1.00)',
    ...     'j': 'str(1.23)',
    ...     'k': '[1, 2, 3]',
    ...     'l': '{1: 2, 3: 4}',
    ...     'm': 'none',
    ...     'n': 'null',
    ...     'o': '--na--'
    ... }
    >>> parser = DotKeyDictParser()
    >>> parser.parse(a_dict)
    {'a': {'b': {'c': '1', 'd': 2}, 'e': '3'}, 'f': '4', 'g': True, 'h': 1,
    'i': 1.0, 'j': '1.23', 'k': [1, 2, 3], 'l': {1: 2, 3: 4}, 'm': None, 'n': None}

    >>> with DotKeyDictParser() as parser:
    ...     data = parser.parse(a_dict)
    ...
    >>> data
    {'a': {'b': {'c': '1', 'd': 2}, 'e': '3'}, 'f': '4', 'g': True, 'h': 1,
    'i': 1.0, 'j': '1.23', 'k': [1, 2, 3], 'l': {1: 2, 3: 4}, 'm': None, 'n': None}

"""

from __future__ import absolute_import

import ast
import re


__all__ = 'DotKeyDictParser'


class DotKeyDictParser(object):
    __slots__ = ['__dict__']
    _safe_text = {
        'bool(true)': True,
        'bool(false)': False,
        'none': None,
        'null': None
    }
    _type_map = {
        'str': str,
        'float': float,
        'int': int
    }

    def __numbervalue(self, value):
        match = re.match(r'(int|float|str)\((.*?)\)', value)
        if match:
            type_, value = match.groups()
            function = self._type_map.get(type_, str)
            return function(value)

    def __load_safe(self, value):
        # if instance of value is number, return the number
        if isinstance(value, (int, float)):
            return value
        if value.startswith('[') and value.endswith(']'):
            return ast.literal_eval(value)
        if value.startswith('{') and value.endswith('}'):
            return ast.literal_eval(value)
        number_value = self.__numbervalue(value)
        if number_value is not None:
            return number_value
        return self._safe_text.get(value.lower(), value)

    @staticmethod
    def __pre_process(data):
        return {k: v for k, v in data.items() if v != '--na--'}

    def __add_object(self, name):
        setattr(self, name, {})
        return getattr(self, name)

    def __unload(self):
        self.__dict__ = {}

    def parse(self, data):
        super_dict = {}
        re_pattern = re.compile(r'(.*)(\[(\d+)])$|(.+)')
        for key in sorted(self.__pre_process(data), key=len, reverse=True):
            obj = super_dict
            keys = key.split('.')
            for k in keys[:-1]:
                k_, _, idx, k__ = re.match(re_pattern, k).groups()
                k_ = k_ or k__
                if k_ not in obj:
                    # Considering as list, if idx is not None
                    if idx is not None:
                        obj[k_] = [self.__add_object(k)]
                        obj = obj[k_][0]
                    else:
                        obj[k_] = {}
                        obj = obj[k_]
                else:
                    if idx is not None:
                        if not hasattr(self, k):
                            obj[k_].append(self.__add_object(k))
                        obj = getattr(self, k)
                    else:
                        obj = obj if isinstance(obj[k_], list) else obj[k_]
            obj[keys[-1]] = self.__load_safe(data[key])
        self.__unload()
        return super_dict

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__unload()


def test_dot_key_dict_parser():
    a_dict = {
        'a.b.c': '1',
        'a.b.d': 2,
        'a.e': '3',
        'f': '4',
        'g': 'bool(true)',
        'h': 'int(1)',
        'i': 'float(1.00)',
        'j': 'str(1.23)',
        'k': '[1, 2, 3]',
        'l': '{1: 2, 3: 4}',
        'm': 'none',
        'n': 'null',
        'o': '--na--'
    }
    parser = DotKeyDictParser()
    assert parser.parse(a_dict) == {
        'a': {'b': {'c': '1', 'd': 2}, 'e': '3'},
        'f': '4',
        'g': True,
        'h': 1,
        'i': 1.0,
        'j': '1.23',
        'k': [1, 2, 3],
        'l': {1: 2, 3: 4},
        'm': None,
        'n': None
    }, "Failed to parse the dictionary"

    with DotKeyDictParser() as parser:
        data = parser.parse(a_dict)
    assert data == {
        'a': {'b': {'c': '1', 'd': 2}, 'e': '3'},
        'f': '4',
        'g': True,
        'h': 1,
        'i': 1.0,
        'j': '1.23',
        'k': [1, 2, 3],
        'l': {1: 2, 3: 4},
        'm': None,
        'n': None
    }, "Failed to parse the dictionary"

    print("All tests passed!")


if __name__ == '__main__':
    test_dot_key_dict_parser()
