#coding=utf-8
from dssetup.models import ServiceProvider


s1 = ServiceProvider(spName="电信",spNameEn="dx")
 
s2 = ServiceProvider(spName="移动",spNameEn="liantong")
 
s3 = ServiceProvider(spName="联通",spNameEn="tietong")
 
s4 = ServiceProvider(spName="铁通",spNameEn="haiwai")
 
s5 = ServiceProvider(spName="海外",spNameEn="yidong")

s1.save()
s2.save()
s3.save()
s4.save()
s5.save()