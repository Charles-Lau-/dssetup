#coding=utf-8
from dssetup.models import  ServiceProvider

s1 = ServiceProvider(spName=u"上海电信",spNameEn="shdx")
s2 = ServiceProvider(spName=u"北京移动",spNameEn="bjyd")
s3 = ServiceProvider(spName=u"江苏联通",spNameEn="jslt")
s4 = ServiceProvider(spName=u"浙江移动",spNameEn="zjyd")
s5 = ServiceProvider(spName=u"未来电信",spNameEn="wldx")

s1.save()
s2.save()
s3.save()
s4.save()
s5.save()