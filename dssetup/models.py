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
class Authority(models.Model):
    authName = models.CharField(max_length=30)
    authDes = models.TextField(blank=True)
    auth_parent = models.ForeignKey('self',blank=True,null=True)
    def __unicode__(self):
        return self.authName 
    def get_values(self):
        return {"authName":self.authName,"authDescription":self.authDescription,"auth_father":self.auth_father}
class Group(models.Model):
    groupName = models.CharField(max_length=30,unique=True)
    groupDes = models.TextField(blank=True)
    authority = models.ManyToManyField(Authority,blank=True,null=True)
    def __unicode__(self):
        return self.groupName
    def get_values(self):
        return {"groupName":self.groupName,"groupDescription":self.groupDescription,"authority":self.authority.all()}
class User(models.Model):
    userName = models.CharField(max_length=30,unique=True)
    userPassword = models.CharField(max_length=100)
    group = models.ManyToManyField(Group,blank=True,null=True)
    userMail = models.EmailField(unique=True)
    userPhone = models.CharField(max_length=11,blank=True,unique=True)
    user_dpt = models.ForeignKey(Department)
    createTime = models.DateTimeField(auto_now=True)
    loginLastIp = models.IPAddressField(blank=True)
    loginLastTime = models.DateField(blank=True)
    def __unicode__(self):
        return self.userName,self.userMail,self.userPhone
    def is_authenticated(self):
        try:
            
            self.make_password(self.password)
            get_object_or_404(User,username=self.username,password=self.password)
            
            return True
        except Http404:
            print self.password
            return False
     
    def make_password(self,raw_password):
        hs = hashlib.md5()
        hs.update(raw_password)
        self.password = str(hs.hexdigest())
    def get_values(self):
        return {"username":self.username,"realName":self.realName,"group":self.group.all(),"email":self.email}
def hash_password(instance,**kwargs):
    instance.make_password(instance.password)

post_save.connect(hash_password, sender=User)

class DomainApplicationForm(models.Model):
    daDes = models.TextField(blank=True)
    creater = models.ForeignKey(User)
    da_applicant = models.CharField(max_length=30)
    techRespon = models.CharField(max_length=30)
    proRespon = models.CharField(max_length=30)
    appCategory = models.CharField(max_length=10)
    status = models.CharField(max_length=30)
    createTime = models.DateTimeField(auto_now=True)
    effectTime = models.DateTimeField(blank=True,null=True)
    operCategory = models.CharField(max_length=30)
    da_dpt = models.ForeignKey(Department)
    mailList = models.CharField(max_length=200)
class ApplicationFormStatus(models.Model):
    status = models.CharField(max_length=30)
    status_user = models.ForeignKey(User)
    createTime = models.DateTimeField(auto_now=True)
    status_da = models.ForeignKey(DomainApplicationForm)
class Zone(models.Model):
    zoneName = models.URLField(max_length=50)
    manageServer = models.IPAddressField(max_length=50)
    zone_dpt = models.ForeignKey(Department)
class DomainForm(models.Model):
    domainName = models.URLField(max_length=50)
    domainDes = models.TextField(blank=True)
    status = models.CharField(max_length=30)
    domain_zone = models.ForeignKey(Zone)
    da_domain = models.ManyToManyField(DomainApplicationForm)
class ServiceProvider(models.Model):
    spName = models.CharField(max_length=30)
    spNameEn = models.CharField(max_length=30)
class DomainMapping(models.Model):
    mode = models.CharField(max_length=10)
    aim = models.IPAddressField(max_length=50)
    dm_domain = models.ForeignKey(DomainForm)
    dm_sp = models.ForeignKey(ServiceProvider)
        