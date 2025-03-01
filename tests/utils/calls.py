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

from typing import Dict, Any
import urllib.parse
import requests
from behave.runner import Context
from .logger import logger


__all__ = "make"


def _build_url(base_url, api_version, path=None, query_params=None):
    # type: (str, str, str, Dict[str, str] | str) -> str
    """Builds a complete URL based on the given parameters."""
    parts = [base_url, api_version]
    if path:
        parts.append(path)
    url = "/".join(part.strip("/") for part in parts)
    if query_params:
        if isinstance(query_params, dict):
            url += "?" + urllib.parse.urlencode(query_params)
        elif isinstance(query_params, str):
            if not query_params.startswith('?'):
                query_params = '?' + query_params
            url += query_params
        else:
            raise TypeError("'query_params' must be a dictionary or a valid query string")
    return url


def _make_request(method, url, headers=None, body=None):
    # type: (str, str, Dict[str, str], Dict[str, Any]) -> requests.Response
    """Executes an HTTP request with the specified method and parameters."""
    if method == "GET":
        logger.debug(f"[{method}] to: {url!r}")
        return requests.get(url, headers=headers)
    elif method == "POST":
        logger.debug(f"[{method}] to: {url!r} with body: {body}")
        return requests.post(url, headers=headers, data=body)
    else:
        raise ValueError(f"Unsupported method: {method}")


def make(context, method, path, body=None):
    # type: (Context, str, str, Dict[str, Any]) -> requests.Response
    """Main function to build the URL and make the API call."""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    url = _build_url(
        base_url=context.host,
        api_version=context.api_version,
        path=path,
        query_params=getattr(context, "query_params", None),
    )
    return _make_request(method, url, headers=headers, body=body)
