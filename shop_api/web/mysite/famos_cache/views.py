#! /usr/bin/python
# --*-- encoding=UTF-8 --*--

# Create your views here.
from django.shortcuts import render
from famos_cache.models import AppServer, Site, Environment
from concurrent import futures

import requests

url = '%s/cacheclear.xhtml?host=%s&services=%s&name=messageSources'


def index(request):
    """
    index page load env and site list
    :param request: request object

    """
    envs = Environment.objects.all()
    sites = Site.objects.all()

    return render(request, 'famos_cache/index.html', {'envs': envs, 'sites': sites,})


def clear(request):
    """
    clear FAMOS cache
    :param request:  request object
    :return:
    """

    envs = Environment.objects.filter(name__in=request.POST.getlist('envs'))
    sites = Site.objects.filter(name__in=request.POST.getlist('sites'))

    clear_urls = []
    for env in envs:
        apps = AppServer.objects.filter(env__name__exact=env.name)

        keys = request.POST.getlist('keys')

        if len(keys) <= 0 or len(sites) <= 0:
            return render(request, 'famos_cache/done.html', {'clear_urls': clear_urls})

        for app in apps:
            if keys:
                for key in keys:
                    for site in sites:
                        clear_url = url % (app.name, env.host, env.service_url)
                        clear_url += "&key=" + key.strip()
                        clear_url += "&locale=" + site.locale.strip()
                        # requests.get(clear_url)
                        clear_urls.append(clear_url)

    with futures.ThreadPoolExecutor(50) as executor:
        fs = [executor.map(request_to_clear, [clear_url]) for clear_url in clear_urls]
        # futures.wait(fs)

    return render(request, 'famos_cache/done.html', {'clear_urls': clear_urls})


def request_to_clear(clear_url):
    print("calling: " + clear_url)
    requests.get(clear_url)
    print("calling end!\n")

#
# class myThread(threading.Thread):
#     def __init__(self, thread_id, name, request_url):
#         """
#
#         :rtype: object
#         """
#         threading.Thread.__init__(self)
#         self.thread_id = thread_id
#         self.name = name
#         self.request_url = request_url
#
#     def run(self):
#         print("thread: " + self.name + " calling: " + self.request_url)
#         requests.get(self.request_url)
#         print("thread: " + self.name + " calling end!\n")
