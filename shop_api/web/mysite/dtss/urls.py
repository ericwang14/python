#! /usr/bin/python


from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index$', views.index, name='index'),
    url(r'^category$', views.categories, name='categories'),
    url(r'^question/(?P<question_id>[0-9]+)/$', views.main_question, name='question'),
    url(r'^question/(?P<question_id>[0-9]+)/verify$', views.question_verification, name='question_verification'),
    url(r'^login$', views.login, name='login'),
    url(r'^results$', views.results, name='results'),
]
