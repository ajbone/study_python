#!/usr/bin/env python
#coding: utf-8

import requests
import json
import sys


def edu(number,username):
	print username,number
	url = "http://192.168.5.25:8168/data/education"
	#url = "https://gateway.saas.treefinance.com.cn/data/education"

	params = {
	    "appid": "QATestabcdefghQA",
	    "version": "1.0.0",
	    "timestamp": 12423423425000,
	    "type": 1,
	    "identityNumber": number,
	    "userName": username
	}
	#payload = "{\"userName\": \"%s\", \"timestamp\": 12423423425000, \"version\": \"1.0.0\", \"appid\": \"QATestabcdefghQA\", \"identityNumber\": \"%s\", \"type\": 1}" % (username,number)
	#print params
	#print payload
	payload = json.dumps(params,ensure_ascii=False)
	print payload

	headers = {
	    'content-type': "application/json",
	    'cache-control': "no-cache",
	    'postman-token': "6e7c70cf-b917-0877-195e-04cf07833364"
	    }

	response = requests.request("POST", url, data=payload, headers=headers)
	if response.status_code == 200:
		return response.text
		#print response.status_code
		#print(response.text)
	else:
		return ""
	


if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding("utf-8")
	#sum = 0
	fh = open('/tmp/nomatch_result_2.txt','rw')
	for line in fh.readlines():
		username = line.split(',')[0].strip()
		#print username
		number = line.split(',')[1].strip()
		print  edu(number,username)
		#sum = sum +1

	#print sum
		#print ("%s,%s") % (username.decode('utf-8') ,identityNumber)
		# print username,identityNumber

