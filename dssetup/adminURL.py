#coding=utf-8
from django.conf.urls import patterns, url
from dssetup.action import adminAction,groupAction,domainAction
 
#show_XXX 是当你提交显示某个对象列表的时候 使用的 比如展示用户列表
#edit_xxx , delete_xxx 和add_xxx 分别对应 编辑 删除 添加对象
#add_user_to_group,domain_statistics 分别是  批量添加用户到某个群组 和  统计域名申请量
urlpatterns =  patterns('',
       url(r"^$",adminAction.show_object,{"obj":"user"},name="admin_home"),                
       url(r"^add_user/$",adminAction.add_object,{"obj":"user"},name="add_user"),
       url(r"^add_group/$",adminAction.add_object,{"obj":"group"},name="add_group"),
       url(r"^add_authority/$",adminAction.add_object,{"obj":"authority"},name="add_authority"),
       url(r"^add_zone/$",adminAction.add_object,{"obj":"zone"},name="add_zone"),
     
       url(r"^show_user/$",adminAction.show_object,{"obj":"user"},name="show_user"),            
       url(r"^show_group/$",adminAction.show_object,{"obj":"group"},name="show_group"),            
       url(r"^show_authority/$",adminAction.show_object,{"obj":"authority"},name="show_authority"), 
       url(r"^show_domain/$",adminAction.show_object,{"obj":"domain"},name="show_domain"),               
       url(r"^show_zone/$",adminAction.show_object,{"obj":"zone"},name="show_zone"),               
      
       url(r"^domain/delete=(?P<Id>\d+)/$",adminAction.delete_object,{"obj":"domain"},name="delete_domain"),
       url(r"^user/delete=(?P<Id>\d+)/$",adminAction.delete_object,{"obj":"user"},name="delete_user"),
       url(r"^group/delete=(?P<Id>\d+)/$",adminAction.delete_object,{"obj":"group"},name="delete_group"),
       url(r"^authority/delete=(?P<Id>\d+)/$",adminAction.delete_object,{"obj":"authority"},name="delete_authority"),
       url(r"^zone/delete=(?P<Id>\d+)/$",adminAction.delete_object,{"obj":"zone"},name="delete_zone"),
       
       url(r"^zone/edit=(?P<Id>\d+)/$",adminAction.edit_object,{"obj":"zone"},name="edit_zone"),
       url(r"^domain/edit=(?P<Id>\d+)/$",adminAction.edit_object,{"obj":"domain"},name="edit_domain"),
       url(r"^user/edit=(?P<Id>\d+)/$",adminAction.edit_object,{"obj":"user"},name="edit_user"),
       url(r"^group/edit=(?P<Id>\d+)/$",adminAction.edit_object,{"obj":"group"},name="edit_group"),
       url(r"^authority/edit=(?P<Id>\d+)/$",adminAction.edit_object,{"obj":"authority"},name="edit_authority"),  
       
       url(r"^add_user_to_group/(?P<Id>\d+)/$",groupAction.addUserToGroup,name="add_user_to_group"),  
       url(r"^domain_statistics/(?P<year>\d*)?$",domainAction.domainStatistics,name="domain_statistics"),             
       url(r"^domain/(?P<Id>\d+)/$",domainAction.showDetailOfDomain,name="show_detail_of_domain"),
                       
                       
                       )