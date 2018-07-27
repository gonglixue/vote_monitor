import os

from server import app

from flask import make_response
from flask import request
from flask import jsonify
from flask import Response
from flask import render_template
import json

from server.server_db import ServerDB
from server import global_config


db_path = os.path.abspath(os.path.join(os.getcwd(), './asia_vote.db'))
server_db = ServerDB(db_path)     # absolute path
print("db path: ", db_path)

@app.route('/')
def main_page():
    return render_template("index.html")


@app.route('/last_minutes', methods=['GET'])
def response_last_minuts():
    # print(request.args['minutes'], request.args['singer'])
    # name = request.args['singer']
    # print(request.args)
    if 'minutes' in request.args:
        minutes = int(request.args['minutes'])
    else:
        minutes = 60

    if 'singer' in request.args:
        singers_list = [request.args['singer']]
    else:
        singers_list = global_config.all_singers

    result_data_list = [] # each element is a dict {"name": , "list":[]}

    for name in singers_list:
        query_results = server_db.get_per_minute_vote(singer_name=name, minutes=minutes)
        singer_item = {"name": name, "list": query_results, "id":global_config.all_singers_id[name]}
        result_data_list.append(singer_item)

    if len(result_data_list) > 0:
        # TODO
        # sort result by vote_num
        response = Response(json.dumps({"ok":1, "data":result_data_list, "message":"ok"}))
    else:
        response = Response(json.dumps({"ok":-1, "data":[], "message":"not a valid query"}))
        # todo: log


    response.status_code = 200
    response.headers['Content-Type'] = 'text/json'
    return response

@app.route('/last_hours', methods=['GET'])
def response_last_hours():
    if 'hours' in request.args:
        hours = int(request.args['hours'])
    else:
        hours = 48

    if 'singer' in request.args:
        singer_list = [request.args['singer']]
    else:
        singer_list = global_config.all_singers

    result_data_list = []

    for name in singer_list:
        query_results = server_db.get_per_hour_vote(singer_name=name, hours=hours)
        singer_item = {"name": name, "list": query_results, "id":global_config.all_singers_id[name]}
        result_data_list.append(singer_item)

    if len(result_data_list) > 0:
        response = Response(json.dumps({"ok":1, "data":result_data_list, "message":"ok"}))
    else:
        response = Response(json.dumps({"ok":-1, "data":[], "message": "not a valid query"}))
        # todo: log

    response.status_code = 200
    response.headers['Content-Type'] = 'text/json'
    return response


@app.route('/per_gap_in_last_hours', methods=['GET'])
def response_per_gap_in_last_hours():
    if 'singer' in request.args:
        singer_list = [request.args['singer']]
    else:
        singer_list = global_config.all_singers

    if 'last_hours' in request.args['last_hours']:
        last_hours = int(request.args['last_hours'])
    else:
        last_hours = 24

    if 'gap_minutes' in request.args:
        gap_minutes = int(request.args['gap_minutes'])
    else:
        gap_minutes = 60

    result_data_list = []
    for name in singer_list:
        query_results = server_db.get_vote_given_gap(singer_name=name, gap_minutes=gap_minutes, in_last_hours=last_hours)
        singer_item = {"name":name, "list": query_results, "id":global_config.all_singers_id[name]}
        result_data_list.append(singer_item)

    if len(result_data_list) > 0:
        response = Response(json.dumps({"ok":1, "data":query_results, "message":"ok"}))
    else:
        response = Response(json.dumps({"ok":-1, "data":query_results, "message":"not a valid query"}))

    response.status_code = 200
    response.headers['Content-Type'] = 'text/json'
    return response


@app.route('/real_time', methods=['GET'])
def response_real_time():
    name_list = global_config.all_singers
    query_results, nearest_record_time = server_db.get_latest_vote(name_list)
    # query_results: [(name, vote_num), ...]

    if len(query_results) > 0:
        response = Response(json.dumps({"ok":1, "data":query_results}))
    else:
        response = Response(json.dumps({"ok":-1, "data":[], "message": "not a valid query"}))

    response.status_code = 200
    response.headers['Content-Type'] = 'text/json'
    return response


if __name__ == '__main__':
    print("routes")

