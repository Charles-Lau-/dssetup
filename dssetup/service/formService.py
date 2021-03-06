 #coding=utf-8
from dssetup.models import DomainApplication,FormStatus,DomainForm,Zone,DomainMapping,ServiceProvider
from dssetup import staticVar
from django.shortcuts import get_object_or_404
from dssetup.service import userService
import datetime
from dssetup.logDecor import logDecor

def getFormOfApplicant(creater):
    """
                       获得申请者身份允许看到的表单列表
                     即是 表单创建者为该creater的表单集合 并且排除掉那些表单状态为created 和 closed的表单

      created是表单创建 但是未进入流程中 被遗弃在数据库中了
      closed是表单被创建人选择关闭了
     
    """
    return DomainApplication.objects.filter(creater = creater).exclude(status=staticVar.CREATED).exclude(status=staticVar.CLOSED).order_by("createTime")

def getFormOfVerifier(verifier):
    """
                          获得审核者可以审核的表单列表
                         逻辑是：查出所有的申请的域名的父域名为该审核者部门管理的表单 并且表单的状态应该是待审核
 
    """
    zones = Zone.objects.filter(zone_dpt=verifier.user_dpt)
    forms = []
    for zone in zones:
        for domain in DomainForm.objects.filter(domain_zone=zone):
            for form in domain.da_domain.all():
                if(form.status==staticVar.WAITINGFORVERIFY and not form in forms): 
                    forms.append(form)
                    
    
    return forms

def getFormOfOperator():
    """
                     获得所有的待操作的表单  
  
    """
    return DomainApplication.objects.filter(status=staticVar.VERIFIED)
def getFormOfChecker():
    """
                       获得所有的待检查的表单  
  
    """
    return DomainApplication.objects.filter(status=staticVar.OPERATED)

@logDecor
def addMainForm(request,main_part):
    """
                   将表单的主要信息存入数据库中    返回存入后的id

     main_part: 是申请表单主要信息的form
    
    """
    main = main_part.save(commit=False)
    main.creater = userService.getUser(request)
    main.createTime = datetime.datetime.now()
    main.status = staticVar.CREATED
    main.save()

    #创建一条标记表单状态流转的记录
    status = FormStatus(status=staticVar.CREATED)
    status.status_user = userService.getUser(request)
    status.status_da = main
    status.createTime = datetime.datetime.now()
    status.save()
    
    return main.id

def addDomainMappingForm(Id,mapping,root):
    """
                    将申请单 域名映射部分存入数据库

      Id: 该域名映射对应的申请单ID
      mapping：域名映射数据
      root:域名映射对应的父域名
      
    """
  
    main = get_object_or_404(DomainApplication,id=Id)
    main.status = staticVar.WAITINGFORVERIFY
    main.save()

    #创建一条标记表单状态流转的记录
    status = FormStatus(status=staticVar.WAITINGFORVERIFY)
    status.status_user = main.creater
    status.status_da = main
    status.createTime = datetime.datetime.now()
    status.save()
    
    domainName = mapping.values()[0]
    try:                                                       #如果域名存在 则查出来 没有就创建一条新的  这里创建的是  Type=1的域名
        domain1 = DomainForm.objects.get(domainName=domainName,domainType=1)
        
    except DomainForm.DoesNotExist:
        domain1 = DomainForm(domainName=domainName,domainType=1)
    
    domain1.domain_zone = Zone.objects.get(zoneName=root)
    domain1.status = staticVar.CANNOT_APPLY
    domain1.save()
    
    domain = DomainForm(domainName=domainName,domainType=0)
    domain.domain_zone =  Zone.objects.get(zoneName=root)
    domain.status = staticVar.CANNOT_APPLY        
    domain.save()
    domain.da_domain.add(main)
    domain.save()
    
    mappingData = mapping.values()[1]                      #将ip mode sp 这样的映射关系存入数据库
    for m in mappingData:
        domainMapping = DomainMapping(mode=m.get("mode"),aim= m.get("aim"))
        domainMapping.dm_domain = domain
        domainMapping.dm_sp = ServiceProvider.objects.get(spName=m.get("spName"))
        domainMapping.save()
   
          
