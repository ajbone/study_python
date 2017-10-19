# -*- coding: utf-8 -*-



import os
import sys
import platform
import time
from datetime import datetime

user_module_path = os.path.dirname(os.path.realpath(__file__))
from run_cmd import RunCmd

SCRIPT = """ text-report layout:side-by-side &
 options:ignore-unimportant,display-mismatches &
 output-to:%3 output-options:html-color %1 %2"""

if "Windows" == platform.system():
    #STD_TMP_PATH = os.environ.get("TEMP")
    STD_TMP_PATH = user_module_path
elif "Linux" == platform.system():
    #STD_TMP_PATH = "/tmp"
    STD_TMP_PATH = user_module_path
    
LOG_FILE = user_module_path + "/compare_log.txt"

class CodeCompare(object):
    def __init__(self, compare_tool, left, right, extra, thread_number, fp_log):
        self.left = left
        self.right = right
        self.tool = compare_tool
        self.extra_fiter = extra.lower().split(",")
        self.change_lines = 0
        self.diff_file_number = 0
        self.total_file_number = 0
        self.leftonly_number = 0
        self.rightonly_number = 0
        self.thread_number = thread_number
        self.fp_log = fp_log
            
        self.tmp_script_file = STD_TMP_PATH + "/tmp_script_file.txt"
        fp = open(self.tmp_script_file, "w")
        fp.write(SCRIPT)
        fp.close()
        
        self.tmp_result_file = STD_TMP_PATH + "/tmp_compare_result.html"
        self.left_tmp = STD_TMP_PATH + "/tmp_left.txt"
        self.right_tmp = STD_TMP_PATH + "/tmp_right.txt"
        
        
    def __del__(self):
        if os.path.exists(self.tmp_script_file):
            os.remove(self.tmp_script_file)
            
    def file_compare(self, left, right):
        #self.make_nospace_file(left, self.left_tmp)
        #self.make_nospace_file(right, self.right_tmp)
        
        cmd = "%s @%s %s %s %s -silent" % (self.tool, self.tmp_script_file, self.left_tmp, self.right_tmp, self.tmp_result_file)
        process = RunCmd(cmd)
        ret = process.run()
        #print 'ret = %s' % ret
        if 0 == ret:
            self.change_lines += self.check_diff(self.tmp_result_file)
        else:
            self.make_nospace_file_err(left, self.left_tmp)
            self.make_nospace_file_err(right, self.right_tmp)
                    
            cmd = "%s @%s %s %s %s -silent" % (self.tool, self.tmp_script_file, self.left_tmp, self.right_tmp, self.tmp_result_file)
            process = RunCmd(cmd)
            ret = process.run()
            self.change_lines += self.check_diff(self.tmp_result_file)
        
        if os.path.exists(self.tmp_result_file):
            os.remove(self.tmp_result_file)
            
        if os.path.exists(self.left_tmp):
            os.remove(self.left_tmp)
            
        if os.path.exists(self.right_tmp):
            os.remove(self.right_tmp)
            
    def single_file_count(self, filename, side):
        self.file_single_tmp = STD_TMP_PATH + "/tmp_file_single.txt"
        self.make_nospace_file(filename, self.file_single_tmp)
        fp = open(self.file_single_tmp, "r")
        lines = fp.readlines()
        self.change_lines += len(lines)
        fp.close()
        
        if side == "left":
            self.leftonly_number += 1
        elif side == "right":
            self.rightonly_number += 1
            
        
        if os.path.exists(self.file_single_tmp):
            os.remove(self.file_single_tmp)        
        
        
        
        
    def make_nospace_file(self, filename, tmp_filename):
        fp_src = open(filename, "rU")
        fp_dst = open(tmp_filename, "w")
        
        readlines = fp_src.readlines()
        writelines = []
                
        for index in range(len(readlines)):
            space_line = readlines[index].replace(" ", "")
            if space_line != "\n" and space_line != "\r\n":
                try:
                    readlines[index].decode("gbk")
                    writelines.append(readlines[index])
                except Exception, ex:
                    print "filename: %s" % filename
                    print "line: %s" % (index + 1)
                    print ex
                    self.fp_log.write("filename: %s\r\n" % filename)
                    self.fp_log.write("line: %s\r\n" % (index + 1))
                    self.fp_log.write("%s\r\n" % str(ex))
                
                
        fp_dst.writelines(writelines)
        fp_src.close()
        fp_dst.close()
        
    def make_nospace_file_err(self, filename, tmp_filename):
        fp_src = open(filename, "rU")
        fp_dst = open(tmp_filename, "w")
                
        readlines = fp_src.readlines()
        writelines = []
        #print readlines
        for line in readlines:
            space_line = line.replace(" ", "")
            if space_line != "\n" and space_line != "\r\n":
                try:
                    line = line.decode('utf8').encode('ascii')
                    writelines.append(line)
                except UnicodeEncodeError, ex:
                    print "filename : %s" % filename
                    self.fp_log.write("filename: %s\r\n" % filename)
                    print "line : %s" % line
                    self.fp_log.write("line : %s\r\n" % line)
                    pass
                except UnicodeDecodeError, ex:
                    print "filename : %s" % filename
                    self.fp_log.write("filename: %s\r\n" % filename)
                    print "line : %s" % line
                    self.fp_log.write("line : %s\r\n" % line)
                    pass
                        
        fp_dst.writelines(writelines)
        fp_src.close()
        fp_dst.close()    
        
        
    def check_diff(self, result_file):
        fp = open(result_file, "r")
        content = fp.read().replace('''<tr class="SectionGap"><td colspan="3">&nbsp;</td></tr>''', "")
        diff_lines = content.count("</tr>")
        if diff_lines != 0:
            self.diff_file_number += 1
        self.total_file_number += 1
        return diff_lines
    
    def list_path(self, left_path, right_path):
        self.left_file_list = []
        for parent, dirnames, filenames in os.walk(left_path):
            for filename in filenames:
                if filename.split(".")[-1] in self.extra_fiter:
                    self.left_file_list.append(parent[len(left_path) + 1:] + "/" + filename)

        self.rightonly_file_list = []
        for parent, dirnames, filenames in os.walk(right_path):
            for filename in filenames:
                if filename.split(".")[-1] in self.extra_fiter:
                    self.rightonly_file_list.append(parent[len(right_path) + 1:] + "/" + filename)
                    
        self.both_file_list = []
        self.leftonly_file_list = []
        for filename in self.left_file_list:
            if filename in self.rightonly_file_list:
                self.both_file_list.append(filename)
                self.rightonly_file_list.remove(filename)
            else:
                self.leftonly_file_list.append(filename)
                
    def file_merge_compare(self, left_path, right_path):
        left_writelines = []
        right_writelines = []
        for filename in self.both_file_list:
            left_file = left_path + "/" + filename
            right_file = right_path + "/" + filename
            
            fp_left = open(left_file, 'rU')
            left_readlines = fp_left.readlines()
            for index in range(len(left_readlines)):
                space_line = left_readlines[index].replace(" ", "")
                if space_line != "\n" and space_line != "\r\n":
                    try:
                        left_readlines[index].decode("gbk")
                        left_writelines.append(left_readlines[index])
                    except Exception, ex:
                        print "filename: %s" % filename
                        print "line: %s" % (index + 1)
                        print ex
                        self.fp_log.write("filename: %s\r\n" % left_file)
                        self.fp_log.write("line: %s\r\n" % (index + 1))
                        self.fp_log.write("%s\r\n" % str(ex))
            fp_left.close()
            
            fp_right = open(right_file, 'rU')
            right_readlines = fp_right.readlines()
            for index in range(len(right_readlines)):
                space_line = right_readlines[index].replace(" ", "")
                if space_line != "\n" and space_line != "\r\n":
                    try:
                        right_readlines[index].decode("gbk")
                        right_writelines.append(right_readlines[index])
                    except Exception, ex:
                        print "filename: %s" % filename
                        print "line: %s" % (index + 1)
                        print ex
                        self.fp_log.write("filename: %s\r\n" % right_file)
                        self.fp_log.write("line: %s\r\n" % (index + 1))
                        self.fp_log.write("%s\r\n" % str(ex))
            fp_right.close()
            
        fp_tmp = open(self.left_tmp, 'w')
        fp_tmp.writelines(left_writelines)
        fp_tmp.close()
        
        fp_tmp = open(self.right_tmp, 'w')
        fp_tmp.writelines(right_writelines)
        fp_tmp.close()
        
        self.file_compare(self.left_tmp, self.right_tmp)
