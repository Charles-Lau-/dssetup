#coding=utf-8
from dssetup.models import DomainApplicationForm,ApplicationFormStatus,DomainForm,Zone,DomainMapping,ServiceProvider
from dssetup import staticVar
from dssetup.service import adminService
import datetime
def getFormOfApplicant(creater):
    return DomainApplicationForm.objects.filter(creater = creater).exclude(status=staticVar.CREATED)

def getFormOfVerifier(verifier):
    return DomainApplicationForm.objects.filter(creater = verifier)

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

def addDomainMappingForm(Id,mapping):
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
    for zone in Zone.objects.all():
        if(domain.domainName.find(zone.zoneName)>=0):
            domain.domain_zone = zone
            break
            
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