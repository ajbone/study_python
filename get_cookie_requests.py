#!/usr/bin/python
#coding=utf8
import sys
import os
import requests
import urllib, urllib2
from urllib2 import Request, urlopen, URLError, HTTPError

#http://192.168.1.245:8070/sessionManage/login.action?userName=admin&password=admin

'''
if len (sys.argv) < 2:
    print 'usage: %s host port user password' % sys.argv[0]
    sys.exit (-1)

host = sys.argv[1]
port = sys.argv[2]
username = sys.argv[3]
password = sys.argv[4]
'''

def get_cookie():

    url = 'http://192.168.1.245:8070/sessionManage/login.action'
    data = {'userName':'admin','password':'admin'}
    
    r = requests.post(url,data=data)
#    print r.text
#    print r.headers
    
    headers = {'Cookie': r.headers['set-cookie']}
    
#    print headers
    
#    search_url = 'http://192.168.1.245:8070/sysadmin/searchUserListData/searchUserList.action?organizationId=1&user.userName=test4&searchLockStatus=all'
    
#    req = requests.post(search_url,headers=headers)
#    print req.text
    return headers

if __name__ == '__main__':
    get_cookie()
'''
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

'''
