#!/usr/bin/env python
# -*- coding: utf-8 -*-

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import requests
import json
import time

import subprocess
from subprocess import *
import xml.dom.minidom


from_addr = "ajbone@sina.com"
password = "zj5704716"
to_addr = ["zhang_jin@vobile.cn","su_rongyao@vobile.cn"]
smtp_server = "smtp.sina.com"

av_meta_uuid ="8f09defe-c1f3-11e6-b90d-48fd8eaeed8e"
image_meta_uuid = "906f4786-c273-11e6-91e6-48fd8eaeed8e"
av_cmdline = "/root/vddb_v5.10.0.0_debian8_deploy/module/vdna_query_v5.10.0.0_linux_x86_32/bin/vdna_query -s 203.192.16.16 -u admin -w 'Vddb0909&'  -Tdna -i /home/vdna/49_0062.0.dna"
image_cmdline = "/root/vddb_v5.10.0.0_debian8_deploy/module/vdna_query_v5.10.0.0_linux_x86_32/bin/vdna_query -s 203.192.16.16 -u admin -w 'Vddb0909&' --profile D  -Tdna -i /home/vdna/test1.idna"

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

msg = MIMEText('Xinhuashe Vddb Server is down,please check it.', 'plain', 'utf-8')
From = from_addr
msg['To'] = (u'系统邮件，请勿回复 <%s>' % to_addr)
To = to_addr
msg['Subject'] = Header(u'Xinhua Alarm !!! ', 'utf-8').encode()


def send_mail():
    server = smtplib.SMTP(smtp_server, 25)
    #server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()

#class queryier(object):


def queryVddb(cmdline):
    p = subprocess.Popen(cmdline,stdout=PIPE, stderr=PIPE, shell=True)
    ret = p.wait()
    out, err = p.communicate()
    return ret, out, err


def parseResult(out):
    #ret,out,err = queryVddb(image_cmdline)

    dom = xml.dom.minidom.parseString(out)

    root = dom.documentElement
    itemlist = root.getElementsByTagName('master_uuid')

    item = itemlist[0]
    result_meta_uuid = item.firstChild.data
    
    return result_meta_uuid


def checkData():
    image_ret,image_out,image_err = queryVddb(image_cmdline)
    image_result_meta_uuid = parseResult(image_out)
    #print "image uuid: %s" % image_result_meta_uuid

    av_ret,av_out,av_err = queryVddb(av_cmdline)
    av_result_meta_uuid = parseResult(av_out)
    #print "av uuid: %s" % av_result_meta_uuid


    if (image_ret != 0 or av_ret != 0):
	print "Vddb Server is Fail,Query fail,Please check it.",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	send_mail()
    elif (image_ret == 0 and av_ret == 0 and image_result_meta_uuid == image_meta_uuid and av_result_meta_uuid == av_meta_uuid ):
    	print "Vddb Server is OK.",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	return
    else:
        print "Vddb Server is Fail,Please check it.",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	send_mail()


#def main():
#    querier = Querier()
#    querier.runCmdline(cmdline)



if __name__ == '__main__':
    checkData()
