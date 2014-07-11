from django.conf.urls import patterns, include, url
 
from dssetup import views
from dssetup.action import adminAction
 
urlpatterns = patterns('',
    url(r'^$', views.home,name="home"),
    url(r"^login$",views.login,name="login"),
    url(r"^logout$",views.logout,name="logout"),
    url(r"^control_center$",views.control_center,name="control_center"),
    url(r"^admin/",include(adminAction))
     
)
