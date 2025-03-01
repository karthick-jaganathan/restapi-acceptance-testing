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

import json
from behave import given, when, then, step
from behave.runner import Context
from tests.steps import set_attr
from tests.utils import calls, gherkin, validators


@given('a REST API at "{host}"')
def step_impl(context, host):
    # type: (Context, str) -> None
    set_attr(context, 'host', host, raise_if_exists=True)


@step(u'with an API version "{api_version}"')
@step('an API version "{api_version}"')
def step_impl(context, api_version):
    # type: (Context, str) -> None
    set_attr(context, 'api_version', api_version, raise_if_exists=True)


@given('a REST API resource at "{resource_path}"')
def step_impl(context, resource_path):
    # type: (Context, str) -> None
    set_attr(context, 'resource_path', resource_path, raise_if_exists=True)


@step(u'saved attributes to context')
def step_impl(context):
    # type: (Context) -> None
    for key, value in gherkin.dot_key_table_to_body(context, context.table, skip_nulls=False).items():
        set_attr(context, key, value, raise_if_exists=True)


@step(u'with the following query parameters {with_context_attributes}')
@step(u'with the following query parameters')
def step_impl(context, with_context_attributes=None):
    # type: (Context) -> None
    if context.table:
        query_params = gherkin.dot_key_table_to_body(
            context=context,
            table=context.table,
            skip_nulls=False,
            with_context_attributes=with_context_attributes == "with context attributes"
        )
        set_attr(context, 'query_params', query_params)
    elif context.text:
        set_attr(context, 'query_params', context.text)
    else:
        set_attr(context, 'query_params', None)


@when(u'a "{method}" request is made')
def step_impl(context, method):
    # type: (Context, str) -> None
    body = None
    if method == "POST":
        body = context.request_body if hasattr(context, "request_body") else None
    set_attr(context, 'response', calls.make(context, method, context.resource_path, body=body))


@then(u'the expected response status code is "{status_code:d}"')
def step_impl(context, status_code):
    # type: (Context, int) -> None
    assert context.response.status_code == status_code, \
        f"Expected status code is {status_code}, but got {context.response.status_code}"


@then(u'the response body is')
def step_impl(context):
    # type: (Context) -> None
    assert context.response.json() == json.loads(context.text)


@step('the response body contains the following data table')
@step('the response body contains the following data table {with_context_attributes}')
@step('the response body is "{is_partial}" compared against the following data table')
@step('the response body is "{is_partial}" compared against the following data table {with_context_attributes}')
def step_impl(context, is_partial=None, with_context_attributes=None):
    # type: (Context, str, str) -> None
    expected = gherkin.dot_key_table_to_body(
        context=context,
        table=context.table,
        skip_nulls=False,
        with_context_attributes=with_context_attributes == "with context attributes"
    )
    actual = context.response.json()
    if is_partial == "partially":
        validators.partial_dict_compare(expected, actual)
    else:
        assert actual == expected, f"Expected {expected}, but got {actual}"


@step(u'with the following request body')
@step(u'with the following request body {with_context_attributes}')
def step_impl(context, with_context_attributes=None):
    # type: (Context, str) -> None
    request_body = gherkin.dot_key_table_to_body_json(
        context=context,
        table=context.table,
        skip_nulls=False,
        with_context_attributes=with_context_attributes == "with context attributes"
    )
    set_attr(context, 'request_body', request_body)
