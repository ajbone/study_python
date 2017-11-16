# -*- coding: UTF-8 -*-
"""Simple FunkLoad test


$Id$
"""
import json
import requests
import time
url = "http://pf.test.datatrees.cn/gateway"

def ecommerce_start():
	url = "http://pf.test.datatrees.cn/gateway/ecommerce/start"
	payload = "appid=QATestabcdefghQA&uniqueId=qatest&deviceInfo=%7B%20%20%20%20%20%22positionData%22%3A%20%2222.648577%2C114.153408%22%7D"
	headers = {
	    'content-type': "application/x-www-form-urlencoded"
	    }

	response = requests.request("POST", url = url + "/ecommerce/start", data=payload, headers=headers)
	print url
	
	if response.status_code == 200:
		response.encoding = response.apparent_encoding
		results = json.loads(response.text)
		if results['success'] == True:
			results_taskId = results['data']['taskid']
			return results_taskId
		else:
			print "Not get taskId"
	else:
		print "http error info:%s" %response.status_code

def ecommerce_acquisition():

	#url = "http://pf.test.datatrees.cn/gateway/ecommerce/acquisition"
	payload = "appid=QATestabcdefghQA&timestamp=1493897461316&taskid=88226832398954496&cookie=session.cookieNameId%3DALIPAYJSESSIONID%3B%20NEW_ALIPAY_TIP%3D1%3B%20isg%3DAgQE8wJMAZp3_bUPP6SYpYaO1YT2HSiHKkeCqh6lkE-SSaQTRi34Fzrp_9Zr%3B%20mobileSendTime%3D-1%3B%20credibleMobileSendTime%3D-1%3B%20ctuMobileSendTime%3D-1%3B%20riskMobileBankSendTime%3D-1%3B%20riskMobileAccoutSendTime%3D-1%3B%20riskMobileCreditSendTime%3D-1%3B%20riskCredibleMobileSendTime%3D-1%3B%20riskOriginalAccountMobileSendTime%3D-1%3B%20unicard1.vm%3D%22K1iSL1gn5txVkqqu%2BY3UmA%3D%3D%22%3B%20ALIPAYBUMNGJSESSIONID%3DGZ00XpJTUg7uBoLq8xBlArsk8yCMBCmobilecodecGZ00%3B%20cna%3DckmpEXuqhh8CAXrgY9JIzpva%3B%20_hvn_login%3D%220%2C3%2C1%22%3B%20ctoken%3DPgoqlvwtEZbkXalA%3B%20LoginForm%3Dtrust_login_taobao%3B%20alipay%3D%22K1iSL1gn5txVkqqu%2BY3UmK8ohChHh5f14s2IEx4se8gAUI3L1A%3D%3D%22%3B%20CLUB_ALIPAY_COM%3D2088102730205673%3B%20iw.userid%3D%22K1iSL1gn5txVkqqu%2BY3UmA%3D%3D%22%3B%20ali_apache_tracktmp%3D%22uid%3D2088102730205673%22%3B%20iw.nick%3D%22cDkyiTCx0AU%3D%22%3B%20iw.partner%3D%22Lfo3AA%3D%3D%22%3B%20zone%3DRZ13A%3B%20CHAIR_SESS%3DK6iO619fGWnMOmQO_wFsrPXQqfhUc6-BYaJDO5gKtUK6WAxaYnOcRML_iigB319j2ydvtPJYXPbB6nK42aifZD5Ebkn44b37HZdddFk7ORxhYQ6pgO8KiwGiqslTR-yseffdgVfEyJd3xbzoE_ZXsw%3D%3D%3B%20spanner%3DtIbQnx9IhvEcSYdU8vlpl4kQQx4%2B3il5%3B%20ALIPAYJSESSIONID%3DRZ13W3rgV7CRuhnw4U2ZgDLVUlDDs3authRZ13GZ00%3B%20ALIPAYJSESSIONID.sig%3DDDQvT64Vlxph0zirsKX5FibnbpwCEW_TdbjHeKSZfZA%3B%20rtk%3DOd8B2TJ9Npe5%2BIXZRd7Cn3WUO7pcnNk6zfIaCpxmic1y84BzR01&url=https%3A%2F%2Fmy.alipay.com%2Ftile%2Fservice%2Fportal%3Arecent.tile%3Ft%3D1495003306586%26_input_charset%3Dutf-8%26ctoken%3DNChEr_hoqtFMeBJI%26_output_charset%3Dutf-8&website=alipay.com&accountNo=357166781%40qq.com"
	headers = {
	    'jsessionid': "04FE9017EBC787D78C27F625423F7C65; sails.sid=s%3AUpMQHb5jUlMRyXE8PTULxW-tUgnrwG2g.hle1bFbc71X7qK3fDM5ISQVkBXt2lU0Gz2cXZf8RpOU",
	    'content-type': "application/x-www-form-urlencoded"
	    }

	response = requests.request("POST", url = url + "/ecommerce/acquisition", data=payload, headers=headers)
	if response.status_code == 200:
		response.encoding = response.apparent_encoding
		results = json.loads(response.text)
		if results['success'] == True:
			while True:
				directive_result = next_directive()
				time.sleep(2)
				if (directive_result != "task_fail" or directive_result != "task_success" or directive_result != "callback_fail"):
					return directive_result
		else:
			print "Fail"

def next_directive():
	#url = "http://pf.test.datatrees.cn/gateway/task/next_directive"

	payload = "appid=QATestabcdefghQA&version=1.0&timestamp=1493897461316&taskid=88226832398954496"
	headers = {
	'jsessionid': "04FE9017EBC787D78C27F625423F7C65; sails.sid=s%3AUpMQHb5jUlMRyXE8PTULxW-tUgnrwG2g.hle1bFbc71X7qK3fDM5ISQVkBXt2lU0Gz2cXZf8RpOU",
	'content-type': "application/x-www-form-urlencoded"
	}

	response = requests.request("POST", url = url + "/task/next_directive", data=payload, headers=headers)
	if response.status_code == 200:
		response.encoding = response.apparent_encoding
		results = json.loads(response.text)
		results_directive = results['data']['directive']
		return results_directive
	else:
		print "http error info:%s" %response.status_code


if __name__ == '__main__':
	ecommerce_start()
	print ecommerce_acquisition()




	
