#!/usr/bin/env python  
#coding: utf-8  

import json
import sys

def write_crypt_data(bankID,nameOnCard):
	#print username,identityNumber
	with open('/tmp/1.txt','aw') as fh:
		fh.write(str(bankID) + ","+ str(nameOnCard)+"\n")


if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding("utf-8")
	with open ("/Users/lazybone/Downloads/data.json","r") as f:
		bills =  json.loads(f.read())["data"]["bills"]
		for bill in bills:
			bankID = bill["bankId"]
			nameOnCard = bill["nameOnCard"]
			write_crypt_data(bankID,nameOnCard)




