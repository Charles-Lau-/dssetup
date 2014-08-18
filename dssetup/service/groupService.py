#coding=utf-8
from dssetup.models import User,Group

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