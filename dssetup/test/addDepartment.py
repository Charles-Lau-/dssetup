from dssetup.models import Department

d1 =  Department(dptName="It")
d2 = Department(dptName="Research")
d3 = Department(dptName="Service")
d4 = Department(dptName="Logistics")

d1.save()
d2.save()
d3.save()
d4.save()