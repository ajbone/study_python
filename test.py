#!/usr/bin/python
#coding=utf8
import sys
import os
import urllib, urllib2
import requests
from urllib2 import Request, urlopen, URLError, HTTPError
url = "http://znewsapp-c.pala-pala.net/voteFlow/save_shoot"
data = {'match': 'yes','user_id': '8343132486','country': "中国",'province': "浙江",'city': "杭州",'file_id': "test_dammy_file",'result[content_id]': '0af00709-49b9-47e4-833c-2fc50f5b0e38'}
req = requests.post(url=url,data=data)
#print req.text
#print req.raise_for_status
print req.status_code