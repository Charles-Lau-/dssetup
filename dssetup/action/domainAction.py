#coding=utf-8 
from django.shortcuts import render 
from dssetup.service import domainService 
import time 

def domainStatistics(request,year):
    """ 
                   显示year 年份的域名申请的统计 
    
    """
    if(not year):
        year=time.localtime()[0]
    return render(request,"chart.html",{"counter_array":domainService.getDomainStatistics(year),"year":year})

def showDetailOfDomain(request,Id):
    detail = domainService.showDetailOfDomain(Id)
    return render(request,"show_detail_of_domain.html",{"domain":detail[0],"mapping":detail[1]})