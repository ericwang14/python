#! /usr/bin/python

from lxml import etree
import requests

html = requests.get('https://monterey.craigslist.org/search/jjj')
selector = etree.HTML(html.text)

content = selector.xpath('//span[@class="pl"]/a/text()')

for each in content:
    print each
