#!/usr/bin/python
import subprocess
import commands

#ommands.getstatusoutput('ls /home/zhang_jin/')
command="ls /home/zhang_jin/ > /tmp/a.log"
subprocess.Popen(command, shell=True)
