#coding=utf-8
from dssetup.models import User,Authority
from django.shortcuts import get_object_or_404
 
def getUser(request):
    """
                   从request里面获得user对象

    """
    return  get_object_or_404(User,userMail=request.session["user"])


def getPermOfUser(user):
    """
                   获得用户的权限列表
                   当用户的权限里面含有父权限的时候 返回的是该父权限下的所有子权限

    """
    perm = []
    groups =  get_object_or_404(User,id=user.id).group.all()
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