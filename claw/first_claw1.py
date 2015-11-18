#! /usr/bin/python
# -*-coding=utf-8 -*-
import requests
import sys
import re

html = requests.get('https://monterey.craigslist.org/search/jjj')
job_summary = re.findall('<p class="row".*>.*<\/p>', html.text)
for each in job_summary:
    date_list  = re.findall('\w*\s*\w*(?=<\/time>)', each, re.S)
    name = re.findall('class="hdrlnk">(.*?)</a>', each, re.S)
    print len(name)
    i = 0
    for date_each in date_list:
        print date_each,
        i = i + 1
        if i < len(name):
            print name[i]
        else:
            break

