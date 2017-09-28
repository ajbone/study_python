#!/usr/bin/env python
#coding: utf-8

import requests
import json
import os
import time

def DateFormat(publishtime):
    print time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(publishtime))
    return time.strftime("%Y%m%d",time.localtime(publishtime))

def post_account():
	url = "https://api.51datakey.com/fund/v2/tasks"

	payload = "{\n  \"area_code\": \"310000\",\n  \"account\": \"100008917809\",\n  \"password\": \"zj5704716\",\n  \"login_type\": \"1\",\n  \"origin\": \"3\",\n  \"user_id\": \"1234567890\"\n}"

	headers = {
		'authorization': "apiKey 16abe89aff4a414ab3d0823e40504c5b",
		'content-type': "application/json"
	}

	response = requests.request("POST", url, data=payload, headers=headers)
	response.encoding = response.apparent_encoding
	results = json.loads(response.text)
	print results
	#print results["task_id"]
	return results["task_id"]

def get_status():
	global task_id 
	task_id = post_account()
	while True:
		url = "https://api.51datakey.com/fund/v2/tasks/"

		headers = {
			'authorization': "apiKey 16abe89aff4a414ab3d0823e40504c5b",
			'cache-control': "no-cache",
			'postman-token': "5cb2ab16-98df-2422-b408-7e9548c9f245"
		}

		response = requests.request("GET", url = url + task_id + "/status", headers=headers)
		#return response.text["phase_status"]
		response.encoding = response.apparent_encoding
		results = json.loads(response.text)
		if results["phase_status"] == "DONE_SUCC":
			return get_result()

		time.sleep(1)
def get_result():
	url = "https://api.51datakey.com/fund/v2/funds/"

	headers = {
		'authorization': "token 5d56391b8b8c471ab05df75607df6c8e",
		'cache-control': "no-cache",
		'postman-token': "5f5304c3-8bf5-c76d-91e5-ef5d35b50237"
		}

	response = requests.request("GET", url = url + task_id , headers=headers)
	response.encoding = response.apparent_encoding
	results = json.loads(response.text)
	if results["task_id"] == task_id:
		#print "size:",os.path.getsize(results)
		#print(response.text)
		print  "success"
	else:
		print "fail"

if __name__ == '__main__':
	start_time = int(time.time())
	get_status()
	end_time = int(time.time())
	print "Total time :" , end_time - start_time


