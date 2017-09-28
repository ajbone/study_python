#!/usr/bin/env python
#coding: utf-8

import requests
import sys
import json

reload(sys)
sys.setdefaultencoding("utf-8")

def get_city_list():
	url = "https://api.51datakey.com/fund/v2/city-list"

	headers = {
    'cache-control': "no-cache",
    'postman-token': "be677859-510d-cf68-2ab4-c482210a6cfa"
    }

	response = requests.request("GET", url, headers=headers)
	response.encoding = response.apparent_encoding
	results = json.loads(response.text)

	for i in results:
		'''
		if i["city_name"] == u"张掖":
			print elements_ex(i["city_name"],i["area_code"])
			print i["city_name"],i["area_code"]
		'''
		print login_elements_ex(i["city_name"],i["area_code"])

def login_elements_ex(city_name,area_code):

	url = "https://api.51datakey.com/fund/v2/"

	headers = {
	    'cache-control': "no-cache",
	    'postman-token': "e8bf8576-443a-9769-0d7b-7df63085a6bf"
	    }

	response = requests.request("GET", url = url + area_code + "/login-elements-ex", headers=headers)

	if response.status_code == 200:
		response.encoding = response.apparent_encoding
		results = json.loads(response.text)
		for i in results:
			for j in i["fields"]:
				if j["type"] == "select":
					print city_name,area_code
					print json.dumps(results,ensure_ascii=False)
				else:
					break

if __name__ == '__main__':
	get_city_list()



#print(response.text)