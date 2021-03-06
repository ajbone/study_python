#!/usr/bin/env python
#coding: utf-8
'''
unittest xhs image_query interface
@author: zhang_jin
@version: 1.0
@see:
'''

import unittest
import json
import traceback
import requests
import time
import config as cf
from com_logger import  match_Logger
#from result_statistics import *
import result_statistics
class MyTestSuite(unittest.TestCase):
	"""docstring for MyTestSuite"""
	#@classmethod
	def sedUp(self):
		print "start..."
    #图片匹配统计
	def test_image_match_001(self):
		url = cf.URL

		querystring = {
            "category": "image",
            "offset": "0",
		    "limit": "30",
		  "sourceId": "0",
		  "metaTitle": "",
		  "metaId": "0",
		  "classify": "unclassify",
		  "startTime": "",
		  "endTime": "",
		  "createStart": "",
		  "createEnd": "",
		  "sourceType": "",
		  "isTracking": "true",
		  "metaGroup": "",
		  "companyId": "0",
		  "lastDays": "1",
		  "author": ""
		}
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
		#self.assertEqual(results['total'], 888)
		results_total = results['total']
		print "Testcase test_text_match_001"
		result_statistics.test_result(results,936)
		'''
		try:
			self.assertEqual(results['total'], 888)
		except:
			match_Logger.error(traceback.format_exc())
		#print results['total']
		
		#self.assertRegexpMatches(response.text,"[0-9]{10}")
		#print type(results)
		#print results
        '''
    #文字匹配数据统计
	def test_text_match_001(self):

		text_url = cf.URL2

		querystring = {
		    "category": "text",
		    "offset": "0",
		    "limit": "30",
		    "sourceId": "0",
		    "metaTitle": "",
		    "metaId": "0",
		    "startTime": "2017-04-14",
		    "endTime": "2017-04-15",
		    "createStart": "",
		    "createEnd": "",
		    "sourceType": "",
		    "isTracking": "true",
		    "metaGroup": "",
		    "companyId": "0",
		    "lastDays": "0",
		    "author": "",
		    "content": ""
		}
		headers = {
		    'cache-control': "no-cache",
		    'postman-token': "ef3c29d8-1c88-062a-76d9-f2fbebf2536c"
		    }

		response = requests.request("POST", text_url, headers=headers, params=querystring)

		response.encoding = response.apparent_encoding
		results = json.loads(response.text)
		match_Logger.info("start image_query3333")
		results_total = results['total']
		print "Testcase test_text_match_001"
		result_statistics.test_result(results,4521)
		#self.assertEqual(results['total'], 4208)
		#print(response.text)

	def tearDown(self): 
		pass

if __name__ == '__main__':
    #image_match_Logger = ALogger('image_match', log_level='INFO')

	#构造测试集合
	suite=unittest.TestSuite()
	suite.addTest(MyTestSuite("test_image_match_001"))
	suite.addTest(MyTestSuite("test_text_match_001"))
	suite.addTest(MyTestSuite("test_text_match_001"))
	
    #执行测试
	runner = unittest.TextTestRunner()
	runner.run(suite)
	print "success case:",result_statistics.num_success
	print "fail case:",result_statistics.num_fail
	#unittest.main()
