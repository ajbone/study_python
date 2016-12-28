#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import time
import multiprocessing
from websocket import create_connection
def ws_xx():
	random_num=random.randint(0, 10000)
	ws = create_connection("ws://114.215.248.78:8080/command/scmd?deviceId=qa_test_201509009_%s" %(random_num))
	ws.send("QA Test Hello World")
	time.sleep(10000)

if __name__ == "__main__":
	pool = multiprocessing.Pool(processes=100)
 	for i in xrange(1000):
 		pool.apply_async(ws_xx, ())
 	pool.close()
	pool.join()
	print "Sub-process(es) done."

#print "Sent"
#print "Receiving..."
#result =  ws.recv()

#print "Received '%s'" % result
#ws.close()