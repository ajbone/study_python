#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import sys

UserName = 'xxx'  # 用户名或者邮箱
PassWord = 'xx'  # 密码

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:41.0) Gecko/20100101 Firefox/41.0','Host': 'zhiyou.smzdm.com', }
data = {
            'captcha': "",
            'redirect_url': 'http://www.smzdm.com',
            'rememberme': 'on',
            'username': 'xxx',
            'password': 'xx'
        }
        
loginURL = 'https://zhiyou.smzdm.com/user/login/ajax_check'

try:
    req = requests.post(loginURL, data=data, headers=headers)
    print req.status_code
    print type(req.status_code)
    if req.status_code != 200:
        raise Exception("get connent fail")
    if req.json()['error_code'] != 0:
        print "Login Fail..."
except:
    print req.status_code
    sys.exit()




'''

try:
    req = self.session.post(loginURL, data=data, headers=headers)
    return req.json()['error_code']
except Exception, e:
    print 'login error', e
    sys.exit(1)
'''
