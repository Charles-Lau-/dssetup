from dssetup.forms import DomainApplicationFormForm,DomainForm
from django.shortcuts import render 
from django.http import HttpResponseRedirect,HttpResponse
from django.forms.formsets import formset_factory
from dssetup.models import User
from dssetup.decorator import login_required
from dssetup import staticVar
from dssetup.service import formService
@login_required
def homepage(request):
    user = User.objects.get(userName=request.session["user"])
 
    if(user.group.get(groupName = staticVar.APPLICANT)):
        form_list = formService.getFormOfApplicant(user)
    
    
    return render(request,"formlist.html",{
                  "formlist":form_list,                          
                  "role":staticVar.APPLICANT
                })

def createForm(request):
    DomainApplicationFormset = formset_factory(DomainApplicationFormForm)
    DomainFormset = formset_factory(DomainForm)
 
       
    if(request.POST):
        domainApplicationForm = DomainApplicationFormset(request.POST,prefix="main_part")
        domainForm = DomainFormset(request.POST,prefix="mapping_part")
        
        if(domainApplicationForm.is_valid() and domainForm.is_valid()):
            for f in domainForm:
                print f.cleaned_data
            return HttpResponseRedirect("/handleForm")
        else:
            return  render(request,"createform.html",{"main_part":domainApplicationForm,"mapping_part":domainForm})

    else:
        
        domainApplicationForm = DomainApplicationFormset(prefix="main_part")
        domainForm = DomainFormset(prefix="mapping_part")
        return render(request,"createform.html",{"main_part":domainApplicationForm,"mapping_part":domainForm})