def getFormDetails(Id):
    """
                 返回申请表单详细信息

     Id:申请表单Id
     mapping_part: 采取以下格式  {"domainName":xx,mapping:[{"ip":xx,"mode":xx,"aim":xx},....]} 
    """
    domainApplicationForm = get_object_or_404(DomainApplication,id=Id)
    mapping_part=[]
    for domain in DomainForm.objects.filter(da_domain=domainApplicationForm):   #构建一个类似于 session["mapping_part"] 的数据结构的表单数据 并且返回
        domainMapping ={}
        domainMapping["domainName"] = domain.domainName
        domainMapping["mapping"] = []
        for mapping in DomainMapping.objects.filter(dm_domain=domain):
            domainMapping["mapping"].append({"aim":mapping.aim,"mode":mapping.mode,"sp":mapping.dm_sp.spName})
        mapping_part.append(domainMapping)
    
    main_part = domainApplicationForm.get_values()
    if(domainApplicationForm.effectTime):
        
        main_part[u"截止时间"] = str(domainApplicationForm.effectTime)
    
      
    return (main_part,mapping_part)   #第一个是表单的主要信息，第二个是表单的映射信息

@logDecor 
def changeForm(request,Id,operation):
    """
                          改变表单的状态
 
      Id：表单的Id
      Operation：对该表单进行的操作 如 审核 检查       如何要修改operation的名字  除了修改这里之外    还要修改  show_form.html 里面对应的名字

                     返回一个Url用来指引action部分的跳转
      
    """
    def __createStatusRecord():
        """
                                创建表单状态流转记录 由于每一次改变表单状态都需要创建这么一条记录 所以 写成函数会方便很多
    
        """
        user = userService.getUser(request)
        
        status = FormStatus(status=form.status)
        status.status_user = user
        status.status_da = form
        status.createTime = datetime.datetime.now()
        if(request.POST and request.POST.get("comment")):
            status.statusDes = request.POST.get("comment")
            
        status.save()
 
   
    root = "/handleForm/"    
    form = get_object_or_404(DomainApplication,id=Id)
    if(operation=="verify"):
        form.status = staticVar.VERIFIED
        url = root + "show_unverified_form"
    elif(operation=="reject"):
        if(form.status==staticVar.WAITINGFORVERIFY):
            form.status = staticVar.REJECTED
            url =  root + "show_unverified_form"
        elif(form.status==staticVar.VERIFIED):
            form.status = staticVar.REJECTED
            url = root + "show_unimplemented_form"
        elif(form.status==staticVar.OPERATED):
            form.status = staticVar.VERIFIED
            url = root + "show_unchecked_form"
    elif(operation=="close"):
        form.status = staticVar.CLOSED
        #改变表单对应的DOMAIN的状态  在表单完被关闭后   该表弟那对应的域名 都应该设置为 可以被申请
        for domain in DomainForm.objects.filter(da_domain=form):
                domain.status = staticVar.CAN_APPLY
                domain1 = DomainForm.objects.get(domainName=domain.domainName,domainType=1)
                domain1.status = staticVar.CAN_APPLY
                domain1.save()
                domain.save()
        url = root + "show_applied_form"
    elif(operation=="edit"):
        if(form.status==staticVar.REJECTED):
            url  = root +"edit_form/"+str(Id)
        else:
            url = "/index"
        return url
    elif(operation=="operate"):
        form.status = staticVar.OPERATED
        url=root + "show_unimplemented_form" 
    elif(operation=="check"):
        form.status = staticVar.CHECKED
        url = root + "show_unchecked_form"
    elif(operation=="confirm"):
       
        if(form.status==staticVar.CHECKED):
            form.status = staticVar.COMPLETED
            #改变表单对应的DOMAIN的状态  在表单完成流程后  该表弟那对应的域名 都应该设置为 可以被申请
            for domain in DomainForm.objects.filter(da_domain=form): 
                domain.status = staticVar.CAN_APPLY
                domain.save()
                
                domain1 = DomainForm.objects.get(domainName=domain.domainName,domainType=1)
                domain1.status = staticVar.CAN_APPLY
                domain1.save() 
                #如果该域名有绑定的映射  就删除掉映射 然后  再绑定新的 如果没有  就直接创建新的域名绑定
                #这个部分是服务于  发现数据库设计bug后的修复
                if(DomainMapping.objects.filter(dm_domain=domain1)):
                    for m in DomainMapping.objects.filter(dm_domain=domain1):
                        m.delete()
                for m in DomainMapping.objects.filter(dm_domain=domain):
                    domainMapping = DomainMapping(mode=m.mode,aim= m.aim)
                    domainMapping.dm_domain = domain1
                    domainMapping.dm_sp = m.dm_sp
                    domainMapping.save() 
                    
               
                
            
            url = root + "show_applied_form"
        else:
            url = "/index"
    else:
        return "/index"
    
    __createStatusRecord()
    form.save()
    return url



def getMappingDetailsForEdit(Id):
    """
                    返回申请表单映射关系详细信息
                  用于表单再编辑 
     
     Id:申请表单Id
  
    """
    domainApplicationForm = get_object_or_404(DomainApplication,id=Id)
    mapping_part={}
    waiting_for_delete={"domain":[],"mapping":[]}
    i = 0
    #构建一个类似于 session["mapping_part"] 的数据结构的表单数据 并且返回
    for domain in DomainForm.objects.filter(da_domain=domainApplicationForm):  
        waiting_for_delete["domain"].append(domain.id)
        domainMapping ={}
        domainMapping["domainName-"+str(i)] = domain.domainName
        domainMapping["mapping"] = []
        for mapping in DomainMapping.objects.filter(dm_domain=domain):
            domainMapping["mapping"].append({"aim":mapping.aim,"mode":mapping.mode,"spName":mapping.dm_sp.spName})
            waiting_for_delete["mapping"].append(mapping.id)
        mapping_part["domainName-"+str(i)] = domainMapping
        i +=1
     
    return (waiting_for_delete,mapping_part)   #表单的映射信息        

@logDecor
def deleteOldMappingForm(Id,Ids):
    """
                 我们编辑的思路是把编辑之前的旧内容删除掉  新的 插入数据库  这个函数用来删除插入新数据后 把  原来的给删除掉
    
    """
    
    for i in Ids["mapping"]:    
        get_object_or_404(DomainMapping,id=i).delete()
    for i in Ids["domain"]:
        domain = get_object_or_404(DomainForm,id=i)
        domain1 = get_object_or_404(DomainForm,domainType=1,domainName=domain.domainName)
        domain1.status = staticVar.CAN_APPLY
        domain.delete()
       
def getFormatMappingData(Id):
    """
                 经过讨论，需要给操作人员提供更好的数据格式  这个韩式用来处理这个的    可以返回要求中的   申请表单域名映射数据
    
    """
    domainApplicationForm = get_object_or_404(DomainApplication,id=Id)
    formattedData=[]
    for domain in DomainForm.objects.filter(da_domain=domainApplicationForm):
        mappingData={}
        mappingData["domainName"] = domain.domainName
        mappingData["mapping"] = []
        for mapping in DomainMapping.objects.filter(dm_domain=domain):
            mappingData["mapping"].append(mapping.get_values())
        
        #验证 是否 所有的view都映射到一个ip 或域名
        tempt=[]
        for mapping in mappingData["mapping"]:
            if(not mapping["aim"] in tempt ):
                tempt.append(mapping["aim"])
        
        if(len(tempt)==1 and len(mappingData["mapping"])==len(ServiceProvider.objects.all())):
            if(domainApplicationForm.operCategory == u"删除"):
                mappingData["mapping"] = [{"dm_sp":"ad","mode":mappingData["mapping"][0]["mode"],"aim":tempt[-1]}] #如果所有的view都映射到同一个域名 则进行替换
            else:
                mappingData["mapping"] = [{"dm_sp":"a","mode":mappingData["mapping"][0]["mode"],"aim":tempt[-1]}] #如果所有的view都映射到同一个域名 则进行替换
        
        
        
        formattedData.append(mappingData)
        
 
    data=""
    root = domainApplicationForm.getZoneOfApplicationForm().zoneName
    for domainMapping in formattedData:
        if(domainApplicationForm.operCategory == u"删除" and not domainMapping["mapping"][0]["dm_sp"] == "ad"):
            continue
        data += domainMapping["domainName"]+"."+root+".\n"
        for mapping in domainMapping["mapping"]:
                data += mapping["dm_sp"]+"\n"
                if(mapping["mode"]=="cname"):
                    for a in mapping["aim"].split(" "):
                        data += a+". "
                    data += "\n"
                else:
                    data += mapping["aim"]+"\n"
    return data