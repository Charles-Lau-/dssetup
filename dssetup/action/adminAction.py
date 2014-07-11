#coding=utf-8
from django.conf.urls import patterns, url
 
from dssetup.service import adminService
 

urlpatterns =  patterns('',
       url(r"^$",adminService.homepage,name="admin_home"),                
       url("^add_user$",adminService.add_object,{"obj":"user"},name="add_user"),
       url("^add_group$",adminService.add_object,{"obj":"group"},name="add_group"),
       url("^add_authority$",adminService.add_object,{"obj":"authority"},name="add_authority"),
       url("^user/$",adminService.show_object,{"obj":"user"},name="show_user"),            
       url("^group/$",adminService.show_object,{"obj":"group"},name="show_group"),            
       url("^authority/$",adminService.show_object,{"obj":"authority"},name="show_authority"),                        
       url("^user/delete=(?P<Id>\d+)$",adminService.delete_object,{"obj":"user"},name="delete_user"),
       url("^group/delete=(?P<Id>\d+)$",adminService.delete_object,{"obj":"group"},name="delete_group"),
       url("^authority/delete=(?P<Id>\d+)$",adminService.delete_object,{"obj":"authority"},name="delete_authority"),
       url("^user/edit=(?P<Id>\d+)$",adminService.edit_object,{"obj":"user"},name="edit_user"),
       url("^group/edit=(?P<Id>\d+)$",adminService.edit_object,{"obj":"group"},name="edit_group"),
       url("^authority/edit=(?P<Id>\d+)$",adminService.edit_object,{"obj":"autority"},name="edit_authority"),                 
                       
                       
                       
                       )