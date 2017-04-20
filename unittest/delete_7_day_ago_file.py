#!/usr/bin/env python  
#coding: utf-8  
'''
Delete 7 days ago *.ts file
@author: zhang_jin@vobile.cn
@version: 1.0
@see: 
'''

import os
import time
import datetime

#SOURCE_DIR = '/vobiledata/converter/source_abc/'
SOURCE_DIR = "/Users/lazybone/workspaces/study_python/unittest/"

f =  list(os.listdir(SOURCE_DIR))
for i in range(len(f)):
    filemt = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(os.stat(SOURCE_DIR + f[i]).st_mtime))
    filemt_timestamp = int(time.mktime(time.strptime(filemt,'%Y-%m-%d %H:%M:%S')))
    date_now = time.time()
    num1 =(date_now - filemt_timestamp)/60/60/24
    if num1 >= 7:
        #os.remove(SOURCE_DIR + f[i])
        print("已删除文件：%s " %  (SOURCE_DIR + f[i]))
else:
    print("there are no file more than 30 days")