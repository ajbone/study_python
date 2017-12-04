#!/usr/bin/env python  
#coding: utf-8  


import requests
import json

headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
data = {
     'device_id': "1234566",
     'longitude':"1",
     'os':"iOS",
     'latitude':"1"
}

url = "http://haifeisi.yipaijide.cn/recognizeService/query"
files = {'file': open('/home/zhang_jin/vobile/study_python/1.png', 'rb')}

req = requests.post(url=url,  data=data,files=files)
results = req.text
s = json.loads(results)
print type(s)
#print s["result"]
#pint s["result"]["meta"]["content_id"]
content_id = s["result"]["meta"]["content_id"]
print content_id