#coding=utf-8
from dssetup.models import   ApplicationFormStatus,DomainApplicationForm,DomainForm
from dssetup.forms import   validate_url

for i in DomainApplicationForm.objects.filter(createTime__contains="2014-08-12"):
    print i.createTime