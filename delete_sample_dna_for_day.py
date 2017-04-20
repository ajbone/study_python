#!/usr/bin/env python  
#coding: utf-8  
'''
Delete dna file
@author: zhang_jin@vobile.cn
@version: 1.0
@see: 
'''

import os
import time
import syslog

for f in os.listdir('/vobiledata/xhs/dna/'):
    for f1 in os.listdir(os.path.join('/vobiledata/xhs/dna/',f)):
        for f2 in os.listdir(os.path.join('/vobiledata/xhs/dna/',f, f1)):
            f3 = os.path.join('/vobiledata/xhs/dna/',f, f1,f2)
            filedate = os.path.getmtime(f3)
            now_date = time.time()
            #month = time.gmtime(os.stat(f3).st_ctime).tm_mon
            #day = time.gmtime(os.stat(f3).st_ctime).tm_mday
            num1 = now_date-filedate
            if num1 >= 30*60*60*24:
                #print f3, month, day
                os.system('rm %s' %f3)
                syslog.syslog("delete file %s" %f3)