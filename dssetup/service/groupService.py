#coding=utf-8
from dssetup.models import User,Group
from django.shortcuts import get_object_or_404
 
def addUserIntoGroup(groupId,userId):
    """
                     将user添加到某个权限组
        
    """
  
    user = get_object_or_404(User,id=userId)
    group = Group.objects.get(id=groupId)
  
    user.group.add(group)
    
def getUsersNotInThisGroup(Id):
    """
              获得所有不在Id表示的权限组的user  这个函数 服务于 将 用户批量添加至某个权限组的功能
      
    """
    group = get_object_or_404(Group,id=Id)
    return User.objects.exclude(group = group)