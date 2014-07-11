#coding=utf-8
from django.http import HttpResponseRedirect
def login_required(function):
    def _login_required(request,*args,**kwargs):
            if(not request.session.get("user")):
                return HttpResponseRedirect("/")
            else:
                return function(request,*args,**kwargs)
    return _login_required

            
            
    