#! /usr/bin/python
#--* encoding=utf-8 --*--

from django.db import models

# Create your models here.


class User(models.Model):
    email = models.CharField(max_length=200)
    score = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)
    creation_date = models.DateTimeField()
