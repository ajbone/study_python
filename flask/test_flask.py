#!/usr/bin/env python
#coding: utf-8

from flask import abort, jsonify, Flask, request, Response
import json
import time

app = Flask(__name__)
#支持返回json直接中文显示
app.config['JSON_AS_ASCII'] = False

task1 = {
    "data": {
        "loginName": "admin",
        "roles": 1,
        "permissions": 1,
        "active": 1
    },
    "stateCode": {
        "code": 0,
        "desc": "成功"
    },
    "statusText": "成功",
    "timestamp": "1500531770453",
    "success": 1
}

tasks = {
    "data": {
        "request": {
            "pageNumber": 1,
            "pageSize": 10000,
            "offset": 0
        },
        "data": [
            {
                "id": "72312105721925632",
                "appId": "gQXkISZCnzcZqBqQ",
                "appName": "112323243",
                "appBizLicenseVOList": [
                    {
                        "appId": 1,
                        "bizType": 1,
                        "bizName": "bill",
                        "dailyLimit": 1,
                        "isShowLicense": 1,
                        "isValid": 1
                    }
                ]
            }
        ]
    }
}

call_back_error = {
   "errorCode": 101,
   "errorMsg": "保存失败: 交易对手方字段超长"
}

call_back_all = {
   "errorCode": 0,
   "errorMsg": "回调支持的业务类型为-全部"
}

call_back_bankbill = {
   "errorCode": 1,
   "errorMsg": "回调支持的业务类型为-账单"
}

call_back_ecommerce = {
   "errorCode": 2,
   "errorMsg": "回调支持的业务类型为-电商"
}

call_back_operator = {
   "errorCode": 3,
   "errorMsg": "回调支持的业务类型为-运营商"
}

call_back_success = {
    "errorCode": 200,
    "errorMsg": "回调成功"
}

call_back_result = {
    "statusText": "成功",
    "stateCode": "200",
    "Desc":"NULL"
}

@app.route('/v1/callback', methods=['GET', 'POST'])
def app_call_back():
    if request.method == 'GET':
        print "111111111111111111GET"
        #return jsonify(call_back_operator)
        #print request.args.get('params')
        #return request.args.get('params')
        return jsonify(call_back_result)
    else:
        test_data = request.form['params']
        print "11111111111111111111111POST"
        #print test_data
        #time.sleep(3600)
        return jsonify(test_data)
        #return jsonify(call_back_result)

    #from_data = request.form.get('params','0')
    #from_data_type = json.JSONDecoder().decode(from_data)

'''
@app.route('/', methods=['POST'])
def app_call_back():
    from_data = request.form.get('param','0')
    from_data_type = json.JSONDecoder().decode(from_data)["type"]
    #return jsonify(from_data_type)
    #print from_data_info["type"]
    #time.sleep(3600)
    if from_data_type == 'all':
        return jsonify(call_back_all)
    elif from_data_type == 'bankbill':
        return jsonify(call_back_bankbill)
    elif from_data_type == 'ecommerce':
        return jsonify(call_back_ecommerce)
    elif from_data_type == 'operator':
        return jsonify(call_back_operator)
    else:
        #print from_data_type
        return jsonify(from_data_type)
'''

@app.route("/task", methods=['GET'])
def get_all_task():
    return jsonify({"task": tasks})
    #return param

@app.route('/todo/tasks', methods=['POST'])
def create_task():
    #print requets.json();
    #request.jason里面包含请求数据，如果不是JSON或者里面没有包含title字段
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id':request.json['id'],
        'title': request.json['title']
    }
    #tasks.append(task)
    return jsonify(tasks),201;

@app.route('/get_current_user', methods=['POST'])
def get_current_user():
    return jsonify(username=user.username,
                   email=user.email,
                   id=user.id)
if __name__ == "__main__":
    app.run(
        host = "192.168.202.24",
        port = 8989,
        debug = True
        )