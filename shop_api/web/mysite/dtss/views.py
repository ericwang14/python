#! /usr/bin/python
# --*-- encoding=UTF-8 --*--

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.core.urlresolvers import reverse
from .models import User

import smtplib
import string
import random
import json
import product_search

"""
DTSS main view controller

workflow

Index page --> start game --> pick up categories --> answer question 1 ~ 10 --> result & submit email --> save

@author ericw
@since 12/01/15
"""


# Create your views here.

sender = "yeak2002@gmail.com"
pwd = "wanggang1224"
category_list = ['Isotonix', 'Motives', 'Snap', 'Tls', 'Prime',
                 'Fixx', 'DNA Miracles', 'Cellular Laboratories']

default_question_count = 10


def index(request):
    request.session.clear()
    request.session.clear_expired()

    users = User.objects.filter(email__isnull=False).order_by('-score', 'duration')[:10]
    return render(request, 'dtss/index.html', {'users': users, })


def login(request):
    """
    create user info and send mail to user
    :param request:  request object
    :return:
    """
    try:
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        if not email:
            return render(request, 'dtss/results.html', {'error': 'Please enter email first!'})
        user = User.objects.get(pk=request.session.get("user_id"))
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        send_mail(user)
    except KeyError:
        return render(request, reverse('dtss:results'), {'error': 'Please enter email first!'})
    return HttpResponseRedirect(reverse('dtss:index'))


def send_mail(user):
    """
    send mail to user
    :param user: user object
    :return: None
    """
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.ehlo()
    smtp_server.starttls()
    smtp_server.login(sender, pwd)

    text = """Your score is {0}, duration {1}, you can go to http://www.shop.com to finish your registration.""".format(
        str(user.score), str(user.duration))

    message = string.join((
        "From: %s" % sender,
        "To: %s" % user.email,
        "Subject: Your DTSS game score!",
        "",
        "Hey {0},".format(user.first_name),
        "",
        text,
        ), "\r\n")

    message = message.format(sender, user.email, str(user.score), str(user.duration))

    smtp_server.sendmail(sender, user.email, message)
    smtp_server.close()


def main_question(request, question_id):
    """
    question controller
    :param request:     request object
    :param question_id: question id
    :return:
    """
    selected_categories = request.POST.getlist('categories')
    question_count = default_question_count
    if selected_categories:
        _load_product(request, selected_categories)
        if question_count > request.session.get('product_count'):
            question_count = request.session.get('product_count')

    if not request.session.get('products', None):
        return HttpResponseRedirect(reverse('dtss:index'))

    if int(question_id) <= 1:
        user = User(creation_date=timezone.now(), start_date=timezone.now())
        user.ip_address = get_client_ip(request)
        user.save()
        request.session['user_id'] = user.id

    if int(question_id) <= 0:
        return HttpResponseRedirect(reverse('dtss:question', args=(1,)))

    if int(question_id) > question_count:
        _update_question_answer(request, int(question_id))

        score = _check_score(request)
        user = User.objects.get(pk=request.session.get("user_id"))
        user.end_date = timezone.now()
        duration = (user.end_date - user.start_date).seconds
        user.score = score
        mins, seconds = divmod(duration, 60)
        user.duration = "%d:%d" % (mins, seconds)
        user.save()

        return HttpResponseRedirect(reverse('dtss:results'))

    products = request.session.get('products')
    product = pick_up_product(request, products)

    store_picked_product(request, product)

    benefit = random.choice(product['benefits'])
    while len(benefit.split(" ")) < 4:
        benefit = random.choice(product['benefits'])

    product['benefit'] = benefit.strip()

    benefits = build_random_benefits(products, product)
    print 'question product: ' + product['name']
    print "answer list: " + json.dumps(benefits)

    benefits.append(product['benefit'])

    context = {
        'counter': question_id,
        'next': int(question_id) + 1,
        'product': product,
        'benefits': random.sample(benefits, 4),
        'context_debug': 'main' in request.GET and request.GET['main'] == 'debug'
    }
    request.session[question_id] = {'right_product': product, }

    _update_question_answer(request, int(question_id))

    return render(request, 'dtss/qa.html', context)


