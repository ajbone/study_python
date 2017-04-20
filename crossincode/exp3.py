#!/usr/bin/env python
#coding: utf-8  
#【每日一坑 4】 查找文件

import os

for root, dirs, files in os.walk('/Users/lazybone/workspaces/study_python/'):
    #if os.path.splitext(files)[1] == ".py":
    #	print files
    for i in files:
        if os.path.splitext(i)[1] == '.py':
        	print i



