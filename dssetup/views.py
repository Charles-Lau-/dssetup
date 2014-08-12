#coding=utf-8
from django.shortcuts import render
from dssetup.models import User
from django.http import HttpResponseRedirect 
from dssetup.service import adminService
import time

def home(request):
    """
        指向首页
        
    """
    return HttpResponseRedirect("/index") 

def index(request):
    """
        指向首页
        
    """
    return render(request,"base.html")

def login(request):
    """
      用来处理登录信息的

      session["user"] 用来标记是否已经登入
      session["perm"] 用来记住该登入用户的权限
      session["ip"]  用来记住本次登录ip 在登出的时候写入数据库
      session["time"] 用来记住本次登录的时间 在登出的时候写入数据库
      
    """
    if(request.POST):
        if(User(userName=request.POST.get("username"),userPassword=request.POST.get("password")).is_authenticated()):
            
            request.session["user"] = request.POST.get("username")
            request.session["perm"] = adminService.getPermOfUser(adminService.getUser(request))
            request.session["ip"] = request.META["REMOTE_ADDR"]
            now = time.localtime()
            request.session["time"] = now[:6]
            return HttpResponseRedirect("/index")
        else:
            return render(request,"login.html",{"error":"username or password is not correct"})
    else:
        return render(request,"login.html")

def logout(request):
    """
     处理登出的操作
  
    """
    adminService.logout(request)
    
    return HttpResponseRedirect("/index")
def permission(request):
    """
     处理权限不够的情况

    """
    return render(request,"permission.html")
