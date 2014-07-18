from dssetup.models import Zone,Department

z1 = Zone(zoneName="http://www.renren.com",manageServer="192.168.1.2")
z2 = Zone(zoneName="http://www.jingwei.com",manageServer="192.168.1.3")
z3 = Zone(zoneName="http://www.youxi.com",manageServer="192.168.1.4")
 

z1.zone_dpt = Department.objects.get(dptName="It")
z2.zone_dpt = Department.objects.get(dptName="It")
z3.zone_dpt = Department.objects.get(dptName="It")

z1.save()
z2.save()
z3.save()
 
z4 = Zone(zoneName="http://www.maopu.com",manageServer="192.168.1.5")
z5 = Zone(zoneName="http://www.duowan.com",manageServer="192.168.1.6")
 

z4.zone_dpt = Department.objects.get(dptName="Research")
z5.zone_dpt = Department.objects.get(dptName="Research")

z4.save()
z5.save()

 
z6 = Zone(zoneName="http://www.baidu.com",manageServer="192.168.1.7")
z7 = Zone(zoneName="http://www.sina.com",manageServer="192.168.1.8")
z8 = Zone(zoneName="http://www.google.com",manageServer="192.168.1.9")
 
z6.zone_dpt = Department.objects.get(dptName="Service")
z7.zone_dpt = Department.objects.get(dptName="Service")
z8.zone_dpt = Department.objects.get(dptName="Service")

z6.save()
z7.save()
z8.save()



 
z9 = Zone(zoneName="http://www.aiqixi.com",manageServer="192.168.1.10")
z10 = Zone(zoneName="http://www.xxxxx.com",manageServer="192.168.1.11")
z11 = Zone(zoneName="http://www.ttyyyy.com",manageServer="192.168.1.12")
 
z9.zone_dpt = Department.objects.get(dptName="Logistics")
z10.zone_dpt = Department.objects.get(dptName="Logistics")
z11.zone_dpt = Department.objects.get(dptName="Logistics")

z9.save()
z10.save()
z11.save()