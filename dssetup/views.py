#coding=utf-8
from django.shortcuts import render
from dssetup.models import User
from dssetup import staticVar
from django.http import HttpResponseRedirect 
from dssetup.decorator import login_required
from dssetup.service import adminService
# Create your views here.
def home(request):
    return HttpResponseRedirect("/index") 

def index(request):
    return render(request,"base.html",)
def login(request):
    if(request.POST):
        if(User(userName=request.POST.get("username"),userPassword=request.POST.get("password")).is_authenticated()):
            
            request.session["user"] = request.POST.get("username")
            request.session["perm"] = adminService.getPermOfUser(adminService.getUser(request))
            request.session["ip"] = request.META["REMOTE_ADDR"]
            import time
            now = time.localtime()
            request.session["time"] = now[:6]
            return HttpResponseRedirect("/index")
        else:
            return render(request,"login.html",{"error":"username or password is not correct"})
    else:
        return render(request,"login.html")
@login_required
def logout(request):
    adminService.logout(request.session["user"],request.session["ip"],request.session["time"])
    del request.session["user"]
    return HttpResponseRedirect("admin")
def permission(request):
    return render(request,"permission.html")