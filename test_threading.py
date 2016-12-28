#!/bin/python
#coding=utf-8

import threading
from time import ctime,sleep


def music(func):
    for i in range(3):
        print "I was listening to %s. %s" %(func,ctime())
        sleep(4)


def move(func):
    for i in range(3):
        print "I was at the %s! %s" %(func,ctime())
        sleep(4)


threads = []

t1 = threading.Thread(target=music,args=(u'爱情买卖',))
threads.append(t1)

t2 = threading.Thread(target=move,args=(u'变形金刚',))
threads.append(t2)

if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()

    t.join()
    print "all over %s" %ctime()
