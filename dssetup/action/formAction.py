#coding=utf-8
from dssetup.forms import DomainApplicationFormForm,DomainForm
from django.shortcuts import render 
from django.http import HttpResponseRedirect,HttpResponse
from django.forms.formsets import formset_factory
from dssetup.models import User
from dssetup.decorator import login_required
from dssetup import staticVar
from dssetup.service import formService,adminService
@login_required
def homepage(request):
    user = adminService.getUser(request)
 
    if(user.group.get(groupName = staticVar.APPLICANT)):
        form_list = formService.getFormOfApplicant(user)
        
    
    return render(request,"formlist.html",{
                  "form_list":form_list,                          
                  "role":staticVar.APPLICANT
                })

def createForm(request,formName):
    if(formName == "main"):
        return createDomainForm(request)
    else:
        return createMappingForm(request)

def createDomainForm(request):
        def __getHtmlFromForm(form):
            html=""
            for field in form:
                html += r"<div class='control-group'><label class='control-label'>"\
                          +field.label\
                          +r"</label><div class='controls'>"\
                          +"<input readOnly=true value="+field.data+">"\
                          +r"</div></div>"    
            return html
        
        if(request.POST):
            main_part = DomainApplicationFormForm(request.POST)
            if(main_part.is_valid()):
                formService.addMainForm(request,main_part) 
                request.session["main_part"] = __getHtmlFromForm(main_part)
                if("mapping_part" in request.session):
                    del request.session["mapping_part"]
                return HttpResponseRedirect("create_mapping_part")
            else:
                return render(request,"createform.html",{"form":main_part})
        else:
            main_part = DomainApplicationFormForm()
            return render(request,"createform.html",{"form":main_part})
def createMappingForm(request):
        def __addDomainNameDataToSession():
            sessionMapping = request.session.get("mapping_part") 
            if(sessionMapping):
                for i in range(0,len(sessionMapping)):
                        flag = True
                        mapping = sessionMapping[i]
                    
                        if(mapping.has_key(item[0][0])):
                            mapping[item[0][0]] = item[0][1]
                            sessionMapping[i] = mapping
                            flag=False
                            break
                if(flag):
                        sessionMapping.append({item[0][0]:item[0][1]})
            else:
                    sessionMapping = [{item[0][0]:item[0][1]}]
            request.session["mapping_part"] = sessionMapping
                    
            
        def __addMappingDataToSession():
            sessionMapping = request.session["mapping_part"]
            
            for i in range(0,len(sessionMapping)):
                for key in sessionMapping[i].keys():
                    if(key == request.POST.get("domainName")):
                        mappingDict = sessionMapping[i]
                        cleaned_data = mapping_part.cleaned_data
                        cleaned_data["spName"] = " ".join(cleaned_data["spName"])
                        if(mappingDict.get("mapping")):
                            mappingDict["mapping"].append(cleaned_data)
                        else:
                            mappingDict["mapping"] = [cleaned_data]
                        sessionMapping[i] = mappingDict 
                        break 
            request.session["mapping"] = sessionMapping
        
        if(request.POST):
            mapping_part = DomainForm(request.POST)
            if(mapping_part.is_valid() ):
                __addMappingDataToSession()  
                return render(request,"createmapping.html",{"main_part":request.session["main_part"],"mapping_part":request.session["mapping_part"]})
            else:
                return render(request,"createform.html",{"form":mapping_part,"hidden":request.POST["domainName"]})  
        else:
            item = request.GET.items()
            if(item):
                __addDomainNameDataToSession()
                
                selected=[]
                for mapping in request.session["mapping_part"]:
                    if(item[0][0] in mapping and mapping.has_key("mapping")):
                        for m in mapping.get("mapping"):
                            selected.extend(m.get("spName").split(" "))
                        
                form = DomainForm()
                form.excludeSelected(selected)
                if(form.isAllowedToAdd()):
                    return render(request,"createform.html",{"form":form,"hidden":item[0][0]})
                else:
                    return HttpResponseRedirect("create_mapping_part")      
                    
            else:
                return HttpResponseRedirect("create_mapping_part")
def deleteMappingForm(request,domainName,Id):
    if("mapping_part" in request.session):
        sessionMapping = request.session["mapping_part"]
        for i in range(0,len(sessionMapping)):
             
            if(domainName in sessionMapping[i].keys()):
                del sessionMapping[i]["mapping"][int(Id)]
                break
        request.session["mapping_part"] = sessionMapping
          
    
    return HttpResponseRedirect("/handleForm/create_mapping_part")             
def createMappingPart(request):
    if(request.POST):
        pass
    else:
        if("main_part" in request.session and "mapping_part" in request.session):
            return render(request,"createmapping.html",{"main_part":request.session["main_part"],"mapping_part":request.session["mapping_part"]}) 
        elif("main_part" in request.session):
            return render(request,"createmapping.html",{"main_part":request.session["main_part"]}) 
        else:
            return HttpResponseRedirect("create_main_form")
def checkForm(request,Id):
    
     
    return render(request,"showForm.html",{})
