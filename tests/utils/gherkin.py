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

import six
import re
import json
from typing import Any, Dict, AnyStr
from behave.model import Table
from behave.runner import Context

from .dot_key_dict_parser import DotKeyDictParser

"""
Functions to parse Gherkin tables into dictionaries.
"""

__all__ = [
    'parse_table_to_body',
    'parse_table_to_body_json',
    'dot_key_table_to_body',
    'dot_key_table_to_body_json'
]


_CONTEXT_ATTRIBUTE_PATTERN = re.compile(r"^<ctx\.(\w+)>$")


def _ask_context_value(context, value):
    # type: (Context, str) -> Any
    context_attribute = _CONTEXT_ATTRIBUTE_PATTERN.findall(value)
    if context_attribute:
        if not hasattr(context, context_attribute[0]):
            raise AttributeError(f"Context attribute '{context_attribute[0]}' not found")
        value = getattr(context, context_attribute[0])
    return value


def parse_table_to_body(context, table, skip_nulls=True, with_context_attributes=False):
    # type: (Context, Table, bool, bool) -> Dict[str, Any]
    body = {}
    for row in table:
        if row[1] != 'null' or not skip_nulls:
            key = str(row[0])
            if with_context_attributes:
                value = _ask_context_value(context, row[1])
            else:
                value = row[1]
            if isinstance(value, six.text_type) and \
                    value.startswith('[') and value.endswith(']'):
                value = json.loads(value)
            body[key] = value
    return body


def parse_table_to_body_json(context, table, skip_nulls=True, with_context_attributes=False):
    # type: (Context, Table, bool, bool) -> AnyStr
    return json.dumps(
        parse_table_to_body(
            context=context,
            table=table,
            skip_nulls=skip_nulls,
            with_context_attributes=with_context_attributes
        )
    )


def dot_key_table_to_body(context, table, skip_nulls=True, with_context_attributes=False):
    # type: (Context, Table, bool, bool) -> Dict[str, Any]
    with DotKeyDictParser() as parser:
        return parser.parse(
            parse_table_to_body(
                context=context,
                table=table,
                skip_nulls=skip_nulls,
                with_context_attributes=with_context_attributes
            )
        )


def dot_key_table_to_body_json(context, table, skip_nulls=True, with_context_attributes=False):
    # type: (Context, Table, bool, bool) -> AnyStr
    return json.dumps(
        dot_key_table_to_body(
            context=context,
            table=table,
            skip_nulls=skip_nulls,
            with_context_attributes=with_context_attributes
        )
    )
