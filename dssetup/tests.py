#coding=utf-8
from dssetup.models import  User

u = User.objects.get(userMail="pengkun.liu@renren-inc.com")
u.delete()
 