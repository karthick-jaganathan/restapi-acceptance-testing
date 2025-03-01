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

Feature: POST
  # Enter feature description here

  Background:
    Given a REST API at "http://localhost:5000"
    And with an API version "v1"

  Scenario: POST simple-post (201 Created)
    Given a REST API resource at "/simple-post"
    And with the following request body
      | param | value |
      | key1  | val1  |
      | key2  | val2  |
    When a "POST" request is made
    Then the expected response status code is "201"
    And the response body contains the following data table
      | param          | value |
      | data.key1   | val1  |
      | data.key2   | val2  |

  Scenario Outline: POST simple-post (201 Created)
    Given a REST API resource at "/simple-post"
    And with the following request body
      | param | value |
      | key1  | <key1> |
      | key2  | <key2> |
    When a "POST" request is made
    Then the expected response status code is "201"
    And the response body contains the following data table
      | param          | value |
      | data.key1   | <key1> |
      | data.key2   | <key2> |

    Examples:
      | key1 | key2   |
      | val1 | --na-- |
      | val3 | val4   |
      | val5 | null   |
      | val7 | val8   |
      | ABC  | XYZ    |

  Scenario: POST simple-post (201 OK)
    Given a REST API resource at "/simple-post"
    And saved attributes to context
      | param | value |
      | name  | ABC   |
    And with the following request body with context attributes
      | param | value      |
      | key1  | <ctx.name> |
      | key2  | val2       |
    When a "POST" request is made
    Then the expected response status code is "201"
    And the response body contains the following data table with context attributes
      | param        | value      |
      | data.key1 | <ctx.name> |
      | data.key2 | val2       |
