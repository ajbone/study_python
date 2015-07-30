#!/usr/bin/python
#coding=utf8

import urllib
import httplib2

http = httplib2.Http() 

url = 'http://192.168.1.245:8070/sessionManage/login.action?userName=zh&password=11111111'
headers = {'Content-type': 'application/x-www-form-urlencoded'}  

response, content = http.request(url, 'POST', headers=headers)  


#get headers cookie
headers = {'Cookie': response['set-cookie']}

print "Headers:",headers
print "Cookie:",response['set-cookie']

'''
search_url = 'http://192.168.1.245:8070/baseinfo/householdStaff/findHouseholdStaffByOrgId.action?searchMode=noFast_noAdvanced_search&orgId=7&householdStaffVo.logout=0&householdStaffVo.isDeath=0'


response, content = http.request(search_url, 'POST', headers=headers)

print response,content
'''
