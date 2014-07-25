from dssetup.models import DomainMapping,DomainApplicationForm,Authority,DomainForm

for p in DomainForm.objects.all():
    p.delete()