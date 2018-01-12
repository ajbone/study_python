#!/usr/bin/env python
#coding: utf-8


def bubble_sort(lists):
	count = len(lists)
	for i in range(0,count):
		for j in range(i+1,count):
			if lists[i] > lists[j]:
				lists[i],lists[j] = lists[j],lists[i]
	return lists


def select_sort(lists):
    # 选择排序
    count = len(lists)
    for i in range(0, count):
        min = i
        for j in range(i + 1, count):
            if lists[min] > lists[j]:
                min = j
        lists[min], lists[i] = lists[i], lists[min]
    return lists


if __name__ == '__main__':
	lists = [3,5,1,11,6,12,10,22,11,4]
	print bubble_sort(lists)
	print select_sort(lists)