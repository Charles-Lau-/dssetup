from django.http import HttpResponseRedirect

class PermissionWare():
    def process_view(self,request,view_func,view_args,view_kwargs):
        if(request.path.startswith("/admin")):
            requiredResource = view_func.__name__.split("_")[0]+"_"+view_kwargs["obj"]
            if(not  requiredResource in request.session["perm"]):
                pass
        elif(request.path.startswith("/handleForm")):
            if(request.path.startswith("/handleForm/apply_form/") and not "apply_form" in request.session["perm"]):
                return HttpResponseRedirect("/permission")