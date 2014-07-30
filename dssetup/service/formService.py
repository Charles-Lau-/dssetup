#coding=utf-8
from dssetup.models import DomainApplicationForm,ApplicationFormStatus,DomainForm,Zone,DomainMapping,ServiceProvider
from dssetup import staticVar
from dssetup.service import adminService
import datetime
def getFormOfApplicant(creater):
    return DomainApplicationForm.objects.filter(creater = creater).exclude(status=staticVar.CREATED).exclude(status=staticVar.CLOSED)

def getFormOfVerifier(verifier):
    zones = Zone.objects.filter(zone_dpt=verifier.user_dpt)
    forms = []
    for zone in zones:
        for domain in DomainForm.objects.filter(domain_zone=zone):
            for form in domain.da_domain.all():
                if(form.status==staticVar.WAITINGFORVERIFY and not form in forms):
                    forms.append(form)
                    
    
    return forms

def getFormOfOperator():
    return DomainApplicationForm.objects.filter(status=staticVar.VERIFIED)
def getFormOfChecker():
    return DomainApplicationForm.objects.filter(status=staticVar.OPERATED)

def addMainForm(request,main_part):
    main = main_part.save(commit=False)
    main.creater = adminService.getUser(request)
    main.createTime = datetime.datetime.now()
    main.status = staticVar.CREATED
    main.save()
    
    status = ApplicationFormStatus(status=staticVar.CREATED)
    status.status_user = adminService.getUser(request)
    status.status_da = main
    status.createTime = datetime.datetime.now()
    status.save()
    
    return main.id

def addDomainMappingForm(Id,mapping,root):
    main = DomainApplicationForm.objects.get(id=Id)
    main.status = staticVar.WAITINGFORVERIFY
    main.save()
    
    status = ApplicationFormStatus(status=staticVar.WAITINGFORVERIFY)
    status.status_user = main.creater
    status.status_da = main
    status.createTime = datetime.datetime.now()
    status.save()
    
    domainName = mapping.values()[0]
    try:
        domain = DomainForm.objects.get(domainName=domainName)
    except DomainForm.DoesNotExist:
        domain = DomainForm(domainName=domainName)
        
    domain.status = staticVar.CANNOT_APPLY
    print root
    domain.domain_zone =  Zone.objects.get(zoneName=root)
            
    domain.save()
    domain.da_domain.add(main)
    domain.save()
    
    mappingData = mapping.values()[1]
    for m in mappingData:
        for ip_ in m.get("aim").split(","):
            domainMapping = DomainMapping(mode=m.get("mode"),aim=ip_)
            domainMapping.dm_domain = domain
            domainMapping.dm_sp = ServiceProvider.objects.get(spName=m.get("spName"))
            domainMapping.save()

def getFormDetails(Id):
    domainApplicationForm = DomainApplicationForm.objects.get(id=Id)
    mapping_part=[]
    for domain in DomainForm.objects.filter(da_domain=domainApplicationForm):
        domainMapping ={}
        domainMapping["domainName"] = domain.domainName
        domainMapping["mapping"] = []
        for mapping in DomainMapping.objects.filter(dm_domain=domain):
            domainMapping["mapping"].append({"aim":mapping.aim,"mode":mapping.mode,"sp":mapping.dm_sp.spName})
        mapping_part.append(domainMapping)
    return (domainApplicationForm.get_values(),mapping_part) 


def changeForm(request,Id,operation):
    def __createStatusRecord(status):
        user = adminService.getUser(request)
        
        status = ApplicationFormStatus(status=status)
        status.status_user = user
        status.status_da = form
        status.createTime = datetime.datetime.now()
        status.save()
    
        
    form = DomainApplicationForm.objects.get(id=Id)
    if(operation=="verify"):
        form.status = staticVar.VERIFIED
        url = "/handleForm/show_unverified_form"
    elif(operation=="reject"):
        if(form.status==staticVar.WAITINGFORVERIFY):
            form.status = staticVar.REJECTED
            url =  "/handleForm/show_unverified_form"
        elif(form.status==staticVar.VERIFIED):
            form.status = staticVar.REJECTED
            url =  "/handleForm/show_unimplemented_form"
        elif(form.status==staticVar.OPERATED):
            form.status = staticVar.VERIFIED
            url = "handleForm/show_unchecked_form"
    elif(operation=="close"):
        form.status = staticVar.CLOSED
        url = "/handleForm/show_applied_form"
    elif(operation=="edit"):
        if(form.status==staticVar.REJECTED):
            pass
        else:
            pass
    elif(operation=="operate"):
        form.status = staticVar.OPERATED
        url="/handleForm/show_unimplemented_form" 
    elif(operation=="check"):
        form.status = staticVar.CONFIRMED
        url="/handleForm/show_unchecked_form" 
    __createStatusRecord(form.status)
    form.save()
    return url
    