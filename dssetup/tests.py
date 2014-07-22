from dssetup.models import DomainMapping,DomainApplicationForm,Authority


for o in Authority.objects.all():
    print  o.id