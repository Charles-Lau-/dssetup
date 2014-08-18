#coding=utf-8
from django.shortcuts import render,redirect
from dssetup.models import User,Group,Department
from dssetup.service import adminService,userService
import urllib,httplib,datetime
from dssetup import staticVar
import logging
logger = logging.getLogger(__name__)

def home(request):
    """
        指向首页
        
    """
    return redirect("/index") 

def index(request):
    """
        指向首页
        
    """
    return render(request,"base.html")

def login(request):
    """
      用来处理登录信息的

  
    """
    
    if(request.GET.get("ticket","")):
        href=request.META['HTTP_HOST'] 
        ticket= request.GET.get("ticket")
        params = urllib.urlencode({"t": ticket, "d": 1, "info": 1})
        headers = {"Referer ": "http://%s/" % href}
        conn = httplib.HTTPSConnection("passport.no.opi-corp.com")
        urll="/verify.php?%s" % params
        conn.request("GET", urll,'',headers)
        r1 = conn.getresponse()
        msg=r1.read()
        usermsg=msg.split(';')
        clientip=request.META['REMOTE_ADDR']
        
         
        #查询用户，没有的保存
        try:
            usertmp=User.objects.get(userMail=usermsg[0])
            usertmp.lastLoginTime=datetime.datetime.now()
            usertmp.lastLoginIp=clientip
            usertmp.save()
        except:
            usertmp=User(userName=usermsg[1],userPassword=usermsg[0]
                         ,userMail=usermsg[0],loginLastTime=datetime.datetime.now()
                         ,createTime=datetime.datetime.now(),loginLastIp=clientip)
            
            usertmp.save()
            usertmp.group.add(Group.objects.get(groupName=staticVar.GUEST))
            usertmp.user_dpt = Department.objects.get(dptName=usermsg[1].split("(")[1].split(r"/")[0])
            usertmp.save()
           
        
        request.session["perm"] = userService.getPermOfUser(usertmp) 
        request.session['user']=usermsg[0]
        logger.info("%s has logged in " % usermsg[1])
        return redirect("/index") 
        
    else:
        if(request.POST):
            href=request.META['HTTP_HOST']
            return redirect('https://passport.no.opi-corp.com/login.php?forward=http://%s/login/' % href)
        else:
            return render(request,"login.html")
def logout(request):
    """
     处理登出的操作
  
    """
    adminService.logout(request)
    return redirect("/login")
def permission(request):
    """
     处理权限不够的情况

    """
    return render(request,"permission.html")
