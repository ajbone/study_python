#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
def pingtest():
    ips=""
    begin_ip = 10
    end_ip = 150
    print ("start ping test.....")
    while begin_ip < end_ip:
       p = subprocess.call('timeout 5 ping -c 1 192.168.1.%s' % begin_ip,shell=True,stdout=open('/dev/null','w'),stderr=subprocess.STDOUT)
       if p == 0:
           print "192.168.1.%s is alive" %begin_ip
       else:
           print "192.168.1.%s is down" %begin_ip
       begin_ip=begin_ip+1
   
if __name__=="__main__":
    pingtest()
