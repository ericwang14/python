from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Environment(models.Model):
    name = models.CharField(max_length=200, null=False)
    service_url = models.CharField(max_length=200)
    host = models.CharField(max_length=200)


class Site(models.Model):
    name = models.CharField(max_length=200, null=False)
    locale = models.CharField(max_length=200, null=False)


class AppServer(models.Model):
    name = models.CharField(max_length=200, null=False)
    env = models.ForeignKey(Environment, on_delete=models.CASCADE)
