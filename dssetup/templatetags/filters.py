#coding=utf-8
from django import template

register = template.Library()

@register.filter(name="strcat")
def strcat(value,arg):
    return value + arg