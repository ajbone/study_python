#!/usr/bin/env python
#coding: utf-8
'''
unittest xhs image_query interface
@author: zhang_jin@vobile.cn
@version: 1.0
@see:
'''
import redis
import sys

if len(sys.argv) < 2:
    print sys.argv[0]+":" +"list_name"
    #print sys.argv[0] + ' ftp_dir  local_dir'
    sys.exit(0)
else:
	list_name = sys.argv[1]

client =redis.Redis(host='116.62.120.213',port=6379,db=0)

arrayList = client.lrange(list_name,0,-1)
print arrayList

'''
with open('/tmp/redis_result.txt', 'w') as f:
    f.write(arrayList)
'''
