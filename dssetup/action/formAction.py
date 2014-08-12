#coding=utf-8
from dssetup.forms import DomainApplicationFormForm,DomainMappingForm,validate_url
from django.shortcuts import render 
from django.http import HttpResponseRedirect 
from dssetup.models import ServiceProvider,DomainApplicationForm
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404 
from django.http import Http404
from dssetup.service import formService,adminService
from copy import copy
from dssetup import staticVar

def showUncheckedForm(request):
    """
             显示待检查申请单列表
     
    """
    return render(request,"formlist.html",{
                  "form_list":formService.getFormOfChecker(),                          
                  "role":"checker"
                })
def showUnimplementedForm(request):
    """
             显示待操作申请单列表
     
    """
    return render(request,"formlist.html",{
                  "form_list":formService.getFormOfOperator(),                          
                  "role":"operator"
                })
def showUnverifiedForm(request):
    """
             显示待审核申请单列表
     
    """
    user = adminService.getUser(request)
    return render(request,"formlist.html",{
                  "form_list":formService.getFormOfVerifier(user),                          
                  "role":"verifier"
                })
def showAppliedForm(request):
    """
             显示已申请单列表
     
    """
    user = adminService.getUser(request)
    return render(request,"formlist.html",{
                  "form_list":formService.getFormOfApplicant(user),                          
                  "role":"applicant"
                })

               
def createDomainForm(request):
    """
            创建申请单的主要信息 如 申请人   产品负责人 所有的信息将会被存入SESSION里面 
     
    """
    def __getHtmlFromForm(form):
            """
            创建 显示申请单主要信息的HTML代码
     
            """
            html=""
            for field in form:
                if(field.data):
                    html += r"<div class='control-group'><label class='control-label'>"\
                          + field.label\
                          + r"</label><div class='controls'>"\
                          + "<input readOnly=true value=" + unicode(field.data) + ">"\
                          + r"</div></div>"    
            return html
        
    if(request.POST):
        main_part = DomainApplicationFormForm(request.POST) 
        if(main_part.is_valid()):
            request.session["Id"] = formService.addMainForm(request,main_part) #将申请表单的主要信息存入数据库 并且返回Id
            request.session["main_part"] = __getHtmlFromForm(main_part)        #记录该申请表单的主要信息的HTML显示 用于显示在页面上面
            request.session["root"] = request.POST["RootDomain"]               #记录该申请表单所操作的主域名 用于后续的操作 
            if("mapping_part" in request.session):
                del request.session["mapping_part"]                            #在创建一个新的申请表单的时候 如果域名映射部分有缓存 则应该删掉                          
            return HttpResponseRedirect("create_mapping_part")
        else:
            return render(request,"createform.html",{"form":main_part})
    else:
        main_part = DomainApplicationFormForm()
        return render(request,"createform.html",{"form":main_part})
            
def createMappingForm(request,domainName=None):
        """
         用于创建申请表单的 域名映射部分 主要填写 IP MODE 和 SP 三个字段数据，而domainName 参数是用来标记 这个映射关系 是属于哪个域名的  

         domainName: 标记 该域名映射部分属于哪个域名
         
        """
        def __addMappingDataToSession():
            """
              将映射信息存入SESSION中

            """
            sessionMapping = request.session["mapping_part"] 
            if(sessionMapping.get(domainName,"")):
                mappingDict = sessionMapping.get(domainName) #获得该域名对应的字典数据 返回的数据格式是{"domainName-x":xxx,"mapping":[{"aim":xx,"mode":xx,"Ip":xxx},....],"error":...}
                cleaned_data = mapping_part.cleaned_data
                cleaned_data_spName = " ".join(cleaned_data["spName"])
                if(not mappingDict.get("mapping","")):
                    mappingDict["mapping"] = []
                      
                  
                print request.POST.get("hidden_value")
                for sp in cleaned_data_spName.split(" "): #由于sp是多选框  但是我们显示的时候 需要一个 SP一行的显示 所以这里是分开他们 为每一个创建一行
                    if(request.POST.get("flag")=="false"):
                        for sp__ in ServiceProvider.objects.filter(spName__icontains=sp):
                            cleaned_data["spName"] = sp__.spName
                            mappingDict["mapping"].append(copy(cleaned_data))
                    else:
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
                selected=[]                                #如果你已经选择了联通 移动，那么返回的表格里面SP字段 就应该排除掉这两个选项 只显示其他剩下的选项给你选择                                           
                mapping = request.session["mapping_part"].get(request.POST.get("domainName"),"")
                if(mapping and mapping.has_key("mapping")):   #selected 里面放的是已经选择了的sp的名字                               
                        for m in mapping.get("mapping"):
                            selected.extend(m.get("spName").split(" "))
                   
        
                mapping_part.excludeSelected(selected) #从form的sp字段 可以选择的值里面排除掉selected数组里面存放的已经被选择了的SP名字
                
                return render(request,"createform.html",{"form":mapping_part,"hidden":request.POST["domainName"]})  
        else:
           
            if(domainName and request.session["mapping_part"].get(domainName,"")): #防止通过URL进行攻击 进行domainName审核
                 
                selected=[]              #如果你已经选择了联通 移动，那么返回的表格里面SP字段 就应该排除掉这两个选项 只显示其他剩下的选项给你选择
                print request.session["mapping_part"]
                mapping = request.session["mapping_part"].get(domainName,"")
                if(mapping and mapping.has_key("mapping")): #selected 里面放的是已经选择了的sp的名字   
                        for m in mapping.get("mapping"):
                            selected.extend(m.get("spName").split(" "))
                
                form = DomainMappingForm()
                form.excludeSelected(selected)  #从form的sp字段 可以选择的值里面排除掉selected数组里面存放的已经被选择了的SP名字
                
                if(form.isAllowedToAdd()):  #如果排除掉已经选择的选项后  还有剩余的选项可选择
                    print form
                    return render(request,"createform.html",{"form":form,"hidden":domainName})
                else:
                    return HttpResponseRedirect("/handleForm/apply_form/create_mapping_part")      
                    
            else:
                return HttpResponseRedirect("/handleForm/apply_form/create_mapping_part")

