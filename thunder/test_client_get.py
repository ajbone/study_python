#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import httplib
import json

if len (sys.argv) < 3:
    print 'Usage: %s host url' % sys.argv[0]
    sys.exit (-1)

host = sys.argv[1]
url = sys.argv[2]

api_key = "this-is-TMP-apikey"

header = { 'Content-type' : 'application/x-www-form-urlencoded', \
    'User-Agent' : 'thunder 7.0.1', \
'X-Client-ID' : 'client_id123456', \
'X-File-ID' : 'test',\
'X-File-Name' : 'testname',\
'X-File-Size' : '123456',\
'X-Download-Percentage' : '50',\
'X-Mime-Type' : 'video/mp4' }

request_url = '/query?key=%s&url=%s' % (api_key, url)
print request_url

#GET /query?key=thunder-client&url=http://host/video.mp4&hash=hash-code&f=0 HTTP/1.1
conn = httplib.HTTPSConnection (host, 443)
#conn = httplib.HTTPConnection (host, 80)
conn.request("GET", request_url, None, header)

res = conn.getresponse ()
results = res.read ()
r_headers = res.getheaders ()

print res.status
print r_headers
print results
