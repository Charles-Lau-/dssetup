#coding=utf-8
from dssetup.models import DomainApplicationForm,ApplicationFormStatus,DomainForm,Zone,DomainMapping,ServiceProvider
from dssetup.service import adminService
import datetime
def getFormOfApplicant(creater):
    return DomainApplicationForm.objects.filter(creater = creater)
def addDomainApplicationForm(request,mainFormset,mappingFormset):
    mainform = mainFormset[0]
    main = mainform.save(commit=False)
    main.creater = adminService.getUser(request)
    main.createTime = datetime.datetime.now()
    main.save()
        
    status = ApplicationFormStatus(status="created")
    status.status_user = adminService.getUser(request)
    status.status_da = main
    status.createTime = datetime.datetime.now()
    status.save()
    
    for mappingform in mappingFormset:
        try:
            domain = DomainForm.objects.get(domainName=mappingform.cleaned_data["domainName"])
        except DomainForm.DoesNotExist:
            domain = DomainForm(domainName=mappingform.cleaned_data["domainName"])
        
        domain.status = "occupied"
        for zone in Zone.objects.all():
            if(domain.domainName.find(zone.zoneName)>=0):
                domain.domain_zone = zone
                break
            
        domain.save()
        domain.da_domain.add(main)
        domain.save()
        
        for i in range(1,5):
            mapping = DomainMapping(mode=mappingform.cleaned_data["mode"+str(i)],aim=mappingform.cleaned_data["aim"+str(i)])
            mapping.dm_domain = domain
            mapping.dm_sp = ServiceProvider.objects.get(id=mappingform.cleaned_data["spName"+str(i)])
            mapping.save()

def getDomainApplicationForm(Id):
    applicationForm  = DomainApplicationForm.objects.get(id=Id)       
    domains = applicationForm.domainform_set.all()
    domainMappings=[] 
    for domain in domains:
        domainMapping={"domainName":domain.domainName}
        mappings = domain.domainmapping_set.all() 
        i=1
        for mapping in mappings:
            domainMapping["mode"+str(i)]=mapping.mode
            domainMapping["aim"+str(i)]=mapping.aim
            domainMapping["spName"+str(i)]=mapping.dm_sp.spName
            i+=1
      
        domainMappings.append(domainMapping)
        
        