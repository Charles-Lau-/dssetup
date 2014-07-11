from dssetup.forms import AccountForm,GroupForm,AuthorityForm
from django.core.paginator import  Paginator,EmptyPage,InvalidPage,PageNotAnInteger
from django.shortcuts import render
#coding=utf-8
from dssetup.models import Account,Group,Authority
from dssetup.staticVar import NUM_PER_PAGE,RIGHT_PAGES,LEFT_PAGES
from django.http import HttpResponseRedirect,Http404 
from dssetup.decorator import login_required

@login_required
def homepage(request):
    return show_object(request,"user")
@login_required
def show_object(request,obj):
    if(obj == "user"):
        objs_list = Account.objects.all()
    elif(obj == "group"):
        objs_list = Group.objects.all()
    else:
        objs_list = Authority.objects.all()
    
    
     

    return render(request,"index.html",{
                  "obj_list":objs_list,
                  "obj":obj,                     
                })
 
@login_required
def delete_object(request,Id,obj):
    if(obj == "user"):
        object_ = Account.objects.get(id=int(Id))
    elif(obj == "group"):
        object_ = Group.objects.get(id=int(Id))
    else:
        object_ = Authority.objects.get(id=int(Id))
     
    object_.delete()
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
    