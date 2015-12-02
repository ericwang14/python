#! /usr/bin/python
# --*-- encoding=utf-8 --*--

from HTMLParser import HTMLParser

import product_search
import parse_product
import random


"""
DTSS client
"""

answer_counter = {
    '1': 'A',
    '2': 'B',
    '3': 'C',
    '4': 'D'
}

def out_put():
    score = 0
    products = parse_product.parse()
    
    print '\n\r'
    print '\n\r'
    print "======================================================"
    print "****welcome to DTSS question game system!*****"
    print "********GAME START, PLEASE ENTER YOUR NAME: *****************"
    user_name = raw_input()
    print "======================================================"
    print '\n\r'
    print '\n\r'

    for i in range(1, 11):
        h = HTMLParser()
        product = random.choice(products)
        right_name = h.unescape(product['name'])
        product_names = [right_name] + [(lambda p: h.unescape(p['name']))(p) for p in random.sample(products, 3)]
        while 'benifits' not in product or len(product['benifits']) <= 0:
            product = random.choice(products)

        print '{0}. Please pick the one best benefit of the product "{1}"?'\
            .format(i, h.unescape(random.choice(product['benifits']).encode('utf-8').strip()))

        print '\n\r'
        count = 1
        for name in random.sample(product_names, 4):
            print '    {0}. {1}'.format(answer_counter[str(count)], name.encode('utf-8').strip())
            count += 1
        selected = raw_input('please select: ').upper()
        while (selected not in [value for key, value in answer_counter.iteritems()]):
            selected = raw_input('not right answer, please select again: ').upper()
        for k, v in answer_counter.iteritems():
            if v.upper() == selected:
                selected_count = int(k)

        if product_names[selected_count - 1] == right_name:
            score += 1
        print '\n\r'
        print '\n\r'


    print '\n\r'
    print '============================================================'
    print '****** GAME END YOUR {0} SCORE IS {1}'.format(user_name, str(score))
    print '==========================================================='






if __name__ == '__main__':
    out_put()

