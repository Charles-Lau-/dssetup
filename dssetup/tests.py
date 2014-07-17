from dssetup.forms import DomainForm

form = DomainForm()

for field in form:
    print field.errors