

import os
import sys
import platform


user_module_path = os.path.dirname(os.path.realpath(__file__))
from run_cmd import RunCmd

SCRIPT = """ text-report layout:side-by-side &
 options:ignore-unimportant,display-mismatches &
 output-to:%3 output-options:html-color %1 %2"""


class CodeCompare(object):
    def __init__(self, compare_tool, left, right, extra):
        self.left = left
        self.right = right
        self.tool = compare_tool
        self.extra_fiter = extra.lower().split(",")
        self.change_lines = 0
        self.diff_file_number = 0
        self.total_file_number = 0
        self.leftonly_number = 0
        self.rightonly_number = 0
        
        if "Windows" == platform.system():
            self.std_tmp_path = os.environ.get("TEMP")
        elif "Linux" == platform.system():
            self.std_tmp_path = "/tmp"        
    
    def file_compare(self, left, right):
        
            
        tmp_script_file = self.std_tmp_path + "/tmp_script_file.txt"
        tmp_result_file = self.std_tmp_path + "/compare_result.html"
        #tmp_result_file = "F:\\cc.html"
        fp = open(tmp_script_file, "w")
        fp.write(SCRIPT)
        fp.close()
        
        self.left_tmp = self.std_tmp_path + "/tmp_left.txt"
        self.right_tmp = self.std_tmp_path + "/tmp_right.txt"
        self.make_nospace_file(left, self.left_tmp)
        self.make_nospace_file(right, self.right_tmp)
        
        cmd = "%s @%s %s %s %s -silent" % (self.tool, tmp_script_file, self.left_tmp, self.right_tmp, tmp_result_file)
        process = RunCmd(cmd)
        process.run()
        
        self.change_lines += self.check_diff(tmp_result_file)
        
        if os.path.exists(tmp_script_file):
            os.remove(tmp_script_file)
            
        if os.path.exists(tmp_result_file):
            os.remove(tmp_result_file)
            
        if os.path.exists(self.left_tmp):
            os.remove(self.left_tmp)
            
        if os.path.exists(self.right_tmp):
            os.remove(self.right_tmp)
            
    def single_file_count(self, filename, side):
        self.file_single_tmp = self.std_tmp_path + "/tmp_file_single.txt"
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
        fp_src = open(filename, "r")
        fp_dst = open(tmp_filename, "w")
        
        readlines = fp_src.readlines()
        writelines = []
        
        for line in readlines:
            space_line = line.replace(" ", "")
            if space_line != "\n" and space_line != "\r\n":
                writelines.append(line)
                    
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
                
if __name__ == "__main__":
    if len(sys.argv) < 6:
        print 'Usage: python %s "beyond compare tool" left_folder right_folder mode extra_filter' % os.path.basename(__file__)
        sys.exit(-1)
    code_comp = CodeCompare(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[5])
    
    if sys.argv[4] == "folder":
        code_comp.list_path(sys.argv[2], sys.argv[3])
        for filename in code_comp.both_file_list:
            left = sys.argv[2] + "/" + filename
            right = sys.argv[3] + "/" + filename
            code_comp.file_compare(left, right)

        
        for filename in code_comp.leftonly_file_list:
            code_comp.single_file_count(sys.argv[2] + "/" + filename, "left")
        
        for filename in code_comp.rightonly_file_list:
            code_comp.single_file_count(sys.argv[3] + "/" + filename, "right")
    
        print "left total files: %s" % (len(code_comp.both_file_list) + len(code_comp.leftonly_file_list))
        print "right total files: %s" % (len(code_comp.both_file_list) + len(code_comp.rightonly_file_list))
        print "total check diff files: %s" % code_comp.total_file_number
        print "diffrent files: %s" % code_comp.diff_file_number
        print "left only files: %s" % code_comp.leftonly_number
        print "right only files: %s" % code_comp.rightonly_number
    elif sys.argv[4] == "file":
        code_comp.file_compare(sys.argv[2], sys.argv[3])
    else:
        print "[error] mode error!"
        sys.exit(-1)
    print "total diffrent lines: %s" % code_comp.change_lines
