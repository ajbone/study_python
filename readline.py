#!/usr/bin/env python
#coding: utf-8

import requests
import os

f = open("/Users/lazybone/workspaces/study_python/c.list","r")

url = "http://203.192.16.12/ingest/07/a6/XxjpsgC001649_20161231_TPPFN1A001.jpg"

#save_file = open("/Users/lazybone/workspaces/study_python/b.list","w")
for i in f.readlines():
	file_name = i.split('/')[-1]
	downloader_url = i[7:]

	print file_name
	requests.adapters.DEFAULT_RETRIES = 5
	response = requests.get(downloader_url, stream=True)
	status = response.status_code
	if status == 200:
    	total_size = int(response.headers['Content-Length'])
		with open(file_name, 'wb') as f1:
        	for chunk in response.iter_content(chunk_size=102400):
            	if chunk:
                	f1.write(chunk)
	#os.system("wget "+downloader_url+" -O "+"/tmp/"+file_name)

'''
with open(file_name, 'r') as f2:
    if isinstance(f2, file):
        length = os.fstat(f2.fileno()).st_size
        
if total_size == length:
    print "Success"
else:
    print "Fail"
'''

f.close()
#save_file.close()