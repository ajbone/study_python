#!/usr/bin/env python
#coding: utf-8  
#【每日一坑 2】 去除重复加排序

import random 
a = [4, 7, 3, 14,17,19,5,6,4, 1, 9, 8, 3, 7]
b = []


print a[2]

for i in range(0,len(a)):
	if a[i] in b:
		pass
	else:
		b.append(a[i])
    
for j in range(0,len(b)):
	for k in range(j+1,len(b)):
		if b[j] > b[k]:
			b[j],b[k] = b[k],b[j]
print b

print sorted(set((4, 7, 3, 4, 1, 9, 8, 3, 7)))


