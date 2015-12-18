#! /usr/bin/python
# --*-- encoding=UTF-8 --*--

from lxml import etree
from HTMLParser import HTMLParser
import requests

h = HTMLParser()
html = requests.get('http://www.shop.com/Snap+trade+Pak-681238216-p+.xhtml')
selector = etree.HTML(html.text)

content = selector.xpath('//div[@id="benefits"]/*/li/text()')

for each in content:
	if each:
		texts = [h.unescape(text.encode('utf-8')) for text in each.itertext()]
		print ' '.join(texts)