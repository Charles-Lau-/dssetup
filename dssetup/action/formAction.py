#coding=utf-8
from dssetup.forms import DomainApplicationFormForm,DomainMappingForm
from django.shortcuts import render 
from django.http import HttpResponseRedirect 
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from dssetup import staticVar
from dssetup.service import formService,adminService
from copy import copy
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
            request.session["Id"] = formService.addMainForm(request,main_part) 
            request.session["main_part"] = __getHtmlFromForm(main_part)
            request.session["root"] = request.POST["RootDomain"]    
            if("mapping_part" in request.session):
                del request.session["mapping_part"]
            return HttpResponseRedirect("create_mapping_part")
        else:
            return render(request,"createform.html",{"form":main_part})
    else:
        main_part = DomainApplicationFormForm()
        return render(request,"createform.html",{"form":main_part})\
            
def createMappingForm(request):
        def __addDomainNameDataToSession():
            sessionMapping = request.session.get("mapping_part") 
            if(sessionMapping):
                if(sessionMapping.get(domain_key,"")):
                    mapping = sessionMapping.get(domain_key)
                    mapping[domain_key] = domain_value
                    sessionMapping[domain_key] = mapping

                else:
                    sessionMapping[domain_key] = {domain_key:domain_value}
            else:
                    sessionMapping = {domain_key:{domain_key:domain_value}}
            request.session["mapping_part"] = sessionMapping
                    
            
        def __addMappingDataToSession():
            sessionMapping = request.session["mapping_part"]
            domainName = request.POST.get("domainName") 
            if(sessionMapping.get(domainName,"")):
                mappingDict = sessionMapping.get(domainName)
                cleaned_data = mapping_part.cleaned_data
                cleaned_data_spName = " ".join(cleaned_data["spName"])
                if(not mappingDict.get("mapping")):
                    mappingDict["mapping"] = []
                      
                   
                for sp in cleaned_data_spName.split(" "):
                    cleaned_data["spName"] = sp
                    mappingDict["mapping"].append(copy(cleaned_data))
                                
            sessionMapping[domainName] = mappingDict 
                         
            request.session["mapping"] = sessionMapping
        
        if(request.POST):
            mapping_part = DomainMappingForm(request.POST)
            if(mapping_part.is_valid() ):
                __addMappingDataToSession()  
                return render(request,"createmapping.html",{"main_part":request.session["main_part"],"mapping_part":request.session["mapping_part"].values()})
            else:
               
                
                return render(request,"createform.html",{"form":mapping_part,"hidden":request.POST["domainName"]})  
        else:
            item = request.GET.items()
            if(item):
                domain_key = item[0][0]
                domain_value = item[0][1]
                try:
                    URLValidator(item[0][1])
                except ValidationError:
                    return render(request,"createmapping.html",{"main_part":request.session["main_part"],"mapping_part":request.session["mapping_part"],"error":"Invalid URl"}) 
                
                __addDomainNameDataToSession()
                
                selected=[]
                mapping = request.session["mapping_part"].get(domain_key,"")
                if(mapping and mapping.has_key("mapping")):
                        for m in mapping.get("mapping"):
                            selected.extend(m.get("spName").split(" "))
                        
                form = DomainMappingForm()
                form.excludeSelected(selected)
                if(form.isAllowedToAdd()):
                    return render(request,"createform.html",{"form":form,"hidden":domain_key})
                else:
                    return HttpResponseRedirect("create_mapping_part")      
                    
            else:
                return HttpResponseRedirect("create_mapping_part")
def deleteMappingForm(request,domainName,Id):
    if("mapping_part" in request.session):
        sessionMapping = request.session["mapping_part"]
        if(sessionMapping.get(domainName,"")):
            del sessionMapping.get(domainName)["mapping"][int(Id)]
              
        request.session["mapping_part"] = sessionMapping
          
    
    return HttpResponseRedirect("/handleForm/create_mapping_part")             
def createMappingPart(request):
    if(request.POST):
        pass
    else:
        if("main_part" in request.session and "mapping_part" in request.session):
            return render(request,"createmapping.html",{"main_part":request.session["main_part"],"mapping_part":request.session["mapping_part"].values()}) 
        elif("main_part" in request.session):
            return render(request,"createmapping.html",{"main_part":request.session["main_part"]}) 
        else:
            return HttpResponseRedirect("create_main_form")
def addFormIntoDatabase(request):
    if ("Id" in request.session and "mapping_part" in request.session):
        for mapping in request.session.get("mapping_part").values():
            formService.addDomainMappingForm(request.session.get("Id"),mapping,request.session["root"])
        
        del request.session["mapping_part"]
        del request.session["Id"]
        del request.session["main_part"]
        del request.session["root"]
        
        return  homepage(request)
    else:
        return HttpResponseRedirect("create_mapping_part")
def checkForm(request,Id):
    
    
    formDetails = formService.getFormDetails(Id) 
    
    html=""
    for k,v in formDetails[0].items():
        html += r"<div class='control-group'><label class='control-label'>"\
                 +k\
                 +r"</label><div class='controls'>"\
                 +"<input readOnly=true value="+v+">"\
                 +r"</div></div>"     
                 
    return render(request,"showForm.html",{"main_part":html,"mapping_part":formDetails[1]})

