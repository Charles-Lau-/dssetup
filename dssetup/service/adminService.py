 #coding=utf-8
from dssetup.models import User,Group,Authority,DomainForm,Zone
from django.shortcuts import get_object_or_404
from django.contrib.sessions.models import  Session

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
        objs_list = DomainForm.objects.filter(domainType=1)
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
        return get_object_or_404(User,id=Id) 
    elif(obj == "group"):
        return get_object_or_404(Group,id=Id)
    elif(obj=="authority"):
        return get_object_or_404(Authority,id=Id) 
    elif(obj=="domain"):
        return get_object_or_404(DomainForm,id=Id)
    elif(obj == "zone"):
        return get_object_or_404(Zone,id=Id)

def logout(request):
    """
                处理登出

    """
    

    Session.objects.get(pk=request.COOKIES["sessionid"]).delete()