#!/usr/bin/env python

import os
import sys
import time
import shutil

import threading
import ConfigParser
from ftplib import FTP 
reload(sys)
sys.setdefaultencoding('utf-8')

user_module_path = os.path.dirname(os.path.realpath(__file__))
SYSCONFIG = os.path.join(user_module_path, '../etc/system.conf')

# simple config parse
#config = ConfigParser.ConfigParser()
#config.read (config_file)
#xx = config.get('xx', 'xx')

if len(sys.argv) != 2:
    print '%s channel' %sys.argv[0]
    sys.exit(0)
channel = sys.argv[1]
target_path = '/vobiledata/qatest/target'
tmp_path = os.path.join('/vobiledata/qatest/tmp/', channel)
if not os.path.exists(tmp_path):
    os.makedirs(tmp_path)
save_path = os.path.join('/vobiledata/qatest/tmp/target/', channel)
if not os.path.exists(save_path):
    os.makedirs(save_path)
source_path = os.path.join('/vobiledata/rtfpvideo/', channel)
success_path = os.path.join('/vobiledata/qatest/success/', channel)
if not os.path.exists(success_path):
    os.makedirs(success_path)

sleep_time = 5 * 60

#TODO
#ftp=FTP() 
#ftp.connect('58.215.162.7','12021')
#ftp.login('fubotong','78ajdfaldfl_adf')

'''
300s length video, ex: 12.1485388800000.1485389100000.mp4
merge to 1800s length video
total 48 videos one day
'''

def time_change1(timestamp):
    #14853888000 to 20170126
    timestamp = str(timestamp)
    return int(os.popen("date -d @%s  +%%Y%%m%%d" %timestamp).read().strip())

def time_change2(timestamp):
    # 20170126 to 1485360000
    return int(time.mktime(time.strptime(str(timestamp),"%Y%m%d")))

def get_time_year(timestamp):
    return os.popen('date -d @%s  +%%Y' %timestamp).read().strip()

def get_time_month(timestamp):
    return os.popen('date -d @%s  +%%m' %timestamp).read().strip()

def get_time_day(timestamp):
    return os.popen('date -d @%s  +%%d' %timestamp).read().strip()

def get_time_hour(timestamp):
    return os.popen('date -d @%s  +%%H' %timestamp).read().strip()

def get_time_minute(timestamp):
    return os.popen('date -d @%s  +%%M' %timestamp).read().strip()

def in_success_dir(checked_dir):
    if checked_dir in os.listdir(success_path):
        return True
    return False

def ctime_compare(x, y):
    stat_x = int(x.split('.')[1])
    stat_y = int(y.split('.')[1])
    if stat_x < stat_y:
        return -1
    elif stat_x > stat_y:
        return 1
    else:
        return 0

def parse_timestamp(filename):
    #12.1485388800000.1485389100000.mp4
    print 'parse filename: ' + filename
    if len(filename.split('.')) < 3:
        return
    iid = filename.split('.')[0] 
    t1  = filename.split('.')[1][0:10] # get 1485388800 length
    t2  = filename.split('.')[2][0:10]
    if int(t1) < time.time() - 24*3600:
        return
    t1 =  int(t1) + 8*3600
    source_start_time = time_change2(time_change1(t1))
    print '===='+str(time.time())+' now ====='
    print 'source_start_time: ' + str(source_start_time)
    for i in range(0, 48):
        start_time = source_start_time + i * 1800
        end_time = start_time + 1800
        to_touch_dir = os.path.join(tmp_path, '%s_%s' %(start_time, end_time))
        if in_success_dir(to_touch_dir):
            print 'dir: %s in success, pass...' %to_touch_dir
            continue

        if (t1 >= start_time-60 and t1 < end_time-60):
            to_touch_file = os.path.join(to_touch_dir, filename)
            if(not os.path.exists(to_touch_file)):
                if not os.path.exists(to_touch_dir):
                    os.makedirs(to_touch_dir)
                print 'to touch file: ', to_touch_file
                open(to_touch_file,'w').write('')
def DateFormat(publishtime):
    return time.strftime("%Y%m%d",time.localtime(publishtime))
def get_last_name():
    return DateFormat(time.time()-24*3600)

def find_todo_videos(source_path):
    while True:
        all_video_list = os.listdir(source_path)
        all_video_list.sort(ctime_compare)
        last_name = get_last_name()
        print 'last_name is: ' + str(last_name)
        last_name_time = time_change2(last_name) * 1000
        print 'last_name_time is: ', last_name_time
        new_all_video_list = []
        for video in all_video_list:
            if int(video.split('.')[1]) > last_name_time:
                new_all_video_list.append(video)
        all_video_list = new_all_video_list
        print len(all_video_list)

        for video in all_video_list:
            if video.startswith('.'):
                continue
            parse_timestamp(video)

        print 'finish find_todo_videos this round...'

        time.sleep(sleep_time)

def merge_todo_videos(source_path):
    while True:
        for todo_dir in os.listdir(tmp_path):
            print '=====TODO DIR IS======='+ todo_dir
            #if int(todo_dir) < 20170301:
            #    continue
            
            todo_path = os.path.join(tmp_path, todo_dir)
            can_merge = True
            to_check_list = os.listdir(todo_path)
            for video in to_check_list:
                source_video = os.path.join(source_path, video)
                if not os.path.exists(source_video):
                    continue
                mtime = os.path.getmtime(source_video)
                now = time.time()
                if now - mtime < 1800:
                    print 'file %s not time to merge...' %(source_path)
                    can_merge = False

            if can_merge == True:
                merge_video(to_check_list)
                #mv to success
                if not os.path.exists(os.path.join(success_path, todo_dir)):
                    os.makedirs(os.path.join(success_path, todo_dir))
        
        print 'finish merge_todo_videos this round...'
        time.sleep(sleep_time)

