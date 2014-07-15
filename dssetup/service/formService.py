from dssetup.models import DomainApplicationForm
 
def getFormOfApplicant(applicant):
    return DomainApplicationForm.objects.filter(creater = applicant)