#!/usr/bin/env python
#coding: utf-8

import requests
import json

url = "https://api.51datakey.com/fund/v2/funds/0a140260-9ea7-11e7-b5e6-00163e002b50"

headers = {
    'authorization': "token 5d56391b8b8c471ab05df75607df6c8e",
    'cache-control': "no-cache",
    'postman-token': "83c96891-fcf8-d0ed-704e-56870beb6f68"
    }

response = requests.request("GET", url, headers=headers)

#print(response.text)
#print(response.text)

response.encoding = response.apparent_encoding
results = json.loads(response.text)

print len(results["loan_repay_record"])
print len(results["bill_record"])

url2 = "https://api.51datakey.com/fund/v2/funds-ex/0a140260-9ea7-11e7-b5e6-00163e002b50"

headers = {
    'authorization': "token 5d56391b8b8c471ab05df75607df6c8e",
    'cache-control': "no-cache",
    'postman-token': "83c96891-fcf8-d0ed-704e-56870beb6f68"
    }

response = requests.request("GET", url, headers=headers)

#print(response.text)
#print(response.text)

response.encoding = response.apparent_encoding
results = json.loads(response.text)

print len(results["loan_repay_record"])
print len(results["bill_record"])

# s = 0
# for i in  results["loan_repay_record"]:
# 	s = s +1
# 	print i
# 	print "111111111111"

# print s

