#!/usr/bin/env python
#coding=utf8

import requests
import time

url = "http://zhiyou.smzdm.com/user/checkin/jsonp_checkin"
t = time.time()
t_ms = (int(round(t * 1000)))

querystring = {"callback":"jQuery112401605018902052624_"+ str(t_ms),"_":"%s" % str(t_ms)}

headers = {
    'cache-control': "no-cache",
    'postman-token': "1f5614c9-ced5-b26b-8876-e1c6edaa712c"
    }
print querystring

#response = requests.request("GET", url, headers=headers, params=querystring)

#print(response.text)