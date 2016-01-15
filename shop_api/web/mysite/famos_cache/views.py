#! /usr/bin/python
# --*-- encoding=UTF-8 --*--

# Create your views here.
from django.shortcuts import render
from famos_cache.models import AppServer, Site, Environment

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
                        requests.get(clear_url)
                        clear_urls.append(clear_url)

    return render(request, 'famos_cache/done.html', {'clear_urls': clear_urls})




