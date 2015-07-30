#!/usr/bin/python
#coding=utf8
import sys
import os
import urllib, urllib2
import traceback
from urllib2 import Request, urlopen, URLError, HTTPError
import httplib2

#http://192.168.1.245:8070/sessionManage/login.action?userName=admin&password=admin
#http://192.168.1.245:8070/baseinfo/householdStaff/findHouseholdStaffByOrgId.action?searchMode=noFast_noAdvanced_search&orgId=7&householdStaffVo.logout=0&householdStaffVo.isDeath=0
#os.system( "python ./login.py 192.168.1.245 8070 admin admin" )

'''
if len (sys.argv) < 2:
    print 'usage: %s host port user password' % sys.argv[0]
    sys.exit (-1)

host = sys.argv[1]
port = sys.argv[2]

username = sys.argv[3]
password = sys.argv[4]
'''

http = httplib2.Http()
url = 'http://192.168.1.245:8070/sessionManage/login.action?userName=admin&password=admin'

#login 
response, content = http.request(url, 'POST')

#get headers
headers = {'Cookie': response['set-cookie']}

#householdstaff post data
data = {'searchMode':'noFast_noAdvanced_search','orgId':7,'householdStaffVo.logout':'0','householdStaffVo.isDeath':'0',}

url = 'http://192.168.1.245:8070/baseinfo/householdStaff/findHouseholdStaffByOrgId.action'
#Cookie access
req = Request(url,data = urllib.urlencode(data),headers=headers)

try:
    response = urllib2.urlopen(req)
except HTTPError, e:
    print 'Error code: ', e.code
except URLError, e:
    print 'Reason: ', e.reason
else:
    print response.read()
