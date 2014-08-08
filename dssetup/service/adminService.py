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

def getPermOfUser(user):
    perm = []
    groups = User.objects.get(id=user.id).group.all()
    for group in groups:
        for auth in group.authority.all():
            auth_children = Authority.objects.filter(auth_parent=auth)
            if(auth_children):
                for auth_child in auth_children:
                    if(not auth_child.authName in perm):
                        perm .append(auth_child.authName)
            else:
                if(not auth.authName in perm):
                    perm.append(auth.authName)
    print perm
    return perm
def logout(request):
    username = request.session["user"]
    ip = request.session["ip"]
    time = request.session["time"]
    user = User.objects.get(userName=username)
    user.loginLastIp = ip
    import datetime
    user.loginLastTime = datetime.datetime(*time)
    user.save()
    
    from django.contrib.sessions.models import  Session
    Session.objects.get(pk=request.COOKIES["sessionid"]).delete()

def addUserIntoGroup(groupId,userId):
    user = User.objects.get(id=userId)
    user.group.add(Group.objects.get(id=groupId))
    
def getUsersNotInThisGroup(Id):
    return User.objects.exclude(group = Group.objects.get(id=Id))