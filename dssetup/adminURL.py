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
       url("^user/delete=(?P<Id>\d+)$",adminAction.delete_object,{"obj":"user"},name="delete_user"),
       url("^group/delete=(?P<Id>\d+)$",adminAction.delete_object,{"obj":"group"},name="delete_group"),
       url("^authority/delete=(?P<Id>\d+)$",adminAction.delete_object,{"obj":"authority"},name="delete_authority"),
       url("^user/edit=(?P<Id>\d+)$",adminAction.edit_object,{"obj":"user"},name="edit_user"),
       url("^group/edit=(?P<Id>\d+)$",adminAction.edit_object,{"obj":"group"},name="edit_group"),
       url("^authority/edit=(?P<Id>\d+)$",adminAction.edit_object,{"obj":"autority"},name="edit_authority"),                 
                       
                       
                       
                       )