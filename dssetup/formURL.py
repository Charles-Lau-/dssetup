#coding=utf-8
from django.conf.urls import patterns, url
from dssetup.action import formAction
 

urlpatterns =  patterns('',                 
       url(r"^show_applied_form$",formAction.showAppliedForm,name="show_applied_form"),
       url(r"show_unverified_form$",formAction.showUnverifiedForm,name="show_unverified_form"),
        url(r"show_unchecked_form$",formAction.showUncheckedForm,name="show_unchecked_form"),
       url(r"show_unimplemented_form",formAction.showUnimplementedForm,name="show_unimplemented_form"),                
       url( r"^apply_form/create_main_form",formAction.createDomainForm,name="create_main_form"),
       url(r"^apply_form/create_mapping_form/(?P<domainName>\S*)$",formAction.createMappingForm,name="create_mapping_form"),
       url(r"^apply_form/store_domainName$",formAction.storeDomainName,name="store_domainName"),
       url(r"^apply_form/create_mapping_part$",formAction.createMappingPart,name="create_mapping_part"),
       url(r"^apply_form/delete_mapping_form/(?P<domainName>\S+)/(?P<Id>\d+)$",formAction.deleteMappingForm,name="delete_mapping_form"),
       url(r"^apply_form/delete_domain_form/(?P<domainName>\S+)$",formAction.deleteDomainForm,name="delete_domain_form"),  
       url(r"^apply_form/submit$",formAction.addFormIntoDatabase,name="add_form"),                 
       url(r"^check_form/(?P<Id>\d+)/(?P<role>\S*)$",formAction.checkForm,name="check_form"),
       url(r"^change_form/(?P<Id>\d+)/(?P<operation>\S+)$",formAction.changeForm,name="change_form_status"),
       url(r"^edit_form/(?P<Id>\d+)/(?P<step>\d*)$",formAction.editForm,name="edit_form"),                
            )