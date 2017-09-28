#!/usr/bin/env python
#coding: utf-8

import requests
import json

url = "http://supermarket.test.91gfd.cn/supermarket/loanProduct/home"

payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"userid\"\r\n\r\n60394065904144384\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
headers = {
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'cache-control': "no-cache",
    'postman-token': "9aed0266-adc3-d5f6-3546-1276112bc724"
    }

response = requests.request("POST", url, data=payload, headers=headers)
#results = json.loads(response.text)
#print(results)
#print len(results['data'])
#print type(results['data'])
for item in results['data']:
	print  item['id'],item['name']
