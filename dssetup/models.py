#coding=utf-8
from django.db import models
from django.shortcuts import get_object_or_404 
from django.http import Http404
from django.db.models.signals import post_save
import hashlib
# Create your models here.
class Department(models.Model):
    departementName = models.CharField(max_length = 10)
    departmentDescription = models.TextField(blank=True,null=True)
    depart_super = models.ForeignKey('self',blank=True,null=True)
class Authority(models.Model):
    authName = models.CharField(max_length = 10)
    authDes = models.TextField(blank=True,null=True)
    auth_parent = models.ForeignKey('self',blank=True,null=True)
    def __unicode__(self):
        return self.authName 
    def get_values(self):
        return {"authName":self.authName,"authDescription":self.authDescription,"auth_father":self.auth_father}
class Group(models.Model):
    groupName = models.CharField(max_length = 10)
    groupDes = models.TextField(blank=True,null=True)
    authority = models.ManyToManyField(Authority,blank=True,null=True)
    def __unicode__(self):
        return self.groupName
    def get_values(self):
        return {"groupName":self.groupName,"groupDescription":self.groupDescription,"authority":self.authority.all()}
class Account(models.Model):
    userName = models.CharField(max_length=30)
    userPassword = models.CharField(max_length=100)
    group = models.ManyToManyField(Group,blank=True,null=True)
    userMail = models.EmailField()
    userPhone = models.CharField(max_length=11,blank=True,null=True)
    user_dpt = models.ForeignKey(Department,blank=True,null=True)
    createTime = models.DateField(auto_now=True)
    loginLastIp = models.IPAddressField(blank=True,null=True)
    loginLastTime = models.DateField(blank=True,null=True)
    def __unicode__(self):
        return self.username
    def is_authenticated(self):
        try:
            
            self.make_password(self.password)
            get_object_or_404(Account,username=self.username,password=self.password)
            
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

post_save.connect(hash_password, sender=Account)