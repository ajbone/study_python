#!/usr/bin/env python
#coding=utf8

import os
import re
import sys
import time
import threading
from ftplib import FTP
import datetime   



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

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print sys.argv[0]+":" +"date_time"
        #print sys.argv[0] + ' ftp_dir  local_dir'
        sys.exit(0)
    else:
        date_time = sys.argv[1]
    #date_time = "20170309"
    channels1 = ['BBC_World_News', 'CNN', 'Fox_News', 'NBC']
    for chl1 in channels1:
        ftpdir = 'video/%s1/%s' % (chl1,date_time)
        Total,file_list = check_ftp_file(ftpdir)
        print chl1,Total,file_list

    channels2 = ['sky','abc']
    for chl2 in channels2:
        ftpdir = 'video/%s/%s' % (chl2.upper(),date_time)
        Total,file_list = check_ftp_file(ftpdir)
        print chl2,Total,file_list
