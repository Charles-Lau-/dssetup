 #coding=utf-8
from dssetup.models import User,Group,Authority 
def getAllObject(obj):
    if(obj == "user"):
        objs_list = User.objects.all()
    elif(obj == "group"):
        objs_list = Group.objects.all()
    else:
        objs_list = Authority.objects.all()
    return objs_list

def deleteObjectById(obj,Id):
    if(obj == "user"):
        User.objects.get(id=Id).delete()
    elif(obj == "group"):
        Group.objects.get(id=Id).delete()
    else:
        Authority.objects.get(id=Id).delete() 

def logout(username,ip,time):
    user = User.objects.get(userName=username)
    user.loginLastIp = ip
    import datetime
    user.loginLastTime = datetime.datetime(*time)
     
    user.save()