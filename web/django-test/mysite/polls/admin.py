#! python
# -*-encoding=utf-8 -*-
#polls/admin.py
from django.contrib import admin

from .models import Question, Choice
# Register your models here.

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('quesiton_text', 'pub_date', 'was_published_recently')

admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice) # remove for now since we don't need separate page for choice

