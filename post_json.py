#!/usr/bin/env python
#coding: utf-8

import urllib2
import json

url = "http://bankbill.datatrees.com.cn/bankbill-search/crypt"

data = {
    "env": "2",
    "flag": "0",
    "inputString": "2$1$AAAAA1KcA9+OfzOpr+UpDF4vxYhZxfJoo8lpOU0kgtj9vYiB"
}
headers = {'Content-Type': 'application/json'}
request = urllib2.Request(url=url, headers=headers, data=json.dumps(data))
response = urllib2.urlopen(request)
print response.content