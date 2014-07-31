from django.http import HttpResponseRedirect
from dssetup.models import  DomainApplicationForm,DomainForm
from dssetup.service import adminService

class PermissionWare():
    def process_view(self,request,view_func,view_args,view_kwargs):
        if(request.path.startswith("/admin")):
            requiredResource = view_func.__name__.split("_")[0]+"_"+view_kwargs["obj"]
            if(not  requiredResource in request.session["perm"]):
                pass
        elif(request.path.startswith("/handleForm")): 
            if(request.path.startswith("/handleForm/apply_form/") and not "apply_form" in request.session["perm"]):
                return HttpResponseRedirect("/permission")
            elif(request.path.find("show")>=0):
                if(not view_func.__name__ in request.session["perm"]):
                    return HttpResponseRedirect("/permission")
            elif(request.path.startswith("/handleForm/check_form/")):
                requiredResource = view_kwargs["role"]+"_"+"check"
                if(not requiredResource in request.session["perm"]):
                    return HttpResponseRedirect("/permission")
                else:
                    if(view_kwargs["role"]=="applicant" and not DomainApplicationForm.objects.get(id=view_kwargs["Id"]).creater==adminService.getUser(request)):
                        return HttpResponseRedirect("/permission")
                    elif(view_kwargs["role"]=="verifier"):
                        domain = DomainForm.objects.filter(da_domain=DomainApplicationForm.objects.get(id=view_kwargs["Id"]))    
                        if(domain and not domain[0].domain_zone.zone_dpt==adminService.getUser(request).user_dpt):
                            return HttpResponseRedirect("/permission")
                            
                        