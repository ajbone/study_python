#!/usr/bin/env python
#coding: utf-8
import requests
import sys

if len (sys.argv) < 1:
        print 'usage: %s url' % sys.argv[0]
        sys.exit (-1)

url1 = "https://api.saas.treefinance.com.cn/gateway/"
#url2 = "https://api.saas.treefinance.com.cn/gateway/operator/start"
#url3 = "https://api.saas.treefinance.com.cn/gateway/ecommerce/start"

gateway_type = sys.argv[1]

payload = "appid=pJWAtOx8SDIZr5PH&uniqueId=qatest0906&deviceInfo=%7B%22positionData%22%3A%20%2222.648577%2C114.153408%22%2C%20%20%20%20%20%22platformId%22%3A%201%2C%20%20%20%20%20%22appVersion%22%3A%20%223.5.5%22%7D"
headers = {
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache",
    'postman-token': "9d189b7c-2a34-3295-b18b-8b0bf2e87071"
    }

response = requests.request("POST", url= url1 + gateway_type + "/start", data=payload, headers=headers)

print(response.text)
