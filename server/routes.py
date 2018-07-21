import os

from server import app

from flask import make_response
from flask import request
from flask import jsonify
from flask import Response
import json

from server.server_db import ServerDB


db_path = os.path.abspath(os.path.join(os.getcwd(), './asia_vote.db'))
server_db = ServerDB(db_path)     # absolute path
print("db path: ", db_path)

@app.route('/')
def main_page():
    return 'hello world'


@app.route('/last_minutes', methods=['GET'])
def response_last_minuts():
    # print(request.args['minutes'], request.args['singer'])
    name = request.args['singer']
    minutes = int(request.args['minutes'])
    # query = json.loads(request.get_data())
    # minutes = query["minutes"]
    # print(minutes)
    # name = request.args[]
    query_results = server_db.get_per_minute_vote(singer_name=name, minutes=minutes)

    if len(query_results) > 0:
        response = Response(json.dumps({"ok":1, "data":query_results, "message":"ok"}))
    else:
        response = Response(json.dumps({"ok":1, "data":[], "message":"not a valid query"}))


    response.status_code = 200
    response.headers['Content-Type'] = 'text/json'
    return response

@app.route('/real_time', methods=['GET'])
def response_real_time():
    name_list = ['吴宣仪', '孟美岐', 'Yamy', '周洁琼', '鞠婧祎', '李艺彤', '于文文', '陈意涵', '王菊', '苏诗丁']
    query_results = server_db.get_latest_vote(name_list)

    response = Response(json.dumps({"ok":1, "data":query_results}))
    response.status_code = 200
    response.headers['Content-Type'] = 'text/json'
    return response


if __name__ == '__main__':
    print("routes")

