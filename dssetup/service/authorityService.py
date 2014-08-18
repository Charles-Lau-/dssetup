#coding=utf-8
from dssetup.models import Authority

def getFormattedAuth():
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
   
     
    print formattedAuth
    return formattedAuth