def get_output_path(filename):
    t1  = filename.split('.')[1][0:10]
    t1 = int(t1) + 8*3600
    t1 = str(t1)
    date_dir = str(time_change1(t1))
    out_filename = get_time_hour(t1) + get_time_minute(t1) + '.mp4'
    if not os.path.exists(os.path.join(save_path, date_dir)):
        os.makedirs(os.path.join(save_path, date_dir))
    return os.path.join(save_path, date_dir, out_filename)

def merge_video(to_merge_list):
    ret = False

    to_merge_list.sort(ctime_compare)
    print 'to merge video list: ', str(to_merge_list)
    merge_video_str = ''
    output_path = get_output_path(to_merge_list[0])
    print 'output_path: ', output_path
    if int(to_merge_list[0].split('.')[1][:10]) < time.time() - 86400:
        print 'video is out of date , dont merge'
        return True
    if os.path.exists(output_path) and os.path.exists(output_path+'.merged'):
        print 'merge file %s exists, do not merge it...' %(output_path)
        return True

    if os.path.exists(output_path):
        os.system('sudo rm -rf %s' %output_path)

    if os.path.exists(output_path + '.uploaded'):
        os.system('sudo rm -rf %s' % (output_path + '.uploaded'))
    
    #for video in to_merge_list:
    #    merge_video_str += os.path.join(source_path, video) + '|'
    #merge_video_str = merge_video_str[:-1]
    #cmdline = 'ffmpeg -i concat:"%s" -vcodec h264 %s' %(merge_video_str, output_path)
    f = open(channel + 'list.txt', 'w+')
    for video in to_merge_list:
        abs_video_path = os.path.join(source_path, video)
        if os.path.exists(abs_video_path):
            f.write('file ' + os.path.join(source_path, video) + '\n')
    f.close()
    cmdline = 'ffmpeg -y -f concat -safe 0 -i '+channel+'list.txt -vcodec h264  %s' %(output_path)
    if 'BBC' in channel:
        cmdline = 'ffmpeg -y -f concat -safe -0 -i '+channel+'list.txt -c copy  %s' %(output_path)
    ret = os.system(cmdline)
    if os.path.exists(output_path) and 'BBC' in channel:
        cmdline1 = 'ffmpeg -i %s -vcodec copy -map_channel 0.1.1 %s' %(output_path, output_path[:-4]+'_tmp.mp4')
        cmdline2 = 'mv -f %s %s'%(output_path[:-4]+'_tmp.mp4', output_path)
        res1 = os.system(cmdline1)
        res2 = os.system(cmdline2)
        ret += res1+res2
    print 'merge video cmdline: ', cmdline
    if ret != 0:
        print 'run cmdline error...'
    else:
        print 'merge %s success...' %output_path
        open(output_path+'.merged', 'w').write('')
        ret = True

    return ret

def merge_video_ftp_upload(save_path):
    while True:
        for to_upload_dir in os.listdir(save_path):
            print '=====DIR NAME IS====='+to_upload_dir
            #if int(to_upload_dir) < 20170301:
            #    continue
            to_upload_path = os.path.join(save_path, to_upload_dir)
            for to_upload_file in os.listdir(to_upload_path):
                if not to_upload_file.endswith('.mp4'):
                    continue

                if os.path.exists(os.path.join(to_upload_path, to_upload_file+'.uploaded')):
                    print '%s just uploaded...' %to_upload_file
                    continue

                if os.path.exists(os.path.join(to_upload_path, to_upload_file+'.merged')):
                    upload_file(os.path.join(to_upload_path, to_upload_file), to_upload_dir)

        time.sleep(sleep_time)

def upload_file(upfile, updir):
    print "start to upload %s, %s..." %(upfile, updir)
    try:
        channel1 = '%s1' %channel
        cmdline = './upload_singl_video_to_ftp.py /video/%s/%s %s' %(channel1, updir, upfile)
        os.system(cmdline)
        #ftp.cwd('/video/%s' %(channel1))
        #if updir not in ftp.nlst():
        #    ftp.mkd('/video/%s/%s' %(channel1, updir))

        #ftp.cwd('/video/%s/%s' %(channel1, updir))
        #bufsize = 1024
        #file_handler = open(upfile,'rb')
        #ftp.storbinary('STOR %s' % os.path.basename(upfile), file_handler, bufsize)
        #file_handler.close() 
        print "upload %s successfylly..." %(upfile)
        open(upfile+'.uploaded', 'w').write('')
    except:
        import traceback
        traceback.print_exc()
    print "upload %s finish..." %(upfile)

def main():
    t1 = threading.Thread(target=find_todo_videos,args=(source_path,))
    t2 = threading.Thread(target=merge_todo_videos,args=(source_path,))
    #t3 = threading.Thread(target=merge_video_ftp_upload,args=(save_path,))
    t1.start()
    t2.start()
    #t3.start()
    t1.join()
    t2.join()
    #t3.join()

def main1():
    upload_file('/tmp/0820.mp4', '20170221')

if __name__ == '__main__':
    try:
        main()
    except:
        import traceback
        traceback.print_exc()
