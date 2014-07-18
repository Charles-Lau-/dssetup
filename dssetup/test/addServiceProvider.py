from dssetup.models import ServiceProvider


s1 = ServiceProvider(spName="1",spNameEn="dx")
 
s2 = ServiceProvider(spName="2",spNameEn="liantong")
 
s3 = ServiceProvider(spName="3",spNameEn="tietong")
 
s4 = ServiceProvider(spName="4",spNameEn="haiwai")
 
s5 = ServiceProvider(spName="5",spNameEn="yidong")

s1.save()
s2.save()
s3.save()
s4.save()
s5.save()