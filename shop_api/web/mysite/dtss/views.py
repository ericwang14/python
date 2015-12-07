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
import parse_product

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
category_list = ['isotonix', 'motives', 'snap', 'tls', 'prime',
                 'fixx', 'DNA Miracles', 'Cellular Laboratories']


def index(request):
    request.session.clear()
    request.session.clear_expired()

    users = User.objects.filter(email__isnull=False).order_by('-score', '-duration')
    return render(request, 'dtss/index.html', {'users': users, })


def login(request):
    """
    create user info and send mail to user
    :param request:  request object
    :return:
    """
    try:
        email = request.POST['email']
        if not email:
            return render(request, 'dtss/results.html', {'error': 'Please enter email first!'})
        user = User.objects.get(pk=request.session.get("user_id"))
        user.email = email
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

    text = """Your score is {0}, duration seconds {1}, you can go to http://www.shop.com to finish your registration.""".format(
        str(user.score), str(user.duration))

    message = string.join((
        "From: %s" % sender,
        "To: %s" % user.email,
        "Subject: Your DTSS game score!",
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
    if selected_categories:
        _load_product(request, selected_categories)

    if not request.session.get('products', None):
        return HttpResponseRedirect(reverse('dtss:index'))

    if int(question_id) <= 1:
        user = User(creation_date=timezone.now(), start_date=timezone.now())
        user.save()
        request.session['user_id'] = user.id

    if int(question_id) <= 0:
        return HttpResponseRedirect(reverse('dtss:question', args=(1,)))

    if int(question_id) > 10:
        _update_question_answer(request, int(question_id))

        user = User.objects.get(pk=request.session.get("user_id"))
        user.end_date = timezone.now()
        user.save()

        return HttpResponseRedirect(reverse('dtss:results'))

    products = request.session.get('products')
    product = random.choice(products)
    while 'benifits' not in product or len(product['benifits']) <= 0:
        product = random.choice(products)

    product['benifit'] = random.choice(product['benifits'])

    benifits = [product['benifit']] + build_random_benefits(products)

    context = {
        'counter': question_id,
        'next': int(question_id) + 1,
        'product': product,
        'benifits': random.sample(benifits, 4)
    }
    request.session[question_id] = {'right_product': product, }

    _update_question_answer(request, int(question_id))

    return render(request, 'dtss/qa.html', context)


def _update_question_answer(request, question_id):
    """
    update question answer
    """
    if question_id == 1:
        return
    question_id -= 1
    answer = request.POST.get('answer', None)
    right_product = request.session.get(str(question_id))['right_product']
    if answer and answer == right_product['benifit']:
        request.session.get(str(question_id))['is_correct'] = True


def _load_product(request, selected_categories):
    """
    if products dataSet existing in session return it
    otherwise load it and store it in session
    """
    products = request.session.get('products')
    if not products:
        products = parse_product.parse(selected_categories)
        request.session['products'] = products
    return products


def results(request):
    score = _check_score(request)
    user = User.objects.get(pk=request.session.get("user_id"))
    duration = (user.end_date - user.start_date).seconds
    user.score = score
    user.duration = duration
    user.save()

    return render(request, 'dtss/results.html', {'score': score, 'duration': duration})


def _check_score(request):
    score = 0
    for i in range(1, 11):
        product_answer = request.session.get(str(i))
        if product_answer.get("is_correct"):
            score += 1
    return score


def build_random_benefits(products):
    benefits = []
    for i in range(1, 4):
        product = random.choice(products)
        while 'benifits' not in product or len(product['benifits']) <= 0:
            product = random.choice(products)
        benefits.append(random.choice(product['benifits']))

    return benefits


def question_verification(request, question_id):
    if request.method == 'POST':
        answer = request.POST.get('answer')
        right_product = request.session.get(question_id)['right_product']
        verification_results = {}
        if answer and answer == right_product['benifit']:
            verification_results['is_correct'] = True
            request.session.get(question_id)["is_correct"] = True
        else:
            verification_results['is_correct'] = False
            request.session.get(question_id)["is_correct"] = False

        verification_results["text"] = "The best benefit of the product " \
                                       '"{0}" is {1}.'.format(right_product['name'].encode('utf-8').strip(),
                                                              right_product['benifit'].encode('utf-8').strip())
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

    return render(request, 'dtss/categories.html', {"categories": category_list})
