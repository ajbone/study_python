#!/usr/bin/env python
#coding: utf-8

import requests
import os

url = "http://203.192.16.12/ingest/07/a6/XxjpsgC001649_20161231_TPPFN1A001.jpg"

requests.adapters.DEFAULT_RETRIES = 5
response = requests.get(url, stream=True)
status = response.status_code
if status == 200:
    total_size = int(response.headers['Content-Length'])
    with open('download.jpg', 'wb') as of:
        for chunk in response.iter_content(chunk_size=102400):
            if chunk:
                of.write(chunk)

print total_size

with open('download.jpg', 'r') as f:
    if isinstance(f, file):
        length = os.fstat(f.fileno()).st_size
        
if total_size == length:
    print "Success"
else:
    print "Fail"