#coding=utf-8
from django.conf.urls import patterns, url
from dssetup.action import formAction
 

urlpatterns =  patterns('',
       url(r"^$",formAction.homepage,name="handleForm_home"),                
       url( r"^create_main_form",formAction.createForm,{"formName":"main"},name="create_main_form"),
       url(r"^create_mapping_form$",formAction.createForm,{"formName":"mapping"},name="create_mapping_form"),
       url(r"^create_mapping_part$",formAction.createMappingPart,name="create_mapping_part"),
       url(r"^delete_mapping_form/(?P<domainName>\S+)/(?P<Id>\d+)$",formAction.deleteMappingForm,name="delete_mapping_form"),                
       url(r"^checkform/Id=(?P<Id>\d+)$",formAction.checkForm,name="check_form"),                
            )