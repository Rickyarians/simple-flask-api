#!/usr/bin/python3

# MIT License

# Copyright (c) 2019 Pipin Fitriadi

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
W
"""
import json
from re import A
from flask import abort, Flask, jsonify, redirect, request, url_for 
import datetime as dt
import pytz

def post():
    data = {}
    if request.json:
        print(request.json)
        date_time_str = json.loads(
                request.data
        ).get('date')
    else:
        abort(400)

    
    try:
        date_time_obj = dt.datetime.strptime(date_time_str, '%d-%m-%Y')
        print(date_time_obj)
        data = {
        'code': 200,
        'message': date_time_str + ' Successfully Converted',
        'date': {
            'Day': '{0:%A}'.format(date_time_obj),
            'Date': '{0:%d}'.format(date_time_obj),
            'Month': '{0:%B}'.format(date_time_obj),
            'Year': '{0:%Y}'.format(date_time_obj),
            'oldFormat': date_time_str,
            'newFormat': '{0:%A}, {0:%d} - {0:%B} - {0:%Y}'.format(date_time_obj),
        },
        }
    except Exception as e:
        print(str(e))
        abort(400, str(e))
   
    return data


def response_api(data):
    return (
        jsonify(**data),
        data['code']
    )

app = Flask(__name__)

@app.errorhandler(400)
def bad_request(e):
    return response_api({
        'code': 400,
        'status': 'failed',
        'message': e.description,
    })

@app.errorhandler(404)
def not_found(e):
    return response_api({
        'code': 404,
        'message': 'Data Tidak Ditemukan.',
        'data': None
    })

@app.errorhandler(405)
def method_not_allowed(e):
    return response_api({
        'code': 405,
        'message': 'Method tidak diperbolehkan.',
        'data': None
    })

@app.errorhandler(500)
def internal_server_error(e):
    return response_api({
        'code': 500,
        'message': 'Mohon maaf, ada gangguan pada server kami.',
        'data': None
    })

@app.route('/')
def root():
    return 'RESTful API Flask Simple Boilerplate'
@app.route('/checkdate', methods=['POST'])
def dateConvert():
    """
    RESTful API dateConvert.
    """
    # Method Post checkdate
    if request.method == 'POST':
        data = post()
    return response_api(data)

if __name__ == '__main__':
    app.run(debug=True)