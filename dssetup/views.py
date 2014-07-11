#coding=utf-8
from django.shortcuts import render
from dssetup.models import Account
from dssetup import staticVar
from django.http import HttpResponseRedirect 
from dssetup.decorator import login_required
# Create your views here.
def home(request):
    return render(request,"login.html") 


def login(request):
    if(request.POST):
        if(Account(username=request.POST.get("username"),password=request.POST.get("password")).is_authenticated()):
            request.session["user"] = request.POST.get("username")
            
            return HttpResponseRedirect("control_center")
        else:
            return render(request,"login.html",{"error":"username or password is not correct"})
    else:
        return render(request,"login.html")
@login_required
def logout(request):
    del request.session["user"]
    return HttpResponseRedirect("admin")
@login_required
def control_center(request):
         
    user = Account.objects.get(username=request.session.get("user"))
    if(user.group.get(groupName = staticVar.ADMINISTRATOR)):
        return HttpResponseRedirect("admin")
    else:
        return render(request," ")