 #coding=utf-8
from dssetup.models import User,Group,Authority,DomainForm,Zone

def getAllObject(obj):
    """ 
       根据obj 来返回相应的对象列表

    """
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
    """
      根据obj 和Id 来删除相应对象

    """
    getObjectById(obj,Id).delete() 
def getObjectById(obj,Id):
    """
      根据obj 和 Id 返回 某个对象

    """
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
    """
      从request里面获得user对象

    """
    user = User.objects.get(userName=request.session["user"])
    return user

def getPermOfUser(user):
    """
       获得用户的权限列表
       当用户的权限里面含有父权限的时候 返回的是该父权限下的所有子权限

    """
    perm = []
    groups = User.objects.get(id=user.id).group.all()
    for group in groups:
        for auth in group.authority.all():
            auth_children = Authority.objects.filter(auth_parent=auth)
            if(auth_children):#如果是父权限 就返回该父权限对应的所有子权限
                for auth_child in auth_children:
                    if(not auth_child.authName in perm):
                        perm .append(auth_child.authName)
            else:
                if(not auth.authName in perm):
                    perm.append(auth.authName)
    return perm

def logout(request):
    """
      处理登出

    """
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
    """
      将user添加到某个权限组

    """
    user = User.objects.get(id=userId)
    user.group.add(Group.objects.get(id=groupId))
    
def getUsersNotInThisGroup(Id):
    """
        获得所有不在Id表示的权限组的user
      
    """
    return User.objects.exclude(group = Group.objects.get(id=Id))
