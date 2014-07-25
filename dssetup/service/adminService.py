 #coding=utf-8
from dssetup.models import User,Group,Authority,DomainForm,Zone
def getAllObject(obj):
    if(obj == "user"):
        objs_list = User.objects.all()
    elif(obj == "group"):
        objs_list = Group.objects.all()
    elif(obj == "authority"):
        objs_list = Authority.objects.all()
    elif(obj =="domain"):
        objs_list = DomainForm.objects.all()
    elif(obj == "zone"):
        objs_list = Zone.objects.all()
    return objs_list

def deleteObjectById(obj,Id):
    getObjectById(obj,Id).delete() 
def getObjectById(obj,Id):
    if(obj == "user"):
        return User.objects.get(id=Id) 
    elif(obj == "group"):
        return Group.objects.get(id=Id) 
    elif(obj=="authority"):
        return Authority.objects.get(id=Id)
    elif(obj=="domain"):
        return DomainForm.objects.get(id=Id)
    elif(obj == "zone"):
        return Zone.objects.get(id=Id)
def getUser(request):
    user = User.objects.get(userName=request.session["user"])
    
    return user
def logout(username,ip,time):
    user = User.objects.get(userName=username)
    user.loginLastIp = ip
    import datetime
    user.loginLastTime = datetime.datetime(*time)
     
    user.save()