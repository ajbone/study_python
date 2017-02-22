#!/usr/bin/env python  
#coding: utf-8  

import requests
import json

url = "http://cn163.net/archives/24016/"
data=requests.get(url,timeout=3)
content=data.text()
link_pat='"(ed2k://\|file\|[^"]+?\.(S\d+)(E\d+)[^"]+?1024X\d{3}[^"]+?)"'
name_pat=re.compile(r'<h2 class="entry_title">(.*?)</h2>',re.S)
print name_pat



print content*()