if __name__ == "__main__":
    if len(sys.argv) < 6:
        print 'Usage: python %s "beyond compare tool" left_folder right_folder mode extra_filter' % os.path.basename(__file__)
        sys.exit(-1)
    elif len(sys.argv) == 6:
        thread_number = 1
    else:
        try:
            thread_number = int(sys.argv[6])
        except ValueError, ex:
            print "param 'thread' is not int"
            sys.exit(-1)
            
    fp_log = open(LOG_FILE, "a")
    fp_log.write("%s\r\n" % ("*" * 100))
    print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    fp_log.write("now is %s\r\n" % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    fp_log.write("left %s %s\r\n" % (sys.argv[4], sys.argv[2]))
    fp_log.write("right %s %s\r\n" % (sys.argv[4], sys.argv[3]))
    fp_log.write("\r\n")
    
    start = time.time()
    
    try:
        code_comp = CodeCompare(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[5], thread_number, fp_log)
    
        if sys.argv[4] == "folder":
            code_comp.list_path(sys.argv[2], sys.argv[3])
            code_comp.file_merge_compare(sys.argv[2], sys.argv[3])
            #for filename in code_comp.both_file_list:
                #left = sys.argv[2] + "/" + filename
                #right = sys.argv[3] + "/" + filename
                #code_comp.file_compare(left, right)
        
            for filename in code_comp.leftonly_file_list:
                code_comp.single_file_count(sys.argv[2] + "/" + filename, "left")
        
            for filename in code_comp.rightonly_file_list:
                code_comp.single_file_count(sys.argv[3] + "/" + filename, "right")
    
            print "left total files: %s" % (len(code_comp.both_file_list) + len(code_comp.leftonly_file_list))
            fp_log.write("left total files: %s\r\n" % (len(code_comp.both_file_list) + len(code_comp.leftonly_file_list)))
            print "right total files: %s" % (len(code_comp.both_file_list) + len(code_comp.rightonly_file_list))
            fp_log.write("right total files: %s\r\n" % (len(code_comp.both_file_list) + len(code_comp.rightonly_file_list)))
            print "total check diff files: %s" % code_comp.total_file_number
            fp_log.write("total check diff files: %s\r\n" % code_comp.total_file_number)
            print "diffrent files: %s" % code_comp.diff_file_number
            fp_log.write("diffrent files: %s\r\n" % code_comp.diff_file_number)
            print "left only files: %s" % code_comp.leftonly_number
            fp_log.write("left only files: %s\r\n" % code_comp.leftonly_number)
            print "right only files: %s" % code_comp.rightonly_number
            fp_log.write("right only files: %s\r\n" % code_comp.rightonly_number)
        elif sys.argv[4] == "file":
            code_comp.file_compare(sys.argv[2], sys.argv[3])
        else:
            print "[error] mode error!"
            sys.exit(-1)
        print "total diffrent lines: %s" % code_comp.change_lines
        fp_log.write("total diffrent lines: %s\r\n" % code_comp.change_lines)
    except Exception, ex:
        print str(ex)
    finally:
        print "cost %s second" % (time.time() - start)
        fp_log.write("cost %s second\r\n" % (time.time() - start))
        fp_log.close()
        
