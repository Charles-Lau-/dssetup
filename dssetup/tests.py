from dssetup.models import Authority,Group,User,Department
 
import time
import datetime

for u in User.objects.all():
    print u.group.get("")