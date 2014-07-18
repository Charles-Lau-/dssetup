from dssetup.models import DomainMapping


for o in DomainMapping.objects.all():
    print  o.id