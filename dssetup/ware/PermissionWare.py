#coding=utf-8
from django.http import HttpResponseRedirect
from dssetup.models import  DomainApplicationForm 
from dssetup.service import adminService
from django.shortcuts import get_object_or_404

class PermissionWare():
    """
      处理权限

    """
    def process_view(self,request,view_func,view_args,view_kwargs):
        if(request.path.startswith("/admin")): #如果用户想登入后台部分的view
            if(view_kwargs.get("obj")): #后台部分如果要进行obj的增删查改 权限名为 edit/delete_obj 
                requiredResource = view_func.__name__.split("_")[0]+"_"+view_kwargs.get("obj")
            else:
                requiredResource = view_func.__name__       #后台部分的其他操作 权限名都和view function的名字一样
            if(not  requiredResource in request.session["perm"]):
                return HttpResponseRedirect("/permission")
                          
                          
        elif(request.path.startswith("/handleForm")): #表单部分有三种情况的view访问：apply_form,show_xx_form,和 change form
            if(request.path.startswith("/handleForm/apply_form/") and not "apply_form" in request.session["perm"]):
                return HttpResponseRedirect("/permission")
            elif(request.path.find("show")>=0):
                if(not view_func.__name__ in request.session["perm"]):
                    return HttpResponseRedirect("/permission")
            elif(request.path.startswith("/handleForm/check_form/")):
                requiredResource = view_kwargs["role"]+"_"+"check"
                if(not requiredResource in request.session["perm"]):
                    return HttpResponseRedirect("/permission")
                else: #检查是否以在地址栏输入表单id的方式 试图访问自己权限外的表单 主要针对申请者和审核者
                    if(view_kwargs["role"]=="applicant" and not DomainApplicationForm.objects.get(id=view_kwargs["Id"]).creater==adminService.getUser(request)):
                        return HttpResponseRedirect("/permission")
                    elif(view_kwargs["role"]=="verifier"):
                        zone = get_object_or_404(DomainApplicationForm,id=view_kwargs["Id"]).getZoneOfApplicationForm()
                        if(zone and not zone.zone_dpt==adminService.getUser(request).user_dpt):
                            return HttpResponseRedirect("/permission")
                            
                        
