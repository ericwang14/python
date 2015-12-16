#! /usr/bin/python
# --* encoding=utf-8 --*--

from django.db import models

# Create your models here.


class User(models.Model):
    email = models.CharField(max_length=200, null=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    score = models.IntegerField(default=0)
    duration = models.CharField(max_length=200, default=0)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    creation_date = models.DateTimeField()
