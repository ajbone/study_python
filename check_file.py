#!/usr/bin/env python  
#coding: utf-8  
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import requests
import json
import time
import os
import sys

from_addr = "ajbone@sina.com"
password = "zj13968043083"
#to_addr = ["zhang_jin@vobile.cn","yu_shu@vobile.cn"]
to_addr = "zhang_jin@vobile.cn"
smtp_server = "smtp.sina.com"

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

msg = MIMEText('New file is add.', 'plain', 'utf-8')
From = from_addr
msg['To'] = (u'系统邮件，请勿回复 <%s>' % to_addr)
To = to_addr
msg['Subject'] = Header(u'System Alarm !!! ', 'utf-8').encode()



def send_mail():
    server = smtplib.SMTP(smtp_server, 25)
    #server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()

def check_data():
    
    #keyword = "CREATE"
    f = open("/tmp/inotifywait.log","r")
    lines = f.readlines()
    if len(lines) == 0:
        sys.exit()
    else:
        for line in lines:
            #line_str = str(line)
            if line.find("CREATE"):
                print "Find new file"
                send_mail()  
                break
            else:
                print "Not find file"
    f.close()
    #print "#########",s["result"]
'''
    #content_id = s["result"]["meta"]["content_id"]
#print type(s)
#pint s["result"]["meta"]["content_id"]
    if s["result"] == None:
        print "result is null",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        send_mail()
    else:
        print "server is OK.",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    
    #print content_id
    if content_id <> "camery-video-20140403":
        print "send Alarm mail"
        send_mail()
'''
if __name__ == '__main__':
    check_data()





    
