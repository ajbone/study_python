#!/usr/bin/python
#coding=utf8
import sys
import os
import urllib, urllib2
import traceback
from urllib2 import Request, urlopen, URLError, HTTPError

#http://192.168.1.245:8070/sessionManage/login.action?userName=admin&password=admin


if len (sys.argv) < 2:
    print 'usage: %s host port user password' % sys.argv[0]
    sys.exit (-1)

host = sys.argv[1]
port = sys.argv[2]
username = sys.argv[3]
password = sys.argv[4]

data = {'userName': username, 'password': password}

headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

url = 'http://%s:%s/sessionManage/login.action' % (host,port)

req = Request(url,data = urllib.urlencode(data),headers=headers)

try:
    response = urllib2.urlopen(req)
except HTTPError, e:
    print 'Error code: ', e.code
except URLError, e:
    print 'Reason: ', e.reason
else:
    print response.read()
