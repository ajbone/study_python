#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import traceback
import os
import re


def main():
    src_url = ''
    head_url = 'https://seals.vobile.cn/svn/ProjectManagement/demo/aqbk'
    user_name = 'lv_da'
    pass_word = ''
    st_v = 0
    ed_v = 11344


    cmd = 'svn diff -r{}:{} {} --username {} --password {}'
    run_cmd = cmd.format(st_v, ed_v, ''.join([head_url, src_url]),
                             user_name, pass_word)
    print run_cmd
    pipe = os.popen(run_cmd, 'r')
    output = pipe.read()
    status = pipe.close()
    if status is None:
        m_del = re.compile('\n(\-{1}[^\-\n]+)').findall(output)
        if m_del:
            print 'total delete {}'.format(len(m_del))
        m_add = re.compile('\n(\+{1}[^\+\n]+)').findall(output)
        if m_add:
            print 'total add {}\n\n\n'.format(len(m_add))
    else:
        print 'run error: {}'.format(output)



if __name__ == '__main__':
    try:
        main()
    except:
        print traceback.format_exc()
