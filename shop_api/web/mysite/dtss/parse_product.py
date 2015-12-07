#! /usr/bin/python
# --*-- encoding=utf-8 --*--

from lxml import etree

import product_search


"""
parse product benifit string and build new benifit array
"""


def parse(categories):
    products = product_search.get_products(categories)
    for product in products:
        try:
            if "benifits" in product:
                selector = etree.HTML(product['benifits'])
                product['benifits'] = selector.xpath('//ul/li/text()')
        except KeyError as e:
            print e
    return products



if __name__ == '__main__':
    print parse()
