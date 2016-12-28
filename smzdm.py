#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-10-04 22:34:11
import requests
from bs4 import BeautifulSoup
import sys

UserName = 'ajbone@sina.com'  # 用户名或者邮箱
PassWord = 'zj5704716'  # 密码


class smzdm:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:41.0) Gecko/20100101 Firefox/41.0',
                        'Host': 'zhiyou.smzdm.com',
                        }
        self.session = requests.session()

    def login(self):
        data = {
            'captcha': "",
            'redirect_url': 'http://www.smzdm.com',
            'rememberme': 'on',
        }
        data['username'] = self.username
        data['password'] = self.password
        loginURL = 'https://zhiyou.smzdm.com/user/login/ajax_check'
        try:
            req = self.session.post(loginURL, data=data, headers=self.headers)
            return req.json()['error_code']
        except Exception, e:
            print 'login error', e
            sys.exit(1)
'''
    def checkin(self):
        signURL = 'http://zhiyou.smzdm.com/user/checkin/jsonp_checkin'
        checkinREQ = self.session.get(signURL, headers=self.headers)
        print checkinREQ.json()
        return checkinREQ.json()['data']
'''
    def start(self):
        loginData = self.login()
        if loginData == 0:
            print '登陆成功'
            print '签到中....'
'''
        checkinData = self.checkin()
        if checkinData:
            print '签到成功'
            print '本次签到增加积分:', checkinData['add_point']
            print '连续签到次数:', checkinData['checkin_num']
            print '总积分:', checkinData['point']
        else:
            print '签到失败,请检查用户名和密码后重新运行.'
'''

if __name__ == "__main__":
    smzmdLogin = smzdm(UserName, PassWord)
    smzmdLogin.start()