def storeDomainName(request):
    """
       将域名存入SESSION里面
       
    """
    def __addDomainNameDataToSession():
            """
              将域名存入SESSION里面

              session里面的mapping_part的数据结构是这样的：{"domainName-x"：{"domainName-x":xxxURL,"mapping":[{"ip":xxxx,"mode":xx,"sp":xx},{...}],"error":xxx},"domainName-y":.....}
              
            """
            sessionMapping = request.session.get("mapping_part") 
            if(sessionMapping):
                if(sessionMapping.get(domain_key,"")):    #如果存在这个域名 则跟新它在session里面的值
                    mapping = sessionMapping.get(domain_key)
                    mapping[domain_key] = domain_value
                    sessionMapping[domain_key] = mapping

                else:                                     #如果不存在 就创建一个 并且赋予它domain_value
                    sessionMapping[domain_key] = {domain_key:domain_value}
            else:
                    sessionMapping = {domain_key:{domain_key:domain_value}}
            request.session["mapping_part"] = sessionMapping
     
    def __validateDomain():
        try:
          
            validate_url(domain_value)        #检测 提交的域名是不是合法的域名格式
            if(formService.domainIsOccupied(domain_value)):
                raise ValidationError("This domain is being applied")
        except ValidationError,e:
            mapping = request.session["mapping_part"].get(domain_key)
            mapping["error"] = e.message
            return render(request,"createmapping.html") 
        else:
            mapping = request.session["mapping_part"].get(domain_key) #检测提交的域名是不是重复了  如果是的就返回错误
            for  value  in request.session["mapping_part"].values():
                if(mapping.values()[0] == value.values()[0] and not mapping.keys() == value.keys()):
                    mapping["error"] = "Same URL"
                    return render(request,"createmapping.html") 
                         
            if("error" in mapping):
                del mapping["error"]    #经过两重检测  提交的域名 没有问题 则删除掉 mapping中error字段 返回
         
    if(request.POST):
        for key in request.POST.keys():
            if(key.find("domainName")>=0):
                domain_key = key            #需要被处理的域名的标记 如domainName-1 或者 domainName-2 标记着域名1 和域名2
                domain_value = request.POST.get(key)  #代表需要被处理的域名的值
     
      
        __addDomainNameDataToSession()
        __validateDomain()    
    
    return HttpResponseRedirect("/handleForm/apply_form/create_mapping_part")      

def deleteDomainForm(request,domainName):
    if("mapping_part" in request.session):
        sessionMapping =request.session["mapping_part"]
        if(sessionMapping.get(domainName,"")):
            del sessionMapping[domainName] 
                
        request.session["mapping_part"] = sessionMapping
        
    
    return HttpResponseRedirect("/handleForm/apply_form/create_mapping_part")        
            
def deleteMappingForm(request,domainName,Id):
    """
     删除某个映射关系 如 132.123.123.123  a 联通

     domainName:用来标记被删除的映射关系式属于哪个域名的
     Id:标记该域名下第几个映射关系呗删除
     
    """
    if("mapping_part" in request.session):
        sessionMapping = request.session["mapping_part"]
        if(sessionMapping.get(domainName,"")):
            del sessionMapping.get(domainName)["mapping"][int(Id)]
              
        request.session["mapping_part"] = sessionMapping
          
    
    return HttpResponseRedirect("/handleForm/apply_form/create_mapping_part")             
def createMappingPart(request):
    """
      跳转中转
      
    """
    return render(request,"createmapping.html") 

