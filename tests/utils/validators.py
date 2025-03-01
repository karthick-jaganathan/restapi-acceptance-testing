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


__all__ = "partial_dict_compare"


def partial_dict_compare(expected, actual, path="root"):
    """
    Recursively compare expected keys and values against the actual JSON object.

    Args:
        expected: The expected JSON structure.
        actual: The actual JSON structure.
        path: The current key path for error tracking.

    Raises:
        AssertionError: If the comparison fails.
    """
    if isinstance(expected, dict):
        assert isinstance(actual, dict), \
            f"Expected a dictionary at '{path}', but got {type(actual)}"
        for key, value in expected.items():
            assert key in actual, \
                f"Key '{key}' not found in the actual JSON at '{path}'"
            partial_dict_compare(value, actual[key], f"{path}.{key}")
    elif isinstance(expected, list):
        assert isinstance(actual, list), \
            f"Expected a list at '{path}', but got {type(actual)}"
        assert len(expected) == len(actual), \
            f"List length mismatch at '{path}': expected {len(expected)}, got {len(actual)}"
        for index, (exp_item, act_item) in enumerate(zip(expected, actual)):
            partial_dict_compare(exp_item, act_item, f"{path}[{index}]")
    else:
        assert expected == actual, \
            f"Value mismatch at '{path}': expected '{expected}', but got '{actual}'"
