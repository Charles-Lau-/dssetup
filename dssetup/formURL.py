#coding=utf-8
from django.conf.urls import patterns, url
from dssetup.action import formAction
 

urlpatterns =  patterns('',
       url(r"^$",formAction.homepage,name="handleForm_home"),                
       url( r"^create_main_form",formAction.createDomainForm,name="create_main_form"),
       url(r"^create_mapping_form/(?P<domainName>\S*)$",formAction.createMappingForm,name="create_mapping_form"),
       url(r"^store_domainName$",formAction.storeDomainName,name="store_domainName"),
       url(r"^create_mapping_part$",formAction.createMappingPart,name="create_mapping_part"),
       url(r"^delete_mapping_form/(?P<domainName>\S+)/(?P<Id>\d+)$",formAction.deleteMappingForm,name="delete_mapping_form"), 
       url(r"^addform$",formAction.addFormIntoDatabase,name="add_form"),                 
       url(r"^checkform/Id=(?P<Id>\d+)$",formAction.checkForm,name="check_form"),                
            )