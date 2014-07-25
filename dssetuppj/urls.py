from django.conf.urls import patterns, include, url
 
from dssetup import views
from dssetup import adminURL,formURL
 
urlpatterns = patterns('',
    url(r'^$', views.home,name="home"),
    url(r"^index$",views.index,name="index"),
    url(r"^login$",views.login,name="login"),
    url(r"^logout$",views.logout,name="logout"), 
    url(r"^admin/",include(adminURL)),
    url(r"^handleForm/",include(formURL)),
     
)
