#coding=utf-8
from dssetup.forms import AccountForm,GroupForm,AuthorityForm
from django.shortcuts import render
from dssetup.models import User,Group,Authority
from django.http import HttpResponseRedirect
from dssetup.decorator import login_required
from dssetup.service import adminService
@login_required
def homepage(request):
    return show_object(request,"user")
@login_required
def show_object(request,obj):
    return render(request,"index.html",{
                  "obj_list":adminService.getAllObject(obj),
                  "obj":obj,                     
                })
 
@login_required
def delete_object(request,Id,obj):
    adminService.deleteObjectById(obj, Id)
    return HttpResponseRedirect("/admin/"+obj+"/")

@login_required
def add_object(request,obj):
    if(request.POST):
        if(obj == "user"):
            form = AccountForm(request.POST)
        elif(obj == "group"):
            form = GroupForm(request.POST)
        else:
            form = AuthorityForm(request.POST)
            
        if(form.is_valid()):
            form.save()
            return HttpResponseRedirect("/admin/"+obj)
        
        else:
            return render(request,"add.html",{"form":form,"obj":obj})
    else:
        if(obj == "user"):
            form = AccountForm()
        elif(obj == "group"):
            form = GroupForm()
        else:
            form = AuthorityForm()
        return render(request,"add.html",{"form":form,"obj":obj})
@login_required
def edit_object(request,page,Id,obj):
    if(request.POST):
        pass
    else: 
        pass    
    