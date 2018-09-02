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
		# "Cookie":
		# '''
		# f=n; commontopbar_new_city_info=483%7C%E8%A5%BF%E5%AE%89%7Cxa; f=n; commontopbar_new_city_info=483%7C%E8%A5%BF%E5%AE%89%7Cxa; userid360_xml=D2BD0C8E95CC4793423E274585E38FAA; time_create=1536140973293; id58=c5/njVsObHnBixRaBAmlAg==; 58tj_uuid=8f9fd83f-d662-4228-b049-89df7fbfd7ea; als=0; xxzl_deviceid=tJUm3Rt4TPje5xgTc51gx404XGRpMJDw5%2Ffy77%2BxqcE%2FaEoR0FvCtjHG%2BYRsS5jZ; bj58_id58s="MjB3X0hhQ3lzaTZwOTQ4Mw=="; gr_user_id=9828040c-9db6-404f-b753-8e5f3ba7d006; wmda_uuid=099506fc0bbed8e4110dd6d0f351aa3a; wmda_new_uuid=1; Hm_lvt_e2d6b2d0ec536275bb1e37b421085803=1527672406; _ga=GA1.2.1959382043.1527672412; xxzl_smartid=a6581bac5246a3e110fb0a36a1ead9c6; wmda_visited_projects=%3B1731918550401%3B1731916484865%3B1409632296065%3B3381039819650; Hm_lvt_b4a22b2e0b326c2da73c447b956d6746=1527672447,1527677335; 58home=xa; city=xa; f=n; commontopbar_new_city_info=483%7C%E8%A5%BF%E5%AE%89%7Cxa; new_uv=15; commontopbar_ipcity=xa%7C%E8%A5%BF%E5%AE%89%7C0; 58cooper="userid=55865318876434&username=k4ge9y99u&cooperkey=4d0661eeb181fcf80038f94ea3b5f12e"; www58com="AutoLogin=true&UserID=55865318876434&UserName=k4ge9y99u&CityID=0&Email=&AllMsgTotal=0&CommentReadTotal=0&CommentUnReadTotal=0&MsgReadTotal=0&MsgUnReadTotal=0&RequireFriendReadTotal=0&RequireFriendUnReadTotal=0&SystemReadTotal=0&SystemUnReadTotal=0&UserCredit=0&UserScore=0&PurviewID=&IsAgency=false&Agencys=null&SiteKey=7A8AA9BF524FE054767118A61DE27F83E6B988D83DFA43321&Phone=&WltUrl=&UserLoginVer=7A8AA9BF524FE05476147814863FF6BA6&LT=1533547565189"; commontopbar_myfeet_tooltip=end; show_zcm_banner=true; sessionid=c026286e-708f-4fc0-a246-96d195f7ada7; param8616=0; param8716kop=1; zcmshow=1; Hm_lvt_a3013634de7e7a5d307653e15a0584cf=1533547984; Hm_lpvt_a3013634de7e7a5d307653e15a0584cf=1533547984; bj58_new_uv=3; __utma=253535702.1959382043.1527672412.1533548302.1533548302.1; __utmc=253535702; __utmz=253535702.1533548302.1.1.utmcsr=xa.58.com|utmccn=(referral)|utmcmd=referral|utmcct=/; hots=%5B%7B%22d%22%3A0%2C%22s1%22%3A%22a%22%2C%22s2%22%3A%22%22%2C%22n%22%3A%22sou%22%7D%5D; xzfzqtoken=nufUKbl7CJefvpOm9eqk8a%2BExBW0Gka3vRQHB%2FQq65Dqk%2BYKO3JApN1DIYRvy6Vdin35brBb%2F%2FeSODvMgkQULA%3D%3D; isShowProtectTel=true; Hm_lvt_5bcc464efd3454091cf2095d3515ea05=1533548338; myfeet_tooltip=end; bangtoptipclose=1; Hm_lvt_b2c7b5733f1b8ddcfc238f97b417f4dd=1533551835; JSESSIONID=76D4B7E392CFB04AECF34D5FC8034D02; Hm_lpvt_5bcc464efd3454091cf2095d3515ea05=1533553137; ppStore_fingerprint=6CCAAEAC5B49516318C22F8B5AE1D916194E94DE02608891%EF%BC%BF1533553158073; Hm_lpvt_b2c7b5733f1b8ddcfc238f97b417f4dd=1533553158; PPU="UID=55865318876434&UN=k4ge9y99u&TT=ace57d01e54bea10a583f6e6b0d71e7c&PBODY=cfyI3JwpkoNwTvXXsYoBn8dbpc2-Jf1hxARTbRSWV8SbCFVLNH-oHVsNNH_moYxozye-3xYaa4yTrtGS3Lc8izQpZ805v1esrSCq3sS8NvyI4_j6n6m3XbkFCo8bSq-kuTYLrKIuBg4SqEXn8dL7ap_Hp8YVOGzy37oxefgmwEU&VER=1"
		# '''
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