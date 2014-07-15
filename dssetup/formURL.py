#coding=utf-8
from django.conf.urls import patterns, url
from dssetup.action import formAction
 

urlpatterns =  patterns('',
       url(r"^$",formAction.homepage,name="handleForm_home"),                
       url( r"^create",formAction.createForm,name="create_form"),             
                       
                       
            )