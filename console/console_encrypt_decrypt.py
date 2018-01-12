#!/usr/bin/env python
#coding: utf-8

import requests
import json
import sys

class console:
#通过requests.session方法保持cookies，跨请求调用
	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.headers = {
			'content-type': "application/json"
			}
		self.session = requests.session()

	def login(self):
		params = {
		"username":self.username,
		"password":self.password
		}

		payload = json.dumps(params,ensure_ascii=False)

		loginURL = "http://console.saas.test.treefinance.com.cn/server/login"

		try:
			req = self.session.post(loginURL, data=payload, headers=self.headers, verify=True)
			res_json = json.loads(req.text)
			if res_json["success"] == True:
				return req.text
			else:
				#print req.text
				return "登录失败"
		except Exception, e:
			print 'login error', e
			#sys.exit(1)

#解密AES加密的数据
	def decrypt(self,decryptData):
		loginData = self.login()

		decryptURL = "http://console.saas.test.treefinance.com.cn/server/saas/console/tool/knife/crypto/decrypt"

		params = {
			"param":decryptData
		}

		try:
			req = self.session.post(decryptURL, data=json.dumps(params), headers=self.headers, verify=True)
			if req.status_code == 200:
				return req.text
			else:
				return "http error info:%s" %req.status_code
		except Exception, e:
			print 'decrypt error', e
			#sys.exit(1)

#对传入的数据进行AES加密
	def encrypt(self,encryptData):
		loginData = self.login()
		#print loginData
		decryptURL = "http://console.saas.test.treefinance.com.cn/server/saas/console/tool/knife/crypto/encrypt"
		params = {
			"param":encryptData
		}

		try:
			#增加ensure_ascii后保证传递中文不会被转义
			req = self.session.post(decryptURL, data=json.dumps(params,ensure_ascii=False), headers=self.headers, verify=True)
			if req.status_code == 200:
				return req.text
				#res_json = json.loads(req.text)
			else:
				return "http error info:%s" %req.status_code
		except Exception, e:
			print 'encrypt error', e
			sys.exit(1)


if __name__ == "__main__":
	#部分变量初始化
	UserName = 'admin'  # 用户名
	PassWord = '123456'  # 密码
	decryptData = "2$UfadOZjOLVlGK2PAb6W8BQAAAAwA"
	encryptData = "13968043083"

	# if len (sys.argv) < 2:
	# 	print 'Usage: %s strData' % sys.argv[0]
	# 	sys.exit (-1)

	consoleLogin = console(UserName, PassWord)
	print consoleLogin.decrypt(decryptData)
	print consoleLogin.encrypt(encryptData)


