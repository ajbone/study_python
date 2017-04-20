#!/usr/bin/env python
#coding: utf-8  
#【每日一坑 3】 找数字

import re
a = ''

text = "aAsmr3idd4bgs7Dlsf9eAF"
arr = []

for i in text:
	if re.match('^[0-9]',i):
		a = a + str(i)

print a


str = ''
print str.join(re.findall(r'[\d|.]+',text))

'''
for i in text:
	if re.match('^[0-9]',i):
		arr.append(i)

s = str.join(map(str,arr))
print s

'''
