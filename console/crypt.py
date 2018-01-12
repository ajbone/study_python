#!/usr/bin/env python
#coding: utf-8

import requests


def decrypt():
	url = "http://console.saas.test.treefinance.com.cn/server/saas/console/tool/knife/crypto/decrypt"

	# payload = "{\"param\":\"2$UfadOZjOLVlGK2PAb6W8BQAAAAwA\"}"

	params = {"param":"2$UfadOZjOLVlGK2PAb6W8BQAAAAwA"}

	payload = json.dumps(params,ensure_ascii=False)

	headers = {
		'content-type': "application/json"
	}

	response = requests.request("POST", url, data=payload, headers=headers)

	print(response.text)

def encrypt():
