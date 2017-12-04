#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
def emails(mail):
    if len(mail)>=5:
        if re.match("[a-zA-Z0-9]+\@+[a-zA-Z0-9]+\.+[a-zA-Z]",mail) !=None:
            return "mail 格式正确"

    return "mail 格式错误"

mail = raw_input("请输入mail：")
print mail
a = emails(mail)
print a
