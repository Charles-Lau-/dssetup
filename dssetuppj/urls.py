#coding=utf-8
from django.conf.urls import patterns, include, url
 
from dssetup import views
from dssetup import adminURL,formURL
 
urlpatterns = patterns('',
    url(r'^$', views.home,name="home"),                         #首页
    url(r"^index/$",views.index,name="index"),                  #首页
    url(r"^login/$",views.login,name="login"),                  #登录页面
    url(r"^logout/$",views.logout,name="logout"),               #登出
    url(r"^permission/$",views.permission,name="permission"),   #提示用户没有该权限的页面
    url(r"^admin/",include(adminURL)),                          #所有和后台操作相关的页面都在admin/下面
    url(r"^handleForm/",include(formURL)),                      #所有和表单操作相关的页面都在form、下面
     
)
