#!/usr/bin/python
# -*- coding: utf-8 -*-
import traceback
import paramiko


def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='203.192.16.16',
                port=22,
                username='root',
                password='xinhua')
    mysql_cmd = "mysql -hfiledb.bqa.sers -uqqw -p'QQw0909&' xhs_web -e '{}'"
    sql_cmd = 'set names utf8;select * from tracking_source where sign="{}" '\
        'and category="website"\G;'
    _, stdout, stderr = ssh.exec_command(
        mysql_cmd.format(sql_cmd.format('qq')))
    if stderr.readlines():
        print ''.join(stderr.readlines())
    else:
        print ''.join(stdout.readlines())
    ssh.close()


if __name__ == '__main__':
    try:
        main()
    except:
        print traceback.format_exc()
