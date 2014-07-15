from dssetup.forms import UserForm,GroupForm,AuthorityForm
from django.shortcuts import render 
from django.http import HttpResponseRedirect
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
    return render("")