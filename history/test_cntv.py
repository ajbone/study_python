#!/usr/bin/env python
#coding: utf-8

import os
import re
import sys
import time
import threading
from ftplib import FTP
import datetime   
  
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import json
import traceback


from_addr = "xxx"
password = "xxx"
to_addr = ["xxx"]
#to_addr = ["xxx","jin_le@vobile.cn"]
smtp_server = "smtp.sina.com"

class SendMailExcept(Exception):
    pass

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

def send_mail():
    if  os.path.exists('/tmp/daily.txt') == True:
        try:
            with open("/tmp/daily.txt",'rb') as f1:
                text_content = f1.read()
                msg = MIMEText(text_content, 'plain', 'utf-8')
                From = from_addr
                msg['To'] = (u'来自张金发送的系统邮件，请勿回复 <%s>' % to_addr)
                To = to_addr
                msg['Subject'] = Header(u'Upload video for WuXiTV Daily', 'utf-8').encode()
                server = smtplib.SMTP(smtp_server, 25)
                #server.set_debuglevel(1)
                server.login(from_addr, password)
                server.sendmail(from_addr, to_addr, msg.as_string())
                server.quit()
        except:
            raise SendMailExcept(traceback.format_exc())
    else:
        raise SendMailExcept("###############222222")
            

def DateFormat(publishtime):
    print time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(publishtime))
    return time.strftime("%Y%m%d",time.localtime(publishtime))

def check_ftp_file(remote_dir):
    #locallist = get_local_mp4_file_list(local_dir)
    bufsize = 1024  # 设置的缓冲区大小
    ftp = FTP('','','','',1800) # set timeout is 1800 s
    print '========================================================================'
    print 'connecting ftp server'
    try:
        ftp.connect('122.192.67.72', '12021')                                                                                                                                        
        ftp.login('fubotong', '78ajdfaldfl_adf')
        print 'FTP login'
        try:
        	ftp.cwd(remote_dir)
        except:
        	print 'Remote dir :' + remote_dir + ' is not exists.'
        	ftp.quit()
        	print "FTP logout"
        	return
        #print ftp.getwelcome()  # 输出欢迎信息
        ftpfilelist = ftp.nlst()  # 获得文件列表
        return len(ftpfilelist),ftpfilelist
    except:
        print 'FTP login failure'
        return


def main():
    date_now = DateFormat(time.time())
    with open("/tmp/daily.txt",'wb') as f:
        f.write(date_now + " " + "\n")
        #print data_now
        channels = ['sky','abc']
        for chl in channels:
            ftpdir = 'video/%s/%s' %(chl.upper(), date_now)
            Total = check_ftp_file(ftpdir)
            f.write(chl+" Total: " + str(Total) + "\n")
            #f.write(str(Total))
            #f.write("\n")
        
        channels2 = ['BBC_World_News', 'CNN', 'Fox_News', 'NBC']
        for chl2 in channels2:
            ftpdir = 'video/%s1/%s' % (chl2,date_now)
            Total2 = check_ftp_file(ftpdir)
            f.write(chl2+" Total: " + str(Total) + "\n")
        
    #with open("/tmp/daily.txt",'rb') as f2:
    #    print f2.read()
    send_mail()     

#date_yest = DateFormat(time.time()-24*3600)

if __name__ == '__main__':
    try:
        main()
    except SendMailExcept, e:
        sys.exit()
    except:
        traceback.print_exc()










