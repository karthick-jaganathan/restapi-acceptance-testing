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

Feature: GET
  # Enter feature description here

  Background:
    Given a REST API at "http://localhost:5000"
    And with an API version "v1"

  @GET
  Scenario: GET simple-get (200 OK)
    Given a REST API resource at "/simple-get"
    When a "GET" request is made
    Then the expected response status code is "200"
    And the response body is
      """
      {
        "message": "GET request successful"
      }
      """

  @GET
  Scenario Outline: GET get_with_params (200 OK)
    Given a REST API resource at "get_with_params"
    And with the following query parameters
      | key    | value    |
      | param1 | <param1> |
      | param2 | <param2> |
    When a "GET" request is made
    Then the expected response status code is "200"
    And the response body contains the following data table
      | param       | value    |
      | data.param1 | <param1> |
      | data.param2 | <param2> |

    Examples:
      | param1 | param2   |
      | 7      | 8        |
      | ABC    | XYZ      |
