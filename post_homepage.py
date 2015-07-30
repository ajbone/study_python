#!/usr/bin/python
#coding=utf8
import sys
import os
import requests
import urllib, urllib2
from urllib2 import Request, urlopen, URLError, HTTPError
import get_cookie_requests

'''
if len (sys.argv) < 2:
    print 'usage: %s host port user password' % sys.argv[0]
    sys.exit (-1)

host = sys.argv[1]
port = sys.argv[2]
username = sys.argv[3]
password = sys.argv[4]
'''
'''
def searchuserlist():
    
    headers = get_cookie_requests.get_cookie()
    
#    print headers
    
    search_url = 'http://192.168.1.245:8070/sysadmin/searchUserListData/searchUserList.action?organizationId=1&user.userName=test4&searchLockStatus=all'
    
    req = requests.post(search_url,headers=headers)
    return req.text

if __name__ == '__main__':
    print searchuserlist()
'''

url = "http://scmd.wasu.cn/cms/web//videoData/homePageMovie"
req = requests.post(url = url)
print req.text
