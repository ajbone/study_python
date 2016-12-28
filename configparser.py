#!/usr/bin/env python
#coding=utf8

import ConfigParser

conf = ConfigParser.ConfigParser()
conf.read("/home/zhang_jin/vobile/study_python/config")

name = conf.get("section1","name")
print(name)

age = conf.get("section1","age")
print age