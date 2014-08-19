#coding=utf-8
from dssetup.models import DomainApplication,DomainForm,DomainMapping
from dssetup.forms import DomainFormForm
from django.shortcuts import get_object_or_404
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
     
     form: 是域名的自己的一些信息 如 域名名字 域名状态
     domainMapping: 是域名对应的一些映射关系  ip sp mode的一个list字典
    """
   
    domain = get_object_or_404(DomainForm,id=Id)
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