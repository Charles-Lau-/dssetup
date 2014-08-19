#coding=utf-8
from django.http import HttpResponseRedirect
from dssetup.models import  DomainApplication
from dssetup.service import userService
from django.shortcuts import get_object_or_404

class PermissionWare():
    """
      处理权限

    """
    def process_view(self,request,view_func,view_args,view_kwargs):
        #如果用户想登入后台部分的view
        if(request.path.startswith("/admin")):
            #后台部分如果要进行obj的增删查改 权限名为  show/edit/delete_obj 其他的 权限名和函数名一样。具体 查看adminURL 就明白了
            if(view_kwargs.get("obj")): 
                requiredResource = view_func.__name__.split("_")[0]+"_"+view_kwargs.get("obj")
            else:
                requiredResource = view_func.__name__       #后台部分的其他操作 权限名都和view function的名字一样
            if(not  requiredResource in request.session["perm"]):
                return HttpResponseRedirect("/permission")
                          
        #表单部分有三种情况的view访问：apply_form,show_xx_form,和 change form                  
        elif(request.path.startswith("/handleForm")):
            #申请表单对应的权限名字是apply_form 
            if(request.path.startswith("/handleForm/apply_form/") and not "apply_form" in request.session["perm"]):
                return HttpResponseRedirect("/permission")
            #展示表单列表view对应的权限名是show_xxxx
            elif(request.path.find("show")>=0):
                if(not view_func.__name__ in request.session["perm"]):
                    return HttpResponseRedirect("/permission")
            elif(request.path.startswith("/handleForm/check_form/")):
                requiredResource = view_kwargs["role"]+"_"+"check"
                if(not requiredResource in request.session["perm"]):
                    return HttpResponseRedirect("/permission")
                #检查是否以在地址栏输入表单id的方式 试图访问自己权限外的表单 主要针对申请者和审核者  因为 申请者应该只能看到自己申请的表单 审核者只能看到自己负责的表单
                else: 
                    if(view_kwargs["role"]=="applicant" and not DomainApplication.objects.get(id=view_kwargs["Id"]).creater==userService.getUser(request)):
                        return HttpResponseRedirect("/permission")
                    elif(view_kwargs["role"]=="verifier"):
                        zone = get_object_or_404(DomainApplication,id=view_kwargs["Id"]).getZoneOfApplicationForm()
                        if(zone and not zone.zone_dpt==userService.getUser(request).user_dpt):
                            return HttpResponseRedirect("/permission")
                            
                        