def get_client_ip(request):
    """
    get client ip address
    :param request:     - request object
    :return: client ip
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def pick_up_product(request, products):
    """
    pick up question product from product list
    :param request:     - request object
    :param products:    - product list
    :return: question product
    """
    product = random.choice(products)
    picked_products = [] if 'picked_products' not in request.session else request.session['picked_products']
    while 'benefits' not in product or len(product['benefits']) <= 0 or product in picked_products:
        product = random.choice(products)

    return product


def store_picked_product(request, product):
    """
    store picked product into session or clear picked products if the stored size greater than 5
    :param request:     - request object
    :param product:     - picked product
    :return:
    """

    if "picked_products" not in request.session or len(request.session['picked_products']) > 5:
        request.session['picked_products'] = []

    request.session['picked_products'].append(product)


def is_product_used(request, product):
    for key, value in request.session.items():
        if type(value) != int and'right_product' in value \
                and value['right_product']['name'] == product['name']:
            return True

    return False


def _update_question_answer(request, question_id):
    """
    update question answer
    """
    if question_id == 1:
        return
    question_id -= 1
    answer = request.POST.get('answer', None)
    right_product = request.session.get(str(question_id))['right_product']
    request.session.get(str(question_id))['is_correct'] = (answer and answer == right_product['benefit'])


def _load_product(request, selected_categories):
    """
    if products dataSet existing in session return it
    otherwise load it and store it in session
    """
    products = request.session.get('products')
    if not products:
        products = product_search.get_products(selected_categories)
        request.session['products'] = products
        request.session['product_count'] = len(products)
    return products


def results(request):
    if request.session.is_empty():
        return HttpResponseRedirect(reverse('dtss:index'))

    user = User.objects.get(pk=request.session.get("user_id"))

    users = User.objects.filter(email__isnull=False).order_by('-score',  'duration')[:9]
    user_list = [s_user for s_user in users]
    user_list.append(user)
    user_list.sort(key=lambda item: (item.score, item.duration), reverse=True)

    return render(request, 'dtss/results.html', {'score': user.score, 'duration': user.duration, 'users': user_list})


def _check_score(request):
    score = 0
    for i in range(1, 11):
        product_answer = request.session.get(str(i))
        if product_answer and product_answer.get("is_correct"):
            score += 1
    return score


def build_random_benefits(products, right_product):
    """
    build random benefit list from given product list
    :param products:        - product list
    :param right_product:   - the product which choose by question
    :return: random benefit answer list the size is 3
    """
    benefits = set()
    for i in range(1, 4):
        product = random.choice(products)
        while 'benefits' not in product \
                or len(product['benefits']) <= 0 \
                or right_product['name'] == product['name']:
            product = random.choice(products)

        benefit = random.choice(product['benefits'])
        while benefit in benefits or benefit in right_product['benefits'] or len(benefit.split(" ")) < 4:
            benefit = random.choice(product['benefits'])

        benefits.add(benefit.strip())

    while len(benefits) < 3:
        return build_random_benefits(products, right_product)

    return list(benefits)[:3]


def question_verification(request, question_id):
    """
    verify selected question
    :param request:         - request object
    :param question_id:     - question id
    :return:    true mean right
    """
    if request.method == 'POST':
        answer = request.POST.get('answer')
        right_product = request.session.get(question_id)['right_product']
        verification_results = {}
        if answer and answer == right_product['benefit']:
            verification_results['is_correct'] = True
            request.session.get(question_id)["is_correct"] = True
        else:
            verification_results['is_correct'] = False
            request.session.get(question_id)["is_correct"] = False

        verification_results["text"] = "The best benefit of the product " \
                                       '"{0}" is {1}.'.format(right_product['name'].encode('utf-8').strip(),
                                                              right_product['benefit'].encode('utf-8').strip())
        verification_results["right_answer"] = right_product['benefit'].encode('utf-8').strip()
        return HttpResponse(
            json.dumps(verification_results),
            content_type="application/json; charset=UTF-8"
        )


def categories(request):
    """
    list all categories to let user pick up
    :param request: request objects
    :return:
    """
    request.session.clear()
    request.session.clear_expired()
    return render(request, 'dtss/categories.html', {"categories": category_list})
