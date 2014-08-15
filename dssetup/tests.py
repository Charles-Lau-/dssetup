#coding=utf-8
from dssetup.models import   ApplicationFormStatus,DomainApplicationForm,DomainForm,DomainMapping
from dssetup.forms import   validate_url

for i in DomainMapping.objects.filter(dm_domain=DomainForm.objects.get(domainName="tt",domainType=1)):
     print i.get_values()