def editForm(request,Id,step):
    """
               用于编辑表单，只有状态为REJECTED的时候  表单才允许被再次编辑 提交
 
    """
    try:
        step = int(step)
    except ValueError:
        step = 1
        
    if(step==1): 
        if(request.POST):
            form = DomainApplicationFormForm(data=request.POST,instance=get_object_or_404(DomainApplicationForm,id=Id))
            if(form.is_valid()):
                form.save()
                return HttpResponseRedirect("/handleForm/edit_form/"+str(Id)+"/2")
            else:
                return render(request,"editForm.html",{"form":form,"Id":Id})
            
        else:
            form = DomainApplicationFormForm(instance=get_object_or_404(DomainApplicationForm,id=Id))
            form.initial["RootDomain"] = formService.getZoneOfApplicationForm(Id).zoneName
            return render(request,"editForm.html",{"form":form,"Id":Id})
    elif(step==2):
        if(request.POST):
            return render(request,"")
        else:
            if(not "mapping_part" in request.session):
                details = formService.getMappingDetailsForEdit(Id)
                request.session["mapping_part"] = details[1]
                request.session["waiting_for_delete"] = details[0]
            if(not "Id" in request.session):
                request.session["Id"] = Id
            if(not "RootDomain" in request.session):
                request.session["root"] = formService.getZoneOfApplicationForm(Id).zoneName
            return render(request,"editMappingForm.html",{"step":2})
    else:
        raise Http404
  
def addFormIntoDatabase(request):
    """
           将所有的SESSION里面的申请表单域名映射部分的信息 存入数据库里面

    """
    if("waiting_for_delete" in request.session):
        formService.deleteOldMappingForm(request.session["Id"],request.session["waiting_for_delete"])
        del request.session["waiting_for_delete"]
        
    if ("Id" in request.session and "mapping_part" in request.session and request.session.get("mapping_part")):
        for mapping in request.session.get("mapping_part").values():
            if("error" in mapping):
                return HttpResponseRedirect("/handleForm/apply_form/create_mapping_part")
            if(not mapping.get("mapping")):
                return HttpResponseRedirect("/handleForm/apply_form/create_mapping_part")
             
            
        for mapping in request.session.get("mapping_part").values():
            formService.addDomainMappingForm(request.session.get("Id"),mapping,request.session["root"])
        
     
         
        del request.session["mapping_part"]  #一个申请表单成功完成后 一个删除掉其对应的SESSION
        del request.session["Id"]
        
        if("main_part" in request.session):
            del request.session["main_part"]
        if("root" in request.session):
            del request.session["root"]
     
        
        return HttpResponseRedirect("/handleForm/show_applied_form")
    else:
        return HttpResponseRedirect("/handleForm/apply_form/create_mapping_part")  #如果SESSION失效则让他重新填写域名映射信息
def checkForm(request,Id,role=None):
    """
     返回某个表单的详细信息给HTML页面
     
     Id:被查看的表单的ID
     role：是哪一种角色要来查看这个表单 不同的角色 拥有不同的操作权限 如审核 还是关闭
     
    """
    
    main_part,mapping_part = formService.getFormDetails(Id) 
 
    html=""
    for k,v in main_part.items():
       
        html += r"<div class='control-group'><label class='control-label'>"\
                 +k\
                 +r"</label><div class='controls'>"\
                 +"<input readOnly=true value='"+v+"'>"\
                 +r"</div></div>"  
    
    root = formService.getZoneOfApplicationForm(Id).zoneName
                    
    html += r"<div class='control-group'><label class='control-label'>"\
                 +u"主域名"\
                 +r"</label><div class='controls'>"\
                 +"<input readOnly=true value='"+root +"'>"\
                 +r"</div></div>"   
    
     
    if(role=="operator"):
        return render(request,"showForm.html",{"main_part":html,"mapping_part":mapping_part,"role":role,"Id":Id,"root":root,"formattedData":formService.getFormatMappingData(Id)})
    else:
        return render(request,"showForm.html",{"main_part":html,"mapping_part":mapping_part,"role":role,"Id":Id,"root":root})

def changeForm(request):
    """
    用来处理  改变表单状态 这种类型的操作
    
    Id: 被操作的表单的ID
    operation:操作的类型 如 审核  检查
    url: 返回的跳转url
    
    """ 
    if(request.POST):
        print request.POST
        url = formService.changeForm(request,request.POST["Id"],request.POST["operation"])
    else:
        url="/index"
    return HttpResponseRedirect(url)
  
def cancelEdit(request):
    """
        取消表单修改

    """
    if("waiting_for_delete" in request.session):
        del request.session["waiting_for_delete"]
    if("root" in request.session):
        del request.session["root"] 
    if("Id" in request.session):
        del request.session["Id"]
    if("mapping_part" in request.session):
        del request.session["mapping_part"]
        
    return HttpResponseRedirect("/handleForm/show_applied_form")     

def showFormHistory(request,Id):
    """
      展示表单的状态流转历史
 
    """
    return render(request,"show_form_history.html",{"status_list":formService.getStatusListOfForm(Id)})
    
