#!/usr/bin/env python
#coding: utf-8

import requests
import json
import sys
import requests

reload(sys)
sys.setdefaultencoding("utf-8")

url = "https://api.51datakey.com/fund/v2/city-list-ex"

headers = {
    'cache-control': "no-cache",
    'postman-token': "ee068827-c827-be9d-4b7e-2fde0bca3482"
    }

response = requests.request("GET", url, headers=headers)
response.encoding = response.apparent_encoding
results = json.loads(sorted(response.text)那

province = []
city_name = []
for i in results:
	#print i["province"],",", i["city_name"]
	province.append(i["province"].decode('utf-8'))
	city_name.append(i["city_name"].decode('utf-8'))
	#print i["province"]
#print len(province)
#print len(city_name)

city_list = sorted(zip(province,city_name))

#print len(city_list)
#print str(city_list).decode("unicode-escape")  
#.decode('unicode-escape')

for j in range(len(city_list)):
	province1 = city_list[j][0]
	city_name1 = city_list[j][1]
	print province1,city_name1
	#print str(city_list[j]).decode('unicode-escape')
	#print type(city_list[j])

#print zip(province,city_name)
#print json.dumps(dict(zip(province,city_name))).decode('unicode-escape')
	#print i["province"]


	#print i["city_name"]


#print(response.text)