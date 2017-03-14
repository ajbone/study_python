#!/usr/bin/env python
#coding: utf-8

import requests
import json
import requests

url = "http://cpright.xinhua-news.cn/api/match/image/getjson"

querystring = {"category":"image","offset":"0","limit":"0","sourceId":"0","metaTitle":"","metaId":"0","classify":"unclassify","startTime":"","endTime":"","createStart":"","createEnd":"","sourceType":"","isTracking":"true","metaGroup":"","companyId":"0","lastDays":"7","author":""}
headers = {
    'cache-control': "no-cache",
    'postman-token': "714c7b71-e6ed-5a3e-95aa-69d85b64188d"
    }

response = requests.request("POST", url, headers=headers, params=querystring)


response.encoding = response.apparent_encoding
results = json.loads(response.text)

#print "Total:",results['total']
print "rows:",len(results['rows'])

f = open("/Users/lazybone/workspaces/study_python/0309_match.list",'w')

for i in results['rows']:
    f.write(u"母本:".encode('utf8')+i['imagePath'].encode('utf8'))
    f.write('\n')
    f.write(u"样本:".encode('utf8')+i['sourceUrl'].encode('utf8'))
    f.write('\n')

f.close()
#print results['total']
#print(response.text)
