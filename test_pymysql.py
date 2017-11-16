# -*- coding: utf-8 -*-
#from flask import jsonify, Flask,make_response,request
import pymysql,sys

reload(sys)
sys.setdefaultencoding('utf-8')

domain = "/server/login"
method = "post"

# config ={
#         'host':_host,
#         'port':int(_port),
#         'user':_dbuser,
#         'passwd':_dbpassword,
#         'db':_dbname,
#         'charset':'utf8',
#         }

# conn = pymysql.connect(**config)
conn = pymysql.connect(host='192.168.5.104',port= 3307,user = 'root',passwd='123456',db='mock_config',charset='utf8')

cur = conn.cursor() 
cur.execute('select reqparams, resparams from mock_config where status=0 and domain=%s and methods=%s', (domain, method))

ret = cur.fetchone()

print ret
