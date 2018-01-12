#!/usr/bin/env python
# coding: utf-8
import sys
import csv
import pytest
import json
import requests
import config

reload(sys)
sys.setdefaultencoding("utf-8")


# 以下测试未对新鲜期进行测试

# 调用data-server学历接口
def getOneBlacklist(params):
    url = config.approach_huadao_blacklist

    payload = json.dumps(params, ensure_ascii=False)

    headers = {
        'content-type': "application/json"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    if response.status_code != 200:
        print ("response.status_code is %d", response.status_code)
    else:
        return response.text


# 命中一个手机号
def test_one():
    params = {
        "appid": "QATestabcdefghQA",
        "version": "1.0.0",
        "timestamp": 12341235,
        "type": 2,
        "phoneNumbers": [18987470949]
    }

    result = {
        "errorMsg": None,
        "timestamp": 12341235,
        "taskId": 123383192211566592,
        "data": {
            "blackPhones": "18987470949"
        }
    }
    result = json.dumps(result, ensure_ascii=False)

    response = getOneBlacklist(params)
    # response = json.loads(response, encoding='utf-8')
    # print response
    # print result
    assert cmp(response, result)


# 命中10个手机号
def test_two():
    params = {
        "appid": "QATestabcdefghQA",
        "version": "1.0.0",
        "timestamp": 12341235,
        "type": 2,
        "phoneNumbers": [18987470949, 13861188517, 15239818186, 18202881910, 15857779401,
                         13720870794, 15858655388, 15123796966, 15932178688, 13623798798]
    }

    result = {
        "errorMsg": None,
        "timestamp": 12341235,
        "taskId": 123383192211566592,
        "data": {
            "blackPhones": "18987470949,13861188517,15239818186,18202881910,15857779401,13720870794,15858655388,15123796966,15932178688,13623798798"
        }
    }
    result = json.dumps(result, ensure_ascii=False)

    response = getOneBlacklist(params)
    assert cmp(response, result)


# 多个手机号有的中，有的不中
def test_three():
    params = {
        "appid": "QATestabcdefghQA",
        "version": "1.0.0",
        "timestamp": 12341235,
        "type": 2,
        "phoneNumbers": [18987470942, 13861188516, 15239818186, 18202881910, 15857779401,
                         13720870790, 15858655388, 15123796966, 15932178688, 13623798798]
    }

    result = {
        "errorMsg": None,
        "timestamp": 12341235,
        "taskId": 123419808409989120,
        "data": {
            "blackPhones": "15239818186,18202881910,15857779401,15858655388,15123796966,15932178688,13623798798"
        }
    }
    result = json.dumps(result, ensure_ascii=False)

    response = getOneBlacklist(params)
    assert cmp(response, result)


# 都未中
def test_four():
    params = {
        "appid": "QATestabcdefghQA",
        "version": "1.0.0",
        "timestamp": 12341235,
        "type": 2,
        "phoneNumbers": [18987470940, 13861188510, 15239818180, 15857779400,
                         13720870790, 15858655380, 15123796960, 15932178680, 13623798790]
    }

    result = {
        "errorMsg": None,
        "timestamp": 12341235,
        "taskId": 123420616937582592,
        "data": {
            "blackPhones": ""
        }
    }
    result = json.dumps(result, ensure_ascii=False)

    response = getOneBlacklist(params)
    assert cmp(response, result)


# 单个未中
def test_five():
    params = {
        "appid": "QATestabcdefghQA",
        "version": "1.0.0",
        "timestamp": 12341235,
        "type": 2,
        "phoneNumbers": [18987470940]
    }

    result = {
        "errorMsg": None,
        "timestamp": 12341235,
        "taskId": 123420616937582592,
        "data": {
            "blackPhones": ""
        }
    }
    result = json.dumps(result, ensure_ascii=False)

    response = getOneBlacklist(params)
    assert cmp(response, result)


# 以下是异常检测
def test_error_one():
    params = {
        "appid": "QATestabcdefghQA",
        "version": "1.0.0",
        "timestamp": 12341235,
        "type": 2,
        "phoneNumbers": []
    }

    result = {
        "errorMsg": "手机号码为空",
        "timestamp": 12341235,
        "taskId": 123423371513180160,
        "data": None
    }
    result = json.dumps(result, ensure_ascii=False)

    response = getOneBlacklist(params)
    assert cmp(response, result)


def test_error_two():
    params = {
        "appid": "QATestabcdefghQA",
        "version": "1.0.0",
        "timestamp": 12341235,
        "type": 2,
        "phoneNumbers": None
    }

    result = {
        "errorMsg": "手机号码为空",
        "timestamp": 12341235,
        "taskId": 123423371513180160,
        "data": None
    }
    result = json.dumps(result, ensure_ascii=False)

    response = getOneBlacklist(params)
    assert cmp(response, result)


def test_error_three():
    params = {
        "appid": "QATestabcdefghQA",
        "version": "1.0.0",
        "timestamp": 12341235,
        "type": 2,
        "phoneNumbers": [189874709401]
    }

    result = {
        "errorMsg": "手机号码无效",
        "timestamp": 12341235,
        "taskId": 123423787772686336,
        "data": None
    }
    result = json.dumps(result, ensure_ascii=False)

    response = getOneBlacklist(params)
    assert cmp(response, result)


def test_error_four():
    params = {
        "appid": "QATestabcdefghQA",
        "version": "1.0.0",
        "timestamp": 12341235,
        "type": 2,
        "phoneNumbers": [1]
    }

    result = {
        "errorMsg": "手机号码无效",
        "timestamp": 12341235,
        "taskId": 123423787772686336,
        "data": None
    }
    result = json.dumps(result, ensure_ascii=False)

    response = getOneBlacklist(params)
    assert cmp(response, result)


def test_error_five():
    params = {
        "appid": "QATestabcdefghQA",
        "version": "1.0.0",
        "timestamp": 12341235,
        "type": 2,
        "phoneNumbers": [18987470942, 138611885161, 15239818186]
    }

    result = {
        "errorMsg": "手机号码无效",
        "timestamp": 12341235,
        "taskId": 123423787772686336,
        "data": None
    }
    result = json.dumps(result, ensure_ascii=False)

    response = getOneBlacklist(params)
    assert cmp(response, result)


def test_error_six():
    params = {
        "appid": "QATestabcdefghQA",
        "version": "1.0.0",
        "timestamp": 12341235,
        "type": 2,
        "phoneNumbers": [18987470940, 13861188510, 15239818180, 15857779400,
                         13720870790, 15858655380, 15123796960, 15932178680, 13623798790, 15932178680, 13623798790]
    }

    result = {
        "errorMsg": "手机号码列表数目太多",
        "timestamp": 12341235,
        "taskId": 123424720279711744,
        "data": None
    }
    result = json.dumps(result, ensure_ascii=False)

    response = getOneBlacklist(params)
    assert cmp(response, result)


def test_error_seven():
    params = {
        "appid": "QATestabcdefghQA",
        "version": "1.0.0",
        "timestamp": 12341235,
        "type": None,
        "phoneNumbers": [18987470940, 13861188510, 15239818180, 15857779400,
                         13720870790, 15858655380, 15123796960, 15932178680, 13623798790, 15932178680, 13623798790]
    }

    result = {
        "errorMsg": "type为空",
        "timestamp": 12341235,
        "taskId": 123424988933271552,
        "data": None
    }
    result = json.dumps(result, ensure_ascii=False)

    response = getOneBlacklist(params)
    assert cmp(response, result)


def test_error_eight():
    params = {
        "appid": "QATestabcdefghQA",
        "version": "1.0.0",
        "timestamp": 12341235,
        "type": 20,
        "phoneNumbers": [18987470940, 13861188510, 15239818180, 15857779400,
                         13720870790, 15858655380, 15123796960, 15932178680]
    }

    result = {
        "errorMsg": "type无效",
        "timestamp": 12341235,
        "taskId": 123425647803904000,
        "data": None
    }
    result = json.dumps(result, ensure_ascii=False)

    response = getOneBlacklist(params)
    assert cmp(response, result)


def test_error_nine():
    params = {
        "appid": "QATestabcdefghQA",
        "version": "alje",
        "timestamp": 12341235,
        "type": 20,
        "phoneNumbers": [18987470940, 13861188510, 15239818180, 15857779400,
                         13720870790, 15858655380, 15123796960, 15932178680]
    }

    result = {
        "errorMsg": "version无效",
        "timestamp": 12341235,
        "taskId": 123425855832993792,
        "data": None
    }
    result = json.dumps(result, ensure_ascii=False)

    response = getOneBlacklist(params)
    assert cmp(response, result)


def test_error_ten():
    params = {
        "appid": "QATestabcdefghQA",
        "version": None,
        "timestamp": 12341235,
        "type": 20,
        "phoneNumbers": [18987470940, 13861188510, 15239818180, 15857779400,
                         13720870790, 15858655380, 15123796960, 15932178680]
    }

    result = {
        "errorMsg": "version为空",
        "timestamp": 12341235,
        "taskId": 123426098385399808,
        "data": None
    }
    result = json.dumps(result, ensure_ascii=False)

    response = getOneBlacklist(params)
    assert cmp(response, result)

def test_error_eleven():
    params = {
        "appid": "QATestabcdefghQA",
        "version": None,
        "timestamp": 12341235,
        "type": 20,
        "phoneNumbers": [18987470940, 13861188510, 15239818180, 15857779400,
                         13720870790, 15858655380, 15123796960, 15932178680]
    }

    result = {
        "errorMsg": "version为空",
        "timestamp": 12341235,
        "taskId": 123426098385399808,
        "data": None
    }
    result = json.dumps(result, ensure_ascii=False)

    response = getOneBlacklist(params)
    assert cmp(response, result)

# if __name__ == '__main__':
#     test_four()
