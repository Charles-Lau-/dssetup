#coding=utf-8
from dssetup.forms import DomainApplicationFormForm,DomainMappingForm
from django.shortcuts import render 
from django.http import HttpResponseRedirect 
from dssetup.forms import validate_url
from django.core.exceptions import ValidationError
from dssetup import staticVar
from dssetup.service import formService,adminService
from copy import copy

def showUncheckedForm(request):
    return render(request,"formlist.html",{
                  "form_list":formService.getFormOfChecker(),                          
                  "role":"checker"
                })
def showUnimplementedForm(request):
    return render(request,"formlist.html",{
                  "form_list":formService.getFormOfOperator(),                          
                  "role":"operator"
                })
def showUnverifiedForm(request):
    user = adminService.getUser(request)
    return render(request,"formlist.html",{
                  "form_list":formService.getFormOfVerifier(user),                          
                  "role":"verifier"
                })
def showAppliedForm(request):
    user = adminService.getUser(request)
    return render(request,"formlist.html",{
                  "form_list":formService.getFormOfApplicant(user),                          
                  "role":"applicant"
                })

               
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
            
def createMappingForm(request,domainName=None):
       
                    
            
        def __addMappingDataToSession():
            sessionMapping = request.session["mapping_part"]
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
                return render(request,"createmapping.html")
            else:
                selected=[]
                mapping = request.session["mapping_part"].get(request.POST.get("domainName"),"")
                if(mapping and mapping.has_key("mapping")):
                        for m in mapping.get("mapping"):
                            selected.extend(m.get("spName").split(" "))
                   
        
                mapping_part.excludeSelected(selected)
                
                return render(request,"createform.html",{"form":mapping_part,"hidden":request.POST["domainName"]})  
        else:
           
            if(domainName and request.session["mapping_part"].get(domainName,"")):
                 
                selected=[]
                mapping = request.session["mapping_part"].get(domainName,"")
                if(mapping and mapping.has_key("mapping")):
                        for m in mapping.get("mapping"):
                            selected.extend(m.get("spName").split(" "))
                
                form = DomainMappingForm()
                form.excludeSelected(selected)
                
                if(form.isAllowedToAdd()):
                    return render(request,"createform.html",{"form":form,"hidden":domainName})
                else:
                    return HttpResponseRedirect("/handleForm/apply_form/create_mapping_part")      
                    
            else:
                return HttpResponseRedirect("/handleForm/apply_form/create_mapping_part")

def storeDomainName(request):
    """
    """
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
     
    if(request.POST):
        for key in request.POST.keys():
            if(key.find("domainName")>=0):
                domain_key = key
                domain_value = request.POST.get(key)
                flag=True
       
        if(flag):
      
            __addDomainNameDataToSession()
                
            try:
                validate_url(domain_value)
            except ValidationError:
                mapping = request.session["mapping_part"].get(domain_key)
                
                mapping["error"] = "Invalid URL"
                return render(request,"createmapping.html") 
            else:
                mapping = request.session["mapping_part"].get(domain_key)
                for  value  in request.session["mapping_part"].values():
                    if(mapping.values()[0] == value.values()[0] and not mapping.keys() == value.keys()):
                        mapping["error"] = "Same URL"
                        return render(request,"createmapping.html") 
                         
                if("error" in mapping):
                    del mapping["error"]   
                     
    return HttpResponseRedirect("/handleForm/apply_form/create_mapping_part")      
                    
def deleteMappingForm(request,domainName,Id):
    if("mapping_part" in request.session):
        sessionMapping = request.session["mapping_part"]
        if(sessionMapping.get(domainName,"")):
            del sessionMapping.get(domainName)["mapping"][int(Id)]
              
        request.session["mapping_part"] = sessionMapping
          
    
    return HttpResponseRedirect("/handleForm/apply_form/create_mapping_part")             
def createMappingPart(request):
    return render(request,"createmapping.html") 
       
def addFormIntoDatabase(request):
    if ("Id" in request.session and "mapping_part" in request.session):
        for mapping in request.session.get("mapping_part").values():
            formService.addDomainMappingForm(request.session.get("Id"),mapping,request.session["root"])
        
        del request.session["mapping_part"]
        del request.session["Id"]
        del request.session["main_part"]
        del request.session["root"]
        
        return HttpResponseRedirect("/handleForm")
    else:
        return HttpResponseRedirect("create_mapping_part")
def checkForm(request,Id,role=None):
    
    
    formDetails = formService.getFormDetails(Id) 
    
    html=""
    for k,v in formDetails[0].items():
        html += r"<div class='control-group'><label class='control-label'>"\
                 +k\
                 +r"</label><div class='controls'>"\
                 +"<input readOnly=true value="+v+">"\
                 +r"</div></div>"     
                  
    return render(request,"showForm.html",{"main_part":html,"mapping_part":formDetails[1],"role":role,"Id":Id})

def changeForm(request,Id,operation):
    url = formService.changeForm(request,Id,operation)
    return HttpResponseRedirect(url)
  
        