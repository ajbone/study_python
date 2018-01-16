#!/usr/bin/env python
#coding=utf8
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import requests
import json
import time

from_addr = "xxx"
password = "xx"
#to_addr = ["xxx","yu_shu@vobile.cn"]
to_addr = "xxx"
smtp_server = "smtp.sina.com"


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

with open("/tmp/a.txt",'r') as f:
	msg = MIMEText(f.read(), 'plain', 'utf-8')
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

if __name__ == '__main__':
    send_mail()



'''
for links in soup.find_all('a'):
	print links.get('href')
'''


