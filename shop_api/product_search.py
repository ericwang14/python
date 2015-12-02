#! /usr/bin/python
# --*-- encoding=utf-8 --*--
import requests
import random

"""
get products information
"""

api_key = 'l7xx175ed35d49844df29b26917291a11038'
api_domain = 'https://api.shop.com'
search_key = 'isotonix'
search_url = 'https://api.shop.com/sites/v1/search/Term/{0}'

def get_response(url):
    """
    get response for given url
    """

    try:
        r = requests.request(method='GET', url=url, headers={'apikey': api_key})
        if r.status_code != 200:
            return 'can not connect api site'
        return r.json()
    except Exception as e:
        print e

def get_search_items():
    """
    get search results and parse it return search item array
    """

    rep = get_response(search_url.format(search_key))
    if len(rep) <= 0:
        raise Exception('nothing search back')

    search_items = rep['searchItems']
    return search_items

def get_product_urls(search_items):
    """
    get product urls from search items
    """

    return [url['productDetail']['href'] for url in search_items]

def get_products():
    """
    get products
    the product object structure will be 
    {name:xxx, benifit: xxx}
    """
    products = []
    product_urls = get_product_urls(get_search_items())
    for url in random.sample(product_urls, 20):
        products.append(build_product(get_response(api_domain + url)))
    return products

def build_product(original_product):
    extended_descriptions = original_product['extendedDescriptions']
    product = {
        'name': original_product['caption'],
        'store_name': original_product['storeName']
    }
    
    if len(extended_descriptions) > 0:
        siblings = extended_descriptions[0]['siblings']
        for sibling in siblings:
            if sibling['caption'].upper() == 'Benefits'.upper() and len(sibling['items']) > 0:
                product['benifits'] = sibling['items'][0]['description']

    return product


if __name__ == "__main__":
    print get_products()

