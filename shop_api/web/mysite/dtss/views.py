from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.http import Http404

from .models import User

import random
import parse_product

# Create your views here.

def index(request):
    users = User.objects.order_by('score', 'duration')
    return render(request, 'dtss/index.html', {'users': users,})

def login(request):
    if not 'email' in request.POST:
        return render(request, 'dtss/login.html')
    if (request.session.get('email')):
        return HttpResponseRedirect(reverse('dtss:question', args=(1,)))
    try:
        email = request.POST['email']
        if not email:
            return render(request, 'dtss/login.html', {'error': 'Please enter email first!'})
        create_date = timezone.now()
        user = User(email=email, creation_date=timezone.now())
        user.save()
        request.session.set_expiry(600) # session will exipred after 10 mins
        request.session['email'] = email
        request.session['user_id'] = user.id
        _load_product(request)
    except KeyError:
        return render(request, reverse('dtss:login'), {'error': 'Please enter email first!'})
    return HttpResponseRedirect(reverse('dtss:question', args=(1,)))

def main_question(request, question_id):
    if (not request.session.get('email')):
        return HttpResponseRedirect(reverse('dtss:index'))

    if (int(question_id) <= 0):
      #  request.session['end_time'] = timezone.now()
        raise Http404("Page Not Found")

    if (int(question_id) > 10):
        _update_question_answer(request, int(question_id))
        return HttpResponseRedirect(reverse('dtss:results'))
    
    email = request.session.get('email')
    products = request.session.get('products')
    product = random.choice(products)
    while 'benifits' not in product or len(product['benifits']) <= 0:
        product = random.choice(products)
    
    r_products =  random.sample([product] + build_random_product(products), 4)

    product['benifit'] = random.choice(product['benifits'])
    context = {
        'counter': question_id,
        'next': int(question_id)+1,
        'email': email,
        'product': product,
        'random_products': r_products
    }
    request.session[question_id] = {'right_product': product,}
    
    _update_question_answer(request, int(question_id))


    return render(request, 'dtss/qa.html', context)

def _update_question_answer(request, question_id):
    """
    update question answer
    """
    if question_id == 1:
        return
    question_id = question_id - 1
    #answer = 'TLS Detox Kit'
    answer = request.POST.get('answer', None)
    if (question_id == 10):
        answer = 'asdfasdf'
    #if (request.session.get(str(question_id)) and answer):
    request.session.get(str(question_id))['answer'] = answer

def _load_product(request):
    """
    if products dataset existing in session return it
    otherwise load it and store it in session
    """
    products = request.session.get('products')
    if (not products):
        products = parse_product.parse()
        request.session['products'] = products
    return products


def results(request):
    user = User.objects.get(pk=request.session.get('user_id'))
    user.score = _check_score(request)
    user.save()
    return render(request, 'dtss/results.html', {'email': user.email, 'user': user, })

def _check_score(request):
    score = 1
    for i in range(1, 11):
        product_answer = request.session.get(str(i))
        if ('answer' in product_answer and product_answer['right_product']['name'] == product_answer['answer']):
           score += 1
    return score

def build_random_product(products):
    r_products = random.sample(products, 3)
    return r_products
