#!/usr/bin/env python
#coding: utf-8

import requests
import json
import sys
import time

url = "http://gateway.saas.test.treefinance.com.cn"

def DateFormat(publishtime):
    print time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(publishtime))
    return time.strftime("%Y%m%d",time.localtime(publishtime))

def fund_start():
	#url = "http://pf.test.datatrees.cn/gateway/ecommerce/start"
	payload = "uniqueId=qatest&appid=QATestabcdefghQA&deviceInfo=%7B%0A%20%20%20%20%22positionData%22%3A%20%2222.648577%2C114.153408%22%2C%0A%20%20%20%20%22platformId%22%3A%201%2C%0A%20%20%20%20%22appVersion%22%3A%20%223.5.5%22%2C%0A%20%20%20%20%22phoneBrand%22%3A%20%22iPhone%22%0A%7D"
	headers = {
		'authorization': "apiKey 16abe89aff4a414ab3d0823e40504c5b",
		'content-type': "application/x-www-form-urlencoded",
		'cache-control': "no-cache",
		'postman-token': "22c53d7f-e04c-41bd-e2a6-f0aa940dd0c2"
	}

	response = requests.request("POST",  url = url + "/grap/h5/fund/start", data=payload, headers=headers)
	
	if response.status_code == 200:
		response.encoding = response.apparent_encoding
		results = json.loads(response.text)
		if results['success'] == True:
			results_taskId = results['data']['taskid']
			#print results_taskId
			return results_taskId
		else:
			print "Not get taskId"
	else:
		print "http error info:%s" %response.status_code
		return

def next_directive():
	payload = "appid=QATestabcdefghQA&taskid=" + taskId
	headers = {
		'content-type': "application/x-www-form-urlencoded"
	}

	response = requests.request("POST", url = url + "/grap/h5/fund/next_directive", data=payload, headers=headers)
	#print "333333333333"
	if response.status_code == 200:
		response.encoding = response.apparent_encoding
		results = json.loads(response.text)
		results_directive = results['data']['directive']
		return results_directive
	else:
		print "http error info:%s" %response.status_code

def foun_submit(username,password):
	global taskId 
	taskId = fund_start()
	print "username:%s password:%s" % (username,password)

	payload = "area_code=310000&account=%s&password=%s&login_type=1&origin=2&appid=QATestabcdefghQA&uniqueid=qatest&taskid=%s" % (username,password,taskId)
	headers = {
		'content-type': "application/x-www-form-urlencoded"
	}

	while True:
		response = requests.request("POST", url = url + "/grap/h5/fund/login/submit", data=payload, headers=headers)

		if response.status_code == 200:
			response.encoding = response.apparent_encoding
			results = json.loads(response.text)
			results_directive = results['data']['directive']
			if results_directive == "login_success":
				#print "11111111111111"
				while True:
					if next_directive() == "task_success":
						print "22222222222"
						return "taskId:%s is success" % taskId
					time.sleep(2)
						
		else:
			print "http error info:%s" %response.status_code
		time.sleep(2)


if __name__ == '__main__':
	#ecommerce_start()
	# list1 = [("100008917809","zj5704716"),("100056598801","kellychen@dfsq")]
	# for i in list1:
	# 	print i[0],i[1] 

	for i in range(2):
		if 1 == 1:
			start_date = DateFormat(time.time())
			date1 = int(time.time())
			print foun_submit("100008917809","zj5704716")
			date2 = int(time.time())

			print foun_submit("100056598801","kellychen@dfsq")
			date3 = DateFormat(time.time())
		time.sleep(2)

