#coding=utf-8
from dssetup.models import Authority


def getFormattedAuth():
    """
                      为了满足  对权限组进行添加和编辑的时候  权限这一选项 是以  父权限套子权限的 友好格式进行显示 的。这个函数式用于次功能  最终返回的是：
       [[父权限,子权限，子权限...],[父权限,子权限,子权限],[]... ]  
    
    """
    formattedAuth=[]
    auth_parent = []
    for auth in Authority.objects.all():
        if(not auth.auth_parent):
            auth_parent.append(auth)
    for auth in auth_parent:
        f_auth=[]
        f_auth.append(auth)
        for auth_child in Authority.objects.filter(auth_parent=auth):
            f_auth.append(auth_child)
        formattedAuth.append(f_auth)
   
      
    return formattedAuth