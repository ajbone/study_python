#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
import datetime

def DateFormat(publishtime):
    return time.strftime("%Y%m%d %H:%M:%S",time.localtime(publishtime ))

print DateFormat(time.time())

i = datetime.datetime.now()
print i