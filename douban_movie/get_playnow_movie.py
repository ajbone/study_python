#!/usr/bin/env python  
#coding: utf-8  

import time
import requests
from bs4 import BeautifulSoup
import re

url = "https://movie.douban.com/nowplaying/hangzhou/"

try:
	response = requests.request("GET", url)
except Exception as e:
    print('请求出现错误，错误信息：%s' %e)
else:
	soup = BeautifulSoup(response.text,"lxml")
	#print soup.prettify()

	movie_all = soup.find_all('div',{"id":"nowplaying"})
	#print movie_all
	print "杭州正在上映的电影："
	for i in movie_all:
		for j in i.find_all('li',{"class":"list-item"}):
			print "电影名称:",j["data-title"]
			print "豆瓣评分：",j["data-score"]
			print "-----------------------------"


'''
soup = BeautifulSoup(response.text,"lxml")
#print soup.prettify()

#print soup.find_all('li',{"class":"list-item"})[0]['data-title']
movie_all = soup.find_all('div',{"id":"nowplaying"})
#print movie_all


for i in movie_all:
	for j in i.find_all('li',{"class":"list-item"}):
		print "电影名称:",j["data-title"]
		print "豆瓣评分：",j["data-score"]
'''

