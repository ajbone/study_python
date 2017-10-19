#!/usr/bin/python
import sys
import os
import httplib
import time
import struct
from datetime import datetime
import subprocess
import shlex
import platform

class RunCmd():
    def __init__(self, cmd, std_tmp_path = None, timeout = None):
        if timeout is None:
            self.timeout = 99999999999
        else:
            self.timeout = timeout
        self.cmd =cmd
        
        if std_tmp_path is None or not os.path.exists(std_tmp_path):
            if "Windows" == platform.system():
                std_tmp_path = os.environ.get("TEMP")
            elif "Linux" == platform.system():
                std_tmp_path = "/tmp"
        
        self.pid = os.getpid()
        self.stdout_file = std_tmp_path + "/stdout_tmp_%s.txt" % self.pid
        self.stderr_file = std_tmp_path + "/stderr_tmp_%s.txt" % self.pid
            
        self.fp_stdout = open(self.stdout_file, "w")
        self.fp_stderr = open(self.stderr_file, "w")

    def run(self):
        #cmd = shlex.split(self.cmd)
        cmd = self.cmd.split(" ")
        self.start = time.time()
        self.process = subprocess.Popen(cmd, stderr = self.fp_stderr, stdout = self.fp_stdout)
        while True:
            return_code = self.process.poll()
            if return_code is None:
                if time.time() - self.start > self.timeout:
                    self.process.kill()
                    self.process.wait()
            else:
                if return_code != -9:
                    #self.stdout = self.process.stdout.read()
                    #self.stderr = self.process.stderr.read()
                    self.stdout = open(self.stdout_file, "r").read()
                    self.stderr = open(self.stderr_file, "r").read()
                break
            
        self.fp_stdout.close()
        self.fp_stderr.close()
        os.remove(self.stdout_file)
        os.remove(self.stderr_file)        

        return return_code

    def __del__(self):
        #self.fp_stdout.close()
        #self.fp_stderr.close()
        #os.remove(self.stdout_file)
        #os.remove(self.stderr_file)
        pass

def main():
    pass

if __name__ == '__main__':
    main()
