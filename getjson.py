#!/usr/bin/env python
#coding: utf-8
 # -*- coding: utf-8 -*-

import requests
import json_tools
import json

def getjson():
    expected_data = {"videoTop":[{"category":"website","count":1,"name":"土豆"},{"category":"paper","count":0,"name":"德宏团结报"},{"category":"paper","count":0,"name":"呼和浩特日报"},{"category":"paper","count":0,"name":"每日商报"},{"category":"paper","count":0,"name":"甘肃经济日报"},{"category":"website","count":0,"name":"六安声屏网"},{"category":"paper","count":0,"name":"衢州晚报"},{"category":"paper","count":0,"name":"西宁晚报"},{"category":"website","count":0,"name":"嘉峪关新闻网"},{"category":"paper","count":0,"name":"富阳日报"}],"imageTop":[{"category":"app","count":462,"name":"交汇点"},{"category":"website","count":363,"name":"北京时间"},{"category":"website","count":294,"name":"视界网"},{"category":"website","count":271,"name":"眉山网"},{"category":"website","count":258,"name":"宜春新闻网"},{"category":"app","count":239,"name":"上游新闻"},{"category":"website","count":239,"name":"丝路明珠网"},{"category":"website","count":234,"name":"观察者网"},{"category":"app","count":210,"name":"鲜果"},{"category":"website","count":176,"name":"新蓝网"}],"textTop":[{"category":"website","count":438,"name":"中国山东网"},{"category":"website","count":355,"name":"兰州新闻网"},{"category":"website","count":352,"name":"天津网"},{"category":"paper","count":351,"name":"余杭晨报"},{"category":"website","count":330,"name":"青海新闻网"},{"category":"paper","count":320,"name":"劳动报"},{"category":"website","count":315,"name":"红网"},{"category":"website","count":287,"name":"海广网"},{"category":"website","count":279,"name":"中国临夏网"},{"category":"website","count":272,"name":"忠县忠州新闻网"}],"totalTop":[{"category":"app","count":565,"name":"交汇点"},{"category":"website","count":479,"name":"北京时间"},{"category":"website","count":478,"name":"中国山东网"},{"category":"website","count":468,"name":"兰州新闻网"},{"category":"website","count":453,"name":"宜春新闻网"},{"category":"website","count":445,"name":"青海新闻网"},{"category":"website","count":434,"name":"新蓝网"},{"category":"paper","count":430,"name":"余杭晨报"},{"category":"website","count":425,"name":"中国临夏网"},{"category":"website","count":413,"name":"天津网"}]}

    expected_json=json.loads(json.dumps(expected_data))

    url = "http://203.192.16.12/api//report/top/getjson?companyId=0&lastDays=30"

    querystring = {"offset":"0","limit":"20","category":"image","metaTitle":"","startDate":"","endDate":"","isTracking":"true","metaGroup":"","author":""}

    headers = {
        'content-type': "application/x-www-form-urlencoded"
        }

    response = requests.request("GET", url, headers=headers)
    return response.content

    a == b 

getjson() 

