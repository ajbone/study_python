#!/usr/bin/env python
#coding=utf8

import MySQLdb

db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123",db="wasu_g20",port=3306)
cursor = db.cursor()

#sql = "delete from query_result_info where id = 28"
sql = "select createdna_costtime from query_result_info limit 10"

cursor.execute(sql)
results = cursor.fetchall()


print results


for row in results:
    
db.close()