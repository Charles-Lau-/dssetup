#coding=utf-8
from django.conf.urls import patterns, url
from dssetup.action import adminAction
 

urlpatterns =  patterns('',
       url(r"^$",adminAction.show_object,{"obj":"user"},name="admin_home"),                
       url(r"^add_user/$",adminAction.add_object,{"obj":"user"},name="add_user"),
       url(r"^add_group/$",adminAction.add_object,{"obj":"group"},name="add_group"),
       url(r"^add_authority/$",adminAction.add_object,{"obj":"authority"},name="add_authority"),
       url(r"^user/$",adminAction.show_object,{"obj":"user"},name="show_user"),            
       url(r"^group/$",adminAction.show_object,{"obj":"group"},name="show_group"),            
       url(r"^authority/$",adminAction.show_object,{"obj":"authority"},name="show_authority"), 
       
       url(r"^domain/$",adminAction.show_object,{"obj":"domain"},name="show_domain"),               
       url(r"^domain/delete=(?P<Id>\d+)/$",adminAction.delete_object,{"obj":"domain"},name="delete_domain"),
       url(r"^domain/edit=(?P<Id>\d+)/$",adminAction.edit_object,{"obj":"domain"},name="edit_domain"),
       
       url(r"^zone/$",adminAction.show_object,{"obj":"zone"},name="show_zone"),               
       url(r"^zone/delete=(?P<Id>\d+)/$",adminAction.delete_object,{"obj":"zone"},name="delete_zone"),
       url(r"^zone/edit=(?P<Id>\d+)/$",adminAction.edit_object,{"obj":"zone"},name="edit_zone"),
       url(r"^add_zone/$",adminAction.add_object,{"obj":"zone"},name="add_zone"),
      
                             
       url(r"^user/delete=(?P<Id>\d+)/$",adminAction.delete_object,{"obj":"user"},name="delete_user"),
       url(r"^group/delete=(?P<Id>\d+)/$",adminAction.delete_object,{"obj":"group"},name="delete_group"),
       url(r"^authority/delete=(?P<Id>\d+)/$",adminAction.delete_object,{"obj":"authority"},name="delete_authority"),
       url(r"^user/edit=(?P<Id>\d+)/$",adminAction.edit_object,{"obj":"user"},name="edit_user"),
       url(r"^group/edit=(?P<Id>\d+)/$",adminAction.edit_object,{"obj":"group"},name="edit_group"),
       url(r"^authority/edit=(?P<Id>\d+)/$",adminAction.edit_object,{"obj":"authority"},name="edit_authority"),  
       
       url(r"^add_user_to_group/(?P<Id>\d+)/$",adminAction.addUserToGroup,name="add_user_to_group"),  
       url(r"^domain_statistics/(?P<year>\d*)?$",adminAction.domainStatistics,name="domain_statistics")             
                       
                       
                       )