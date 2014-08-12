#coding=utf-8
from dssetup.models import ServiceProvider


for s in ServiceProvider.objects.all():
    print s.spName
 
