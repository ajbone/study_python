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
import xml.dom.minidom


from_addr = "ajbone@sina.com"
password = "zj13968043083"
to_addr = "zhang_jin@vobile.cn"
smtp_server = "smtp.sina.com"

av_meta_uuid ="8f09defe-c1f3-11e6-b90d-48fd8eaeed8e"
image_meta_uuid = "8f09defe-c1f3-11e6-b90d-48fd8eaeed8e"
av_cmdline = "/root/vddb_v5.10.0.0_debian8_deploy/module/vdna_query_v5.10.0.0_linux_x86_32/bin/vdna_query -s 203.192.16.16 -u admin -w 'Vddb0909&'  -Tdna -i /home/vdna/49_0062.0.dna"
image_cmdline = "/root/vddb_v5.10.0.0_debian8_deploy/module/vdna_query_v5.10.0.0_linux_x86_32/bin/vdna_query -s 203.192.16.16 -u admin -w 'Vddb0909&' --profile D  -Tdna -i /home/vdna/test1.idna"

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

msg = MIMEText('Paipaibao server is down,please check it.', 'plain', 'utf-8')
From = from_addr
msg['To'] = (u'系统邮件，请勿回复 <%s>' % to_addr)
To = to_addr
msg['Subject'] = Header(u'Paipaibao Alarm !!! ', 'utf-8').encode()


def send_mail():
    server = smtplib.SMTP(smtp_server, 25)
    #server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()

#class queryier(object):


def queryVddb(cmdline):
    p = subprocess.Popen(cmdline,  shell=True)
    ret = p.wait()
    out, err = p.communicate()
    return ret, out, err


def checkResult():
    ret,out,err = queryVddb(av_cmdline)

    dom = xml.dom.minidom.parse(out)

    root = dom.documentElement
    itemlist = root.getElementsByTagName('master_uuid')

    item = itemlist[0]
    result_meta_uuid = item.firstChild.data

    if ret != 0:
        break
    elif (ret == 0 and result_meta_uuid ==av_meta_uuid):
        print "success"
    else
        print "fail"



#def main():
#    querier = Querier()
#    querier.runCmdline(cmdline)



if __name__ == '__main__':
    checkResult()
