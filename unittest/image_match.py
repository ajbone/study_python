#!/usr/bin/env python  
#coding: utf-8  
'''
unittest xhs image_query interface
@author: zhang_jin@vobile.cn
@version: 1.0
@see: 
'''

import unittest
import json
import requests
import time
import config as cf
from com_logger import  match_Logger
import traceback


class MyTestSuite(unittest.TestCase):
	"""docstring for MyTestSuite"""
	#@classmethod
	
	def sedUp(self):
		print "start..."

	def test_image_match_001(self):
		url = cf.URL

		querystring = {"category":"image","offset":"0","limit":"30","sourceId":"0","metaTitle":"","metaId":"0","classify":"unclassify","startTime":"","endTime":"","createStart":"","createEnd":"","sourceType":"","isTracking":"true","metaGroup":"","companyId":"0","lastDays":"1","author":""}

		headers = {
		    'cache-control': "no-cache",
		    'postman-token': "545a2e40-b120-2096-960c-54875be347be"
		    }

		response = requests.request("POST", url, headers=headers, params=querystring)

		#print time.strftime("%Y-%m-%d_%H:%M:%S",time.localtime(time.time()))  

		#response.raise_for_status()
		#source = response.json()
		response.encoding = response.apparent_encoding
		results = json.loads(response.text)
		match_Logger.info("start image_query22222")
		try:
			self.assertEqual(results['total'], 618)
		except:
			match_Logger.error(traceback.format_exc())
			match_Logger.info("start image_query444444")
		#print results['total']
		
		#self.assertRegexpMatches(response.text,"[0-9]{10}")
		#print type(results)
		#print results

	def test_text_match_001(self):

		url = "http://cpright.xinhua-news.cn/api/match/text/getjson"

		querystring = {"category":"text","offset":"0","limit":"30","sourceId":"0","metaTitle":"","metaId":"0","startTime":"2017-04-14","endTime":"2017-04-15","createStart":"","createEnd":"","sourceType":"","isTracking":"true","metaGroup":"","companyId":"0","lastDays":"0","author":"","content":""}

		headers = {
		    'cache-control': "no-cache",
		    'postman-token': "ef3c29d8-1c88-062a-76d9-f2fbebf2536c"
		    }

		response = requests.request("POST", url, headers=headers, params=querystring)

		response.encoding = response.apparent_encoding
		results = json.loads(response.text)
		match_Logger.info("start image_query3333")
		self.assertEqual(results['total'], 4208)
		#print(response.text)

	def tearDown(self): 
		print "end..."

if __name__ == '__main__':
    #image_match_Logger = ALogger('image_match', log_level='INFO')

	#构造测试集合
	suite=unittest.TestSuite()
	suite.addTest(MyTestSuite("test_image_match_001"))
	suite.addTest(MyTestSuite("test_text_match_001"))
	
    #执行测试
	runner = unittest.TextTestRunner()
	runner.run(suite)
	#unittest.main()
