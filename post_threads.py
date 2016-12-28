#!/usr/bin/python
#coding=utf8

import sys
import os
import urllib, urllib2
import requests
from urllib2 import Request, urlopen, URLError, HTTPError
import threading
from random import random

file = open('a.list')
lines = file.readlines()
result=[]
for line in lines:
    line = line.strip('\n')
    result.append(line)
#print result

def post_web(phone_num):
    url = "http://znewsapp-c.pala-pala.net/voteFlow/save_shoot"
    #data = {'match': 'yes','user_id': '8343132486','country': u"china",'province': u"zhejiang",'city': u"hangzhou",'file_id': "test_dammy_file",'result[content_id]': '0af00709-49b9-47e4-833c-2fc50f5b0e38'}
    #req = requests.post(url=url,data=data)
    print "phone num is :%s \n" % (phone_num)
    #print req.status_code

threads = []

for i in range(len(result)):
    #a=str(15967147890+i)
    a=result[i]
    print a
    t1 = threading.Thread(target=post_web,args=([a]))
    threads.append (t1)
if __name__ == '__main__':
    for t in threads:
        #t.setDaemon(True)   
        t.start()
