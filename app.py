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

# Demo Flask application

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/v1/simple-get', methods=['GET'])
def simple_get():
    return jsonify({"message": "GET request successful"}), 200


@app.route('/v1/simple-post', methods=['POST'])
def simple_post():
    data = request.get_json()
    return jsonify({"data": data}), 201


@app.route('/v1/get_with_params', methods=['GET'])
def get_with_params():
    param1 = request.args.get('param1')
    param2 = request.args.get('param2')
    return jsonify({"data": {"param1": param1, "param2": param2}}), 200


if __name__ == '__main__':
    app.run(debug=True)
