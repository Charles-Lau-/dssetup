#coding=utf-8
from dssetup.models import DomainApplicationForm,ApplicationFormStatus,DomainForm,Zone,DomainMapping,ServiceProvider
from dssetup.service import adminService
import datetime
def getFormOfApplicant(creater):
    return DomainApplicationForm.objects.filter(creater = creater)

def addMainForm(request,main_part):
    main = main_part.save(commit=False)
    main.creater = adminService.getUser(request)
    main.createTime = datetime.datetime.now()
    main.status = "created"
    main.save()
    
    status = ApplicationFormStatus(status="created")
    status.status_user = adminService.getUser(request)
    status.status_da = main
    status.createTime = datetime.datetime.now()
    status.save()
    
    return main.id

def addDomainApplicationForm(request,mainFormset,mappingFormset):
    mainform = mainFormset[0]
    main = mainform.save(commit=False)
    main.creater = adminService.getUser(request)
    main.createTime = datetime.datetime.now()
    main.status = "created"
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
    main_partData={"main_part-TOTAL_FORMS":"1","main_part-INITIAL_FORMS":"0","main_part-MAX_NUM_FORMS":"1000"}
    for k,v in applicationForm.get_values().items():
        main_partData["main_part-0-"+k] = v
    main_partData["main_part-0-da_applicant"] = applicationForm.da_applicant
    main_partData["main_part-0-da_dpt"] = applicationForm.da_dpt
    main_partData["main_part-0-mailList"] = applicationForm.mailList
    main_partData["main_part-0-daDes"] = applicationForm.daDes
    main_partData["main_part-0-status"] = applicationForm.status 
     
    
    mapping_partData={}
    j=0; 
    for domain in domains:
        mapping_partData["mapping_part-"+str(j)+"-domainName"] = domain.domainName
        mappings = DomainMapping.objects.filter(dm_domain =domain)
        i=1
        for mapping in mappings:
            mapping_partData["mapping_part-"+str(j)+"-mode"+str(i)]=mapping.mode
            mapping_partData["mapping_part-"+str(j)+"-aim"+str(i)]=mapping.aim
            mapping_partData["mapping_part-"+str(j)+"-spName"+str(i)]=mapping.dm_sp.spName
            i+=1
        j+=1
    mapping_partData["mapping_part-TOTAL_FORMS"] = str(j)
    mapping_partData["mapping_part-INITIAL_FORMS"] = "0"
    mapping_partData["mapping_part-MAX_NUM_FORMS"] = ""
    
    print mapping_partData
    return (main_partData,mapping_partData)