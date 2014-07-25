#coding=utf-8
from dssetup.forms import UserForm,GroupForm,AuthorityForm,ZoneForm,DomainFormForm
from django.shortcuts import render 
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
        form = __generateForm(post=request.POST,obj=obj)
        if(form.is_valid()):
            form.save()
       
            return HttpResponseRedirect("/admin/"+obj)
        
        else:
            return render(request,"add.html",{"form":form,"obj":obj})
    else:
        form = __generateForm(obj=obj)
        return render(request,"add.html",{"form":form,"obj":obj})
@login_required
def edit_object(request,Id,obj):
    instance_ = adminService.getObjectById(obj, Id) 
    if(request.POST):
        form = __generateForm(post=request.POST,instance_=instance_,obj=obj)         
        
        if(form.is_valid()):
            form.save()
            return HttpResponseRedirect("/admin/"+obj)
        else: 
            return render(request,"edit.html",{"form":form,"obj":obj,"id":Id})

    else:
        form = __generateForm(instance_=instance_,obj=obj)         
        return render(request,"edit.html",{"form":form,"obj":obj,"id":Id})

def __generateForm(obj,post=None,instance_=None):
    if(obj == "user"):
        form = UserForm(data=post,instance=instance_)
    elif(obj == "group"):
        form = GroupForm(data=post,instance=instance_)
    elif(obj == "authority"):
        form = AuthorityForm(data=post,instance=instance_)
    elif(obj == "zone"):
        form = ZoneForm(data=post,instance=instance_)
    elif(obj =="domain"):
        form = DomainFormForm(data=post,instance=instance_)
    return form