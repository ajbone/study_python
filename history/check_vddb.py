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


    from_addr = "xxx"
    password = "xx"
to_addr = ["xx","xxx"]
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


def get_attrvalue(node, attrname):
    return node.getAttribute(attrname) if node else ''

def get_nodevalue(node, index = 0):
    return node.childNodes[index].nodeValue if node else ''


def get_xmlnode(node, name):
    return node.getElementsByTagName(name) if node else []

def parseResult(out):
    #获取返回结果中的master_uuid值，并存入list。
    #ret,out,err = queryVddb(image_cmdline)

    dom = xml.dom.minidom.parseString(out)

    root = dom.documentElement
    itemlist = root.getElementsByTagName('master_uuid')
    match_nodes = get_xmlnode(root, 'match')
    #print "match_nodes:", match_nodes
    master_uuid_list=[]
    for node in match_nodes: 
        node_master_uuid = get_xmlnode(node, 'master_uuid')
        match_master_uuid =get_nodevalue(node_master_uuid[0])
        master_uuid_list.append(match_master_uuid)
    return master_uuid_list
    #item = itemlist[0]
    #result_meta_uuid = item.firstChild.data
    
    #return result_meta_uuid


def checkData():
    image_result_flag = 0

    #当返回多个结果时，只要包含在结果list中，就返回flag=1为真。
    image_ret,image_out,image_err = queryVddb(image_cmdline)
    image_meta_uuid_list = parseResult(image_out)

    for image_meta_uuid in  parseResult(image_out):
        image_result_flag = 1
    #print "image uuid: %s" % image_result_meta_uuid
    
    av_result_flag = 0
    
    av_ret,av_out,av_err = queryVddb(av_cmdline)
    av_meta_uuid_list = parseResult(av_out)
    
    for av_meta_uuid in av_meta_uuid_list:
        av_result_flag = 1
    #print "av uuid: %s" % av_result_meta_uuid

    #image_ret 为0时表示查询结果为True，反之为False
    if (image_ret != 0 or av_ret != 0):
	print "Vddb Server is Fail,Query fail,Please check it.",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	#send_mail()
    elif (image_ret == 0 and av_ret == 0 and image_result_flag == 1 and av_result_flag ==1 ):
    	print "Vddb Server is OK.",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	return
    else:
        print "Vddb Server is Fail,Please check it.",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	#send_mail()

#def main():
#    querier = Querier()
#    querier.runCmdline(cmdline)



if __name__ == '__main__':
    checkData()

