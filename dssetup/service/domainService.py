#coding=utf-8
from dssetup.models import DomainApplication,DomainForm,DomainMapping
from dssetup.forms import DomainFormForm
from dssetup import staticVar

def getDomainStatistics(year):
    """ 
              统计出 year年份的每个月的申请域名的数目
    
    """
    counter = []
    for i in range(1,13):
        num=0
        if(i>9):
           
            for form in DomainApplication.objects.filter(createTime__contains=str(year)+"-"+str(i)):
                num += len(DomainForm.objects.filter(da_domain=form))
            
        else:
            for form in DomainApplication.objects.filter(createTime__contains=str(year)+"-0"+str(i)):
                num += len(DomainForm.objects.filter(da_domain=form))
        counter.append(num)
            
    return counter

def showDetailOfDomain(Id):
    """
              这个函数是为了后台的  显示域名的详细绑定信息而使用的 
    
    """
    domain = DomainForm.objects.get(id=Id)
    form = DomainFormForm(instance=domain)
    domainMapping=[]
    for mapping in DomainMapping.objects.filter(dm_domain=domain):
        domainMapping.append(mapping.get_values())
    return (form,domainMapping)

        
def domainIsOccupied(domainName):
    """
                        看某个域名能否被申请
    
    """
    try:                                          
        domain = DomainForm.objects.get(domainName=domainName,domainType=1)
        if(domain.status == staticVar.CANNOT_APPLY):
            return True
        else:
            return False
    except DomainForm.DoesNotExist:
        return False