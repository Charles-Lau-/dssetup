#coding=utf-8
from django.db import models
from django.shortcuts import get_object_or_404 
from django.http import Http404
from django.db.models.signals import post_save
import hashlib
# Create your models here.
class Department(models.Model):
    dptName = models.CharField(max_length=30)
    dptLeader = models.TextField(blank=True)
    dpt_parent = models.ForeignKey('self',blank=True,null=True)
    def __unicode__(self):
        return self.dptName

class Authority(models.Model):
    authName = models.CharField(max_length=30)
    authDes = models.TextField(blank=True)
    auth_parent = models.ForeignKey('self',blank=True,null=True)
    def __unicode__(self):
        return self.authName+" : "+self.authDes 
    def get_values(self):
        return {"authName":self.authName,"authDescription":self.authDes,"auth_parent":self.auth_parent}

class Group(models.Model):
    groupName = models.CharField(max_length=30,unique=True)
    groupDes = models.TextField(blank=True)
    authority = models.ManyToManyField(Authority,blank=True,null=True)
    def __unicode__(self):
        return self.groupName+" : "+self.groupDes
    def get_values(self):
        return {"groupName":self.groupName,"groupDescription":self.groupDes,"authority":self.authority.all()}
    
   
class User(models.Model):
    userName = models.CharField(max_length=30,unique=True)
    userPassword = models.CharField(max_length=100)
    group = models.ManyToManyField(Group,blank=True,null=True)
    userMail = models.EmailField(unique=True)
    userPhone = models.CharField(max_length=11, blank=True)
    user_dpt = models.ForeignKey(Department)
    createTime = models.DateTimeField(auto_now_add=True)
    loginLastIp = models.IPAddressField(blank=True,null=True)
    loginLastTime = models.DateTimeField(blank=True,null=True)
    def __unicode__(self):
        return self.userName+" "+self.userMail+" "+str(self.user_dpt)
    def is_authenticated(self):
        try:
            
            self.make_password(self.userPassword)
            get_object_or_404(User,userName=self.userName,userPassword=self.userPassword)
            
            return True
        except Http404:
            return False
     
    def make_password(self,raw_password):
        hs = hashlib.md5()
        hs.update(raw_password)
    def get_values(self):
        return {"username":self.userName,"mail":self.userMail,"group":self.group.all(),"phone":self.userPhone,"lastLoginIp":self.loginLastIp,"lastLoginTime":self.loginLastTime,"createTime":self.createTime}
def hash_password(instance,**kwargs):
    instance.make_password(instance.userPassword)

post_save.connect(hash_password, sender=User)


class DomainApplicationForm(models.Model):
    APPCATEGORY = (
                   ("normal","普通"),
                   ("urge","紧急"),
                   ("timing","定时"),
                   
                   
                   )
    OPERCATEGORY =  (
                     ("add","添加"),
                     ("delete","删除"),
                     )
    
    daDes = models.TextField(blank=True)
    creater = models.ForeignKey(User)
    da_applicant = models.CharField(max_length=30)
    techRespon = models.CharField(max_length=30)
    proRespon = models.CharField(max_length=30)
    appCategory = models.CharField(max_length=10,choices=APPCATEGORY)
    status = models.CharField(max_length=30)
    createTime = models.DateTimeField(auto_now_add=True)
    effectTime = models.DateTimeField(blank=True,null=True)
    operCategory = models.CharField(max_length=30,choices=OPERCATEGORY)
    da_dpt = models.ForeignKey(Department)
    mailList = models.CharField(max_length=200)
    def get_values(self):
        return {"applicant":self.da_applicant,
                "techRespon":self.techRespon,
                "proRespon":self.proRespon,
                "createTime":self.createTime,
                "operCategory":self.operCategory,
                "appCategory":self.appCategory,
                "department":self.da_dpt,
                "description":self.daDes,
                "status":self.status}
   
class ApplicationFormStatus(models.Model):
    status = models.CharField(max_length=30)
    status_user = models.ForeignKey(User)
    createTime = models.DateTimeField(auto_now_add=True)
    status_da = models.ForeignKey(DomainApplicationForm)
    
class Zone(models.Model):
    zoneName = models.URLField(max_length=50)
    manageServer = models.IPAddressField(max_length=50)
    zone_dpt = models.ForeignKey(Department)
    def __unicode__(self):
        return "%s-%s-%s" % (self.zoneName,self.manageServer,self.zone_dpt)
    def get_values(self):
        return {"zoneName":self.zoneName,
                "manageServer":self.manageServer,
                "zone_dpt":self.zone_dpt
                }
class DomainForm(models.Model):
    domainName = models.URLField(max_length=50)
    domainDes = models.TextField(blank=True)
    status = models.CharField(max_length=30)
    domain_zone = models.ForeignKey(Zone)
    da_domain = models.ManyToManyField(DomainApplicationForm,blank=True,null=True)
    def get_values(self):
        return {"domainName":self.domainName,
                "domainDes":self.domainDes,
                "status":self.status,
                "domain_zone":self.domain_zone,
                 
                }
    
class ServiceProvider(models.Model):
    spName = models.CharField(max_length=30)
    spNameEn = models.CharField(max_length=30)
    
class DomainMapping(models.Model):
    dm_domain = models.ForeignKey(DomainForm)
    dm_sp = models.ForeignKey(ServiceProvider)
    mode = models.CharField(max_length=10)
    aim = models.IPAddressField(max_length=50)