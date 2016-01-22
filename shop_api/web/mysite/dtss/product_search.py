#! /usr/bin/python
# --*-- encoding=utf-8 --*--

from lxml import etree

import requests
import random

"""
get products information
"""

api_key = 'l7xx175ed35d49844df29b26917291a11038'
api_domain = 'https://api.shop.com'
search_key = 'isotonix'
search_url = 'https://api.shop.com/sites/v1/search/Term/{0}'


def get_response(url, repeat_time=3):
    """
    get response for given url
    :param url   - request url
    :param repeat_time  - recursion repeat time default is 3
    """
    if repeat_time <= 0:
        return

    try:
        r = requests.request(method='GET', url=url, headers={'apikey': api_key})
        if r.status_code != 200:
            repeat_time -= 1
            print url + ' ' + str(r.status_code) + ' ' + r.reason
            print 'try ' + str(repeat_time) + ' time!'
            return get_response(url, repeat_time)

        return r.json()
    except Exception as e:
        print e


def get_search_items(categories=search_key):
    """
    get search results and parse it return search item array
    :param categories category list
    """
    rep = []
    search_items = []
    if categories and len(categories) > 0:
        for category in categories:
            rep.append(get_response(search_url.format(category)))
    else:
        rep = get_response(search_url.format(search_key))
    if len(rep) <= 0:
        raise Exception('nothing search back')

    for r in rep:
        if not r:
            pass
        else:
            for item in r['searchItems']:
                if ('isMAStore' in item and item['isMAStore']) \
                        or ('modelQuickViewDetails' in item and item['modelQuickViewDetails']['isMAStore']):
                    search_items.append(item)
    return search_items


def get_product_urls(search_items):
    """
    get product urls from search items
    """
    urls = []
    for item in search_items:
        if 'productDetail' in item:
            urls.append(item['productDetail']['href'])

    return set(urls)


def get_products(categories):
    """
    get products
    the product object structure will be 
    {name:xxx, benefit: xxx}
    :param categories category list
    """
    products = []
    product_urls = get_product_urls(get_search_items(categories))
    num_product = 30
    if len(product_urls) < 30:
        num_product = len(product_urls)
    print 'GET PRODUCT URLs DONE!'

    for url in random.sample(product_urls, num_product):
        product = build_product(get_response(api_domain + url))
        if product:
            products.append(product)
    return parse(products)


def build_product(original_product):
    if not original_product:
        return

    print "BUILD PRODUCT: " + original_product['caption']
    extended_descriptions = original_product['extendedDescriptions']
    product = {
        'name': original_product['caption'],
        'store_name': original_product['storeName']
    }

    if len(extended_descriptions) > 0:
        if extended_descriptions[0]['caption'].upper() == 'Benefits'.upper() \
                and 'items' in extended_descriptions[0] and len(extended_descriptions[0]['items']):
            product['benefits'] = extended_descriptions[0]['items'][0]['description']
            return product

        if 'siblings' not in extended_descriptions[0]:
            product['benefits'] = []
            return product

        siblings = extended_descriptions[0]['siblings']
        for sibling in siblings:
            if sibling['caption'].upper() == 'Benefits'.upper() and len(sibling['items']) > 0:
                product['benefits'] = sibling['items'][0]['description']

    return product


def parse(products):
    print "START PARSE PRODUCTS, build benefits list"
    for product in products:
        try:
            if "benefits" in product and len(product['benefits']) > 0:
                selector = etree.HTML(product['benefits'])
                product['benefits'] = selector.xpath('//ul/li/text()')
                if 'benefits' not in product or len(product['benefits']) <= 0:
                    benefits_elms = selector.xpath('//div[@id="benefits"]/*/li')
                    if isinstance(benefits_elms, list):
                        product['benefits'] = ' '.join(
                            [text for elm in benefits_elms for text in elm.itertext() if elm])
        except KeyError as e:
            print e

    print "PARSE PRODUCTS DONE!"
    return products


if __name__ == "__main__":
    print get_products(search_key)
