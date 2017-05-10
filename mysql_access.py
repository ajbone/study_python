#!/usr/bin/env python
# encoding: utf-8
import MySQLdb


if __name__ == '__main__':
    db_name = 'xhs_web'
    db_host = 'filedb.bqa.sers'
    db_user = 'qqw'
    db_pswd = '123'

    conn = MySQLdb.connect(host=db_host, user=db_user,
                           passwd=db_pswd, db=db_name)
    cursor = conn.cursor()
    sql = '''SELECT create_time,ifnull(imagematch, 0)
      FROM text_match
      GROUP BY
      create_time
      ORDER BY
      create_time '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
