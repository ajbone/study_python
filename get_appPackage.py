#!/usr/bin/env python
#coding: utf-8
import MySQLdb


conn = MySQLdb.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='',
    db='appPackage'
)

# 数据库中取渠道信息
cur = conn.cursor()
cur.execute("select content from channelList where id =1")
rows = cur.fetchmany()
rows = np.array(rows)
for row in rows:
    lines = json.loads(row["content"])