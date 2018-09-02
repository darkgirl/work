#!/usr/bin/env python
#coding:utf-8
#

import time
import urllib
import urllib2
from bs4 import BeautifulSoup

url = "http://xa.58.com/job/pn%(page_index)d/?key=java&final=1&jump=1&bd=1&PGTID=0d302408-001e-3160-53d1-4ecca22a979b&ClickID=3"
black_comp_file = "./black_list.txt"
black_comp_set = set()
white_comp_file = "./white_list.txt"
white_comp_set = set()
black_key_words = [
	"转",
	"培训",
	"讲师",
	"助教",
	"实习生",
]

visit_comp_file = "./visit_list.txt"
visit_comp_set = set()

# def init_black_comp():
# 	fhandle = open(black_comp_file, "r")
# 	data = fhandle.read()
# 	for line in data.split('\n'):
# 		if ("" != line):
# 			print line.decode('utf-8')
# 			black_comp_set.add(line.decode('utf-8'))

# 	fhandle.close()

def init_set(filename, setname):
	fhandle = open(filename, "r")
	data = fhandle.read()
	for line in data.split('\n'):
		if ("" != line):
			print line.decode('utf-8')
			setname.add(line.decode('utf-8'))

	fhandle.close()

# def update_black_comp():
# 	fhandle = open(black_comp_file, "w")

# 	data = '\n'.join(black_comp_set)
# 	fhandle.write(data.encode('utf-8'))
# 	fhandle.close()

def update_set(filename, setname):
	fhandle = open(filename, "w")

	data = '\n'.join(setname)
	fhandle.write(data.encode('utf-8'))
	fhandle.close()

def get_page_html(url):
	headers = {
	}
	req = urllib2.Request(url, headers=headers)
	res = urllib2.urlopen(req)
	return res.read()

if __name__ == '__main__':
	# main()
	# init_black_comp()
	init_set(black_comp_file, black_comp_set)
	init_set(white_comp_file, white_comp_set)
	# exit(0)
	page_index = 1
	page_total = 1
	job_item_total = 0
	while page_index <= page_total:
		if (page_index < page_total):
			break
		print page_total
		print url % ({"page_index": page_index})

		html = get_page_html(url % ({"page_index": page_index}))
		bs = BeautifulSoup(html, "lxml")
		page_total = bs.select("i.total_page")[0].contents[0]
		job_items = bs.select(".job_item")

		for job_item in job_items:
			# print job_item

			job_name = job_item.select(".job_name > a > span.name")[0].contents[0]
			comp_name = job_item.select(".comp_name > a")[0]['title']
			if (comp_name in black_comp_set):
				continue
			is_contains = False
			for key_word in black_key_words:
				if job_name.find(key_word.decode('utf-8')) >= 0:
					black_comp_set.add(comp_name)
					is_contains = True
			if (is_contains):
				continue

			print job_item.select(".job_name > a")[0]['href']
			print job_item.select(".job_name > a > span.address")[0].contents[0]
			print job_name
			print job_item.select(".job_salary")[0].contents[0]
			print comp_name

			white_comp_set.add(comp_name)

			job_item_total += 1
			print '\n'
		page_index += 1
		time.sleep(1)
	print job_item_total
	# update_black_comp()
	update_set(black_comp_file, black_comp_set)
	update_set(white_comp_file, white_comp_set)
	pass