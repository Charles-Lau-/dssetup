#coding=utf-8
from django import template

register = template.Library()

@register.filter(name="strcat")
def strcat(value,arg):
    """ 、
        将两个可以转化成字符串的值进行拼接
    
    """
    return str(value) + str(arg)