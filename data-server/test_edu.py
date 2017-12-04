#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib
import urllib2
import requests
import json


def testEducationQuery(userName, identityNumber):
    test_data = {
        "appid": "QATestabcdefghQA",
        "version": "1.0.0",
        "timestamp": 1234123,
        "type": 1,
        "identityNumber": identityNumber,
        "userName": userName
    }

    return test_data


if __name__ == '__main__':
    file = open("/tmp/test.txt")

    while 1:
        line = file.readline().strip()
        if not line:
            break
        line = line.split(",")

        test_data = testEducationQuery(line[0].strip(), line[1].strip())
        test_data_urlencode = urllib.urlencode(test_data)
        test_url = "http://192.168.5.25:8168/data/education"
        #req = urllib2.Request(url=test_url, data=test_data_urlencode)
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1f148798-1a74-db27-eb10-85726d08de8d"
        }

        response = requests.request("POST", url=test_url, data=test_data_urlencode, headers=headers)

        print(response.text)
        # result = json.dumps(req, sort_keys=True, indent=4, separators=(',', ': '), encoding='utf-8')
        print "finish!"