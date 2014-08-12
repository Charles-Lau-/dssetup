#coding=utf-8
from dssetup.models import   ApplicationFormStatus,DomainApplicationForm,DomainForm

for i in DomainForm.objects.all():
    i.delete() 