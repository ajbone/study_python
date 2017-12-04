#!/usr/bin/env python
#coding: utf-8

import requests
import json
import re
import sys

def crypt(number):

	url = "http://bankbill.datatrees.com.cn/bankbill-search/crypt"

	querystring = {"callback":"jQuery214007561560955789859_1511865011307"}
	params = {"env":"2","flag":"0","inputString":number}
	payload = json.dumps(params)

	#payload = "{\n\"env\":\"2\",\n\"flag\":\"0\",\n\"inputString\":\"" + identityNumber "\"\n}"
	#print payload
	headers = {
	'content-type': "application/json",
	'cookie': "sails.sid=s%3ANVpr7gO-dp1DdARjHShYn4pKdV7B9CqI.4XZXPFCPvUc6wUMYsac3jIW%2BBMoLxjWISDfDZpU8kUo",
	'cache-control': "no-cache",
	'postman-token': "81ce1794-82d2-03c1-8b8c-cb70792d8b27"
	}

	#print payload

	response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

	if response.status_code == 200:
		# response.encoding = response.apparent_encoding
		#data = str(response.text)
		res_json = re.match(".*\((.*)\).*", str(response.text))
		if res_json is None:
			print str(response.text)
			return "identityNumber Is None!"
		else:
			identityNumber = json.loads(res_json.group(1))["data"]
			return identityNumber[0]
	else:
		return "http error info:%s" %response.status_code
		#return "Is Fail!"

	#response.encoding = response.apparent_encoding
	# data = str(response.text)
	# print data
	# res_json = re.match(".*\((.*)\).*", data)
	# print res_json
	# identityNumber = json.loads(res_json.group(1))["data"]


	# #requests = json.dump(response.text)
	# return  identityNumber[0]

def write_crypt_data(username,identityNumber):
	#print username,identityNumber
	with open('/tmp/nomatch_result_2.txt','aw') as fh:
		fh.write(str(username) + ","+ str(identityNumber)+"\n")


if __name__ == '__main__':

	reload(sys)
	sys.setdefaultencoding("utf-8")
	#with open('/Users/lazybone/edu/nomatch_result_2.txt','r') as f:
	with open('/Users/lazybone/edu/11','r') as f:
		for line in f.readlines():
			#print line
			username = line.split(',')[0]
			#print username
			number = line.split(',')[1].strip()
			#print username,number
			identityNumber = crypt(number)
			#print ("%s,%s") % (username.decode('utf-8') ,identityNumber)
			print ("%s,%s") % (username,identityNumber)
			write_crypt_data(username,identityNumber)
			# print username,identityNumber

		



