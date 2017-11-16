#!/usr/bin/env python
#coding: utf-8

import requests
import json
import sys

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
		print "省份：%s,城市:%s"% （elements_ex(i["province"],elements_ex(i["city_name"]))）



def elements_ex(city_name,area_code):
	if sys.version[0] == '2':
		reload(sys)
		sys.setdefaultencoding("utf-8")
	url = "https://api.51datakey.com/fund/v2/"

	headers = {'cache-control': "no-cache",'postman-token': "552fd53c-99dc-eedf-675a-27873e06c7f6"}

	response = requests.request("GET", url = url + area_code + "/login-elements-ex", headers=headers)

	#print "支持城市：%s" % (city_name)
	response.encoding = response.apparent_encoding
	results = json.loads(response.text)
	#if len(results) >= 4:
	#	print results

	#print results
	#print len(results)

	#return "city_name: %s area_code: %s login_type: %s" % (city_name,area_code,len(results))

if __name__ == '__main__':
	get_city_list()




