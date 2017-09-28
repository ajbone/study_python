#!/usr/bin/env python
#coding: utf-8
'''
unittest interface
@author: zhang_jin
@version: 1.0
@see:http://www.python-requests.org/en/master/
'''

import unittest
import json
import traceback
import requests
import config as cf




class MyTestSuite(unittest.TestCase):
	"""docstring for MyTestSuite"""
	#@classmethod
	def sedUp(self):
		print "start..."
    #图片匹配统计
	def test_image_match_001(self):

		response = requests.request("POST", url, headers=headers, params=querystring)
		if response.status_code == 200:
			response.encoding = response.apparent_encoding
			results = json.loads(response.text)
			#预期结果与实际结果校验，调用result_statistics模块
			result_statistics.test_result(results,639)
		else:
			print "http error info:%s" %response.status_code



	def tearDown(self): 
		pass


if __name__ == '__main__':
    #image_match_Logger = ALogger('image_match', log_level='INFO')

	#构造测试集合
	suite=unittest.TestSuite()
	suite.addTest(MyTestSuite("test_image_match_001"))
	suite.addTest(MyTestSuite("test_text_match_001"))
	
    #执行测试
	runner = unittest.TextTestRunner()
	runner.run(suite)
	print "success case:",result_statistics.num_success
	print "fail case:",result_statistics.num_fail
	#unittest.main()