#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
#from bs4 import BeautifulSoup
import sys
import time
import json

UserName = 'ajbone@sina.com'  # 用户名或者邮箱
PassWord = 'zj5704716'  # 密码


class smzdm:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
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
            req = self.session.post(loginURL, data=data, headers=self.headers, verify=True)
            #print json.loads(req.text)
            return req.json()['error_code']
        except Exception, e:
            print 'login error', e
            sys.exit(1)

    def checkin(self):
        t = time.time()
        t_ms = (int(round(t * 1000)))

        querystring = {"callback":"jQuery112401605018902052624_"+ str(t_ms),"_":"%s" % str(t_ms)}

        signURL = 'http://zhiyou.smzdm.com/user/checkin/jsonp_checkin'
        try:
            checkinREQ = self.session.get(url = signURL, headers=self.headers, verify=True)
            print checkinREQ
        #print json.loads(checkinREQ.text)
            return checkinREQ.json()['data']
        except Exception, e:
            print 'checkin error', e
            sys.exit(1)


    def start(self):
        loginData = self.login()
        if loginData == 0:
            print '登陆成功'
            print '签到中....'

        checkinData = self.checkin()
        if checkinData:
            print '签到成功'
            print '本次签到增加积分:', checkinData['add_point']
            print '连续签到次数:', checkinData['checkin_num']
            print '总积分:', checkinData['point']
        else:
            print '签到失败,请检查用户名和密码后重新运行.'


if __name__ == "__main__":
    smzmdLogin = smzdm(UserName, PassWord)
    smzmdLogin.start()