#!/usr/bin/env python
#coding: utf-8

import requests
import json
'''
f=open('/Users/lazybone/workspaces/study_python/results.json','r')
#for i in f.readlines():
#    print i
print f.read()
f.close
'''

url = "http://cpright.xinhua-news.cn/api/match/image/getjson"

querystring = {"category":"image","offset":"30","limit":"0","sourceId":"0","metaTitle":"国新办","metaId":"0","classify":"unclassify","startTime":"","endTime":"","createStart":"","createEnd":"","sourceType":"","isTracking":"true","metaGroup":"","companyId":"0","lastDays":"7","author":""}

headers = {
    'cache-control': "no-cache",
    'postman-token': "017ce5ae-992d-488c-e4a4-342bc4f0d906"
    }

response = requests.request("POST", url, headers=headers, params=querystring)

#response.raise_for_status()
#source = response.json()
response.encoding = response.apparent_encoding
results = json.loads(response.text)
#print results['rows'][0]
print results['total']

f = open('/tmp/FN.list','w')

for i in results['rows']:
    #print u"母本:",i['sourceUrl']
    #print u"样本:",i['imagePath']

    f.write(u"母本:".encode('utf8')+i['imagePath'].encode('utf8'))
    f.write('\n')
    f.write(u"样本:".encode('utf8')+i['sourceUrl'].encode('utf8'))
    f.write('\n')
#print(source['rows'][0])
f.close()

#results = json.loads(response.text)
#print results
#print results['rows']
