#coding=utf-8
from django.shortcuts import render,redirect
from dssetup.service import groupService 

def addUserToGroup(request,Id):
    """ 
       批量添加用户到群组里面

       Id:表示权限组的id     
    """
    if(request.POST):
        for userId in request.POST.getlist("userIds"):
            groupService.addUserIntoGroup(Id, userId)
        return redirect("/admin/group/")
    else:
        return render(request,"user_into_group.html",{"users":groupService.getUsersNotInThisGroup(Id),"Id":Id}) 