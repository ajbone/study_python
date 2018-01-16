# -*- coding: UTF-8 -*-
"""Simple FunkLoad test


$Id$
"""
import json
import requests
import time
url = "http://pf.test.datatrees.cn/gateway"

def DateFormat(publishtime):
    print time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(publishtime))
    return time.strftime("%Y%m%d",time.localtime(publishtime))


def Caltime(date1,date2):
    date1=time.strptime(date1,"%Y-%m-%d %H:%M:%S")
    date2=time.strptime(date2,"%Y-%m-%d %H:%M:%S")
    date1=datetime.datetime(date1[0],date1[1],date1[2],date1[3],date1[4],date1[5])
    date2=datetime.datetime(date2[0],date2[1],date2[2],date2[3],date2[4],date2[5])
    return date2-date1

#调用start接口，获取TaskId
def ecommerce_start():
	payload = "appid=QATestabcdefghQA&uniqueId=qatest&deviceInfo=%7B%20%20%20%20%20%22positionData%22%3A%20%2222.648577%2C114.153408%22%7D"
	headers = {
	    'content-type': "application/x-www-form-urlencoded"
	    }

	response = requests.request("POST", url = url + "/ecommerce/start", data=payload, headers=headers)
	
	if response.status_code == 200:
		response.encoding = response.apparent_encoding
		results = json.loads(response.text)
		if results['success'] == True:
			results_taskId = results['data']['taskid']
			print results_taskId
			return results_taskId
		else:
			print "Not get taskId"
	else:
		print "http error info:%s" %response.status_code
		return

#根据获取的TaskId，间隔2秒循环调用轮询接口；
def ecommerce_acquisition():
	global taskId 
	taskId = ecommerce_start()
	#url_acquisition = "http://pf.test.datatrees.cn/gateway/ecommerce/acquisition"

	#print taskId
	cookie = "JSESSIONID%3DRZ13RdyYViU0WrGH2y3DhXJ6wT6h7JauthRZ13GZ00%3B%20JSESSIONID%3DRZ13NX2LVPc9tIelaqt8lhKPqPWNZ4authRZ13%3B%20session.cookieNameId%3DALIPAYJSESSIONID%3B%20NEW_ALIPAY_TIP%3D1%3B%20isg%3DAgQE8wJMAZp3_bUPP6SYpYaO1YT2HSiHKkeCqh6lkE-SSaQTRi34Fzrp_9Zr%3B%20unicard1.vm%3D%22K1iSL1gn5txVkqqu%2BY3UmA%3D%3D%22%3B%20ALIPAYBUMNGJSESSIONID%3DGZ00XpJTUg7uBoLq8xBlArsk8yCMBCmobilecodecGZ00%3B%20cna%3DckmpEXuqhh8CAXrgY9JIzpva%3B%20ALIPAYJSESSIONID.sig%3DT8DSw5-i17Dx9QXrXBsNdZD0WsnV97OH6EBW6owuhmY%3B%20JSESSIONID%3D32A89F604E46D0E2A2C7122D733E082D%3B%20mobileSendTime%3D-1%3B%20credibleMobileSendTime%3D-1%3B%20ctuMobileSendTime%3D-1%3B%20riskMobileBankSendTime%3D-1%3B%20riskMobileAccoutSendTime%3D-1%3B%20riskMobileCreditSendTime%3D-1%3B%20riskCredibleMobileSendTime%3D-1%3B%20riskOriginalAccountMobileSendTime%3D-1%3B%20ctoken%3DSUJcH77Btp47uF75%3B%20LoginForm%3Dalipay_login_auth%3B%20alipay%3DK1iSL1gn5txVkqqu%2BY3UmK8ohChHh5f14s2IEx4se8gAUJpO%3B%20CLUB_ALIPAY_COM%3D2088102730205673%3B%20iw.userid%3D%22K1iSL1gn5txVkqqu%2BY3UmA%3D%3D%22%3B%20ali_apache_tracktmp%3D%22uid%3D2088102730205673%22%3B%20_hvn_login%3D%220%2C3%2C1%22%3B%20zone%3DRZ13A%3B%20ALIPAYJSESSIONID%3DRZ136W1UHtVaPDPSia0sjvgO29m3c1authRZ13GZ00%3B%20sec%3D59a918f26deaf734bb3b121cc502a5583a0d0a21%3B%20spanner%3DP%2BeWt8x4MTWlw2qgjVSZMLiXiSRRy3M8%3B%20rtk%3DmuHpTj0Uw4834EA%2Ffu8D655bnN7qqcnZgEhaDaSOelwM7%2BkWDzC&accountNo=357166781%40qq.com&url=https%3A%2F%2Fmy.alipay.com%2Ftile%2Fservice%2Fportal%3Arecent.tile%3Ft%3D1495003306586%26_input_charset%3Dutf-8%26ctoken%3DNChEr_hoqtFMeBJI%26_output_charset%3Dutf-8"
	#payload = "appid=QATestabcdefghQA&timestamp=1493897461316&taskid=%s&cookie=%s&website=alipay.com&accountNo=%s" % (taskId,cookie,accountNo)
	payload = "appid=QATestabcdefghQA&website=alipay.com&timestamp=1493897461316&taskid=" + str(taskId) + "&cookie=" + cookie 
	headers = {
	    'jsessionid': "04FE9017EBC787D78C27F625423F7C65; sails.sid=s%3AUpMQHb5jUlMRyXE8PTULxW-tUgnrwG2g.hle1bFbc71X7qK3fDM5ISQVkBXt2lU0Gz2cXZf8RpOU",
	    'content-type': "application/x-www-form-urlencoded"
	    }

	response = requests.request("POST", url = url + "/ecommerce/acquisition", data=payload, headers=headers)


	#print response.status_code
	if response.status_code == 200:
		#print "11111111111111"
		response.encoding = response.apparent_encoding
		results = json.loads(response.text)
		if results['success'] == True:
			#print "22222222222222222"
			num = 0
			while True:
				directive_result = next_directive()
				num += 1
				print directive_result,num
				time.sleep(2)
				if (directive_result == "task_fail" or directive_result == "task_success" or directive_result == "callback_fail"):
					return directive_result
		else:
			print "Fail"

#轮询接口，定时扫描结果返回结果
def next_directive():
	#url = "http://pf.test.datatrees.cn/gateway/task/next_directive"

	payload = "appid=QATestabcdefghQA&version=1.0&timestamp=1493897461316&taskid=%s" % taskId
	headers = {
	'jsessionid': "04FE9017EBC787D78C27F625423F7C65; sails.sid=s%3AUpMQHb5jUlMRyXE8PTULxW-tUgnrwG2g.hle1bFbc71X7qK3fDM5ISQVkBXt2lU0Gz2cXZf8RpOU",
	'content-type': "application/x-www-form-urlencoded"
	}

	response = requests.request("POST", url = url + "/task/next_directive", data=payload, headers=headers)
	if response.status_code == 200:
		response.encoding = response.apparent_encoding
		results = json.loads(response.text)
		#print "333333333333333333"
		results_directive = results['data']['directive']
		#print "111111111111111111"
		#print results
		return results_directive
	else:
		print "http error info:%s" %response.status_code


if __name__ == '__main__':
	#ecommerce_start()
	date1 = DateFormat(time.time())
	print ecommerce_acquisition()
	date2 = DateFormat(time.time())
	
