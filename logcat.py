#!/usr/bin/env python
#coding:utf-8
#This script is aimed to grep logs by application(User should input a packageName and then we look up for the process ids then separate logs by process ids).

import os
import sys
import datetime

packageName=str(sys.argv[1])

time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

command = "adb shell ps | grep %s | awk '{print $2}'"%(packageName)
p = os.popen(command)
##for some applications,there are multiple processes,so we should get all the process id
pid = p.readline().strip()
filters = pid
while(pid != ""):
    pid = p.readline().strip()
    if (pid != ''):
        filters = filters +  "|" + pid
    print 'command = %s;filters=%s'%(command, filters)
if (filters != ''):
    cmd = 'adb logcat -v time | tee logcat/logcat-"%s".txt | grep --color=always -E "%s" '%(time,filters)
    print cmd
    os.system(cmd)