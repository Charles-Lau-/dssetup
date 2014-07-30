from dssetup.models import  Authority

for auth in Authority.objects.all():
    print auth.authName

  
 