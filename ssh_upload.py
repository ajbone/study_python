#!/usr/bin/python
# -*- coding: utf-8 -*-
import traceback
import paramiko
from scp import SCPClient


def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    key = paramiko.RSAKey.from_private_key_file('F:\pub.key')
    ssh.connect(hostname='121.41.96.26',
                port=20140,
                username='root',
                pkey=key)
    scp = SCPClient(ssh.get_transport())
    scp.put('./ssh_upload.py', '/root/ssh_upload.py')
    scp.get('/root/ssh_upload.py', './ssh_upload.py.2')
    scp.close()
    ssh.close()


if __name__ == '__main__':
    try:
        main()
    except:
        print traceback.format_exc()
