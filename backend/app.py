#!flask/bin/python

__author__ = 'mohammad'

import time
import datetime

import logging
import logging.handlers

from flask import Flask, jsonify, abort, make_response, request, current_app
from datetime import timedelta
from functools import update_wrapper
from dynamo_io import get_item

LOG_FILENAME = 'log_api.out'
my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME,
                                               maxBytes=100000,
                                               backupCount=3,
                                               )
my_logger.addHandler(handler)

app = Flask(__name__)

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

@app.errorhandler(404)
def not_found(error):
    my_logger.debug('[API Logs] Error 404')
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/index')
@app.route('/')
def index():
    my_logger.debug('[API Logs] Indexing now')
    return "Hello, World!"

tasks = [
    {
        'id': 1, 'hash': u'abc1',
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'hash': u'abc2',
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    },
    {
        'id': 4,
        'hash': u'abc4',
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@app.route('/allTasks',methods=['GET'])
def get_tasks():
    my_logger.debug('[API Logs] getting all-tasksd')
    return jsonify({'tasks': tasks})

@app.route('/taskByID/<int:task_id>',methods=['GET'])
def get_task_id(task_id):
    my_logger.debug('[API Logs] getting task with id: ', task_id)
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.route('/code_commit', methods=['GET'])
@crossdomain(origin='*')
def get_code_commit():
    date_dd_mm_yyyy = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y')
    my_logger.debug('[API Logs] getting code_commit metric with date: '+date_dd_mm_yyyy)
    json_data = get_item('code_commit', date_dd_mm_yyyy)
    return jsonify({'result': json_data})

@app.route('/boombar', methods=['GET'])
@crossdomain(origin='*')
def get_boombar():
    date_dd_mm_yyyy = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y')
    my_logger.debug('[API Logs] getting boombar metric with date: '+date_dd_mm_yyyy)
    json_data = get_item('boombar', date_dd_mm_yyyy)
    return jsonify({'result': json_data})

@app.route('/vui', methods=['GET'])
@crossdomain(origin='*')
def get_vui():
    date_dd_mm_yyyy = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y')
    my_logger.debug('[API Logs] getting vui metric with date: '+date_dd_mm_yyyy)
    json_data = get_item('vui', date_dd_mm_yyyy)
    return jsonify({'result': json_data})

@app.route('/aws-cost', methods=['GET'])
@crossdomain(origin='*')
def get_aws_cost():
    date_dd_mm_yyyy = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y')
    my_logger.debug('[API Logs] getting aws-costs metric with date: '+date_dd_mm_yyyy)
    json_data = get_item('aws-cost', date_dd_mm_yyyy)
    return jsonify({'result': json_data})

@app.route('/taskByHash/<task_hash>',methods=['GET'])
def get_task_hash(task_hash):
    my_logger.debug('[API Logs] getting task with hash '+task_hash)
    task = [task for task in tasks if task['hash'] == task_hash]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

if __name__ == '__main__':
    app.run(debug=True)

