#coding=utf-8
from django.conf.urls import patterns, url
from dssetup.action import adminAction
 

urlpatterns =  patterns('',
       url(r"^$",adminAction.homepage,name="admin_home"),                
       url("^add_user$",adminAction.add_object,{"obj":"user"},name="add_user"),
       url("^add_group$",adminAction.add_object,{"obj":"group"},name="add_group"),
       url("^add_authority$",adminAction.add_object,{"obj":"authority"},name="add_authority"),
       url("^user/$",adminAction.show_object,{"obj":"user"},name="show_user"),            
       url("^group/$",adminAction.show_object,{"obj":"group"},name="show_group"),            
       url("^authority/$",adminAction.show_object,{"obj":"authority"},name="show_authority"), 
       
       url("^domain/$",adminAction.show_object,{"obj":"domain"},name="show_domain"),               
       url("^domain/delete=(?P<Id>\d+)$",adminAction.delete_object,{"obj":"domain"},name="delete_domain"),
       url("^domain/edit=(?P<Id>\d+)$",adminAction.edit_object,{"obj":"domain"},name="edit_domain"),
       
       url("^zone/$",adminAction.show_object,{"obj":"zone"},name="show_zone"),               
       url("^zone/delete=(?P<Id>\d+)$",adminAction.delete_object,{"obj":"zone"},name="delete_zone"),
       url("^zone/edit=(?P<Id>\d+)$",adminAction.edit_object,{"obj":"zone"},name="edit_zone"),
       url("^add_zone$",adminAction.add_object,{"obj":"zone"},name="add_zone"),
      
                             
       url("^user/delete=(?P<Id>\d+)$",adminAction.delete_object,{"obj":"user"},name="delete_user"),
       url("^group/delete=(?P<Id>\d+)$",adminAction.delete_object,{"obj":"group"},name="delete_group"),
       url("^authority/delete=(?P<Id>\d+)$",adminAction.delete_object,{"obj":"authority"},name="delete_authority"),
       url("^user/edit=(?P<Id>\d+)$",adminAction.edit_object,{"obj":"user"},name="edit_user"),
       url("^group/edit=(?P<Id>\d+)$",adminAction.edit_object,{"obj":"group"},name="edit_group"),
       url("^authority/edit=(?P<Id>\d+)$",adminAction.edit_object,{"obj":"authority"},name="edit_authority"),  
                      
                       
                       
                       )