#coding=utf-8
from dssetup.models import DomainApplicationForm,ApplicationFormStatus,DomainForm,Zone,DomainMapping,ServiceProvider
from dssetup import staticVar
from dssetup.service import adminService
import datetime

def getFormOfApplicant(creater):
    """
      获得申请者身份允许看到的表单列表
      即是 表单创建者为该creater的表单集合 并且排除掉那些表单状态为created 和 closed的表单

      created是表单创建 但是未进入流程中 被遗弃在数据库中了
      closed是表单被创建人选择关闭了
     
    """
    return DomainApplicationForm.objects.filter(creater = creater).exclude(status=staticVar.CREATED).exclude(status=staticVar.CLOSED).order_by("createTime")

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
    return DomainApplicationForm.objects.filter(status=staticVar.VERIFIED)
def getFormOfChecker():
    """
     获得所有的待检查的表单  
  
    """
    return DomainApplicationForm.objects.filter(status=staticVar.OPERATED)

def addMainForm(request,main_part):
    """
     将表单的主要信息存入数据库中

     main_part: 是申请表单主要信息的form
    
    """
    main = main_part.save(commit=False)
    main.creater = adminService.getUser(request)
    main.createTime = datetime.datetime.now()
    main.status = staticVar.CREATED
    main.save()

    #创建一条标记表单状态流转的记录
    status = ApplicationFormStatus(status=staticVar.CREATED)
    status.status_user = adminService.getUser(request)
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
    main = DomainApplicationForm.objects.get(id=Id)
    main.status = staticVar.WAITINGFORVERIFY
    main.save()

    #创建一条标记表单状态流转的记录
    status = ApplicationFormStatus(status=staticVar.WAITINGFORVERIFY)
    status.status_user = main.creater
    status.status_da = main
    status.createTime = datetime.datetime.now()
    status.save()
    
    domainName = mapping.values()[0]
    try:                                                      #如果域名存在 则查出来 没有就创建一条新的
        domain = DomainForm.objects.get(domainName=domainName)
    except DomainForm.DoesNotExist:
        domain = DomainForm(domainName=domainName)
         
    domain.status = staticVar.CANNOT_APPLY                    #正在申请中的域名是不能再被申请了的 
    domain.domain_zone =  Zone.objects.get(zoneName=root)
            
    domain.save()
    domain.da_domain.add(main)
    domain.save()
    
    mappingData = mapping.values()[1]                      #将ip mode sp 这样的映射关系存入数据库
    for m in mappingData:
        for ip_ in m.get("aim").split(","):
            domainMapping = DomainMapping(mode=m.get("mode"),aim=ip_)
            domainMapping.dm_domain = domain
            domainMapping.dm_sp = ServiceProvider.objects.get(spName=m.get("spName"))
            domainMapping.save()

def getFormDetails(Id):
    """
     返回申请表单详细信息

     Id:申请表单Id
  
    """
    domainApplicationForm = DomainApplicationForm.objects.get(id=Id)
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


def changeForm(request,Id,operation):
    """
      改变表单的状态

      Id：表单的Id
      Operation：对该表单进行的操作 如 审核 检查

      返回一个Url用来指引action部分的跳转
      
    """
    def __createStatusRecord(status):
        """
          创建表单状态流转记录 由于每一次改变表单状态都需要创建这么一条记录 所以 写成函数会方便很多

        """
        user = adminService.getUser(request)
        
        status = ApplicationFormStatus(status=status)
        status.status_user = user
        status.status_da = form
        status.createTime = datetime.datetime.now()
        status.save()
 
    root = "/handleForm/"    
    form = DomainApplicationForm.objects.get(id=Id)
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
        url = root + "show_applied_form"
    elif(operation=="edit"):
        if(form.status==staticVar.REJECTED):
            url  = root +"edit_form/"+str(Id)
        else:
            url = "/index"
    elif(operation=="operate"):
        form.status = staticVar.OPERATED
        url=root + "show_unimplemented_form" 
    elif(operation=="check"):
        form.status = staticVar.CHECKED
        url = root + "show_unchecked_form"
    elif(operation=="confirm"):
       
        if(form.status==staticVar.CHECKED):
            form.status = staticVar.COMPLETED
            url = root + "show_applied_form"
        else:
            url = "/index"
    __createStatusRecord(form.status)
    form.save()
    return url
    
