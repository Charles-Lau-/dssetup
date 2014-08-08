#coding=utf-8
from dssetup.models import   ApplicationFormStatus,DomainApplicationForm

for i in ApplicationFormStatus.objects.all():
    print i.statusDes