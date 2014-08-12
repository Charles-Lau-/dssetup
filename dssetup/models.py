#coding=utf-8
from django.db import models
from django.shortcuts import get_object_or_404 
from django.http import Http404
from django.db.models.signals import post_save
import hashlib
 
class Department(models.Model):
    dptName = models.CharField(max_length=30,unique=True,verbose_name=u"部门名字")
    dptLeader = models.TextField(blank=True,verbose_name=u"部门领导")
    dpt_parent = models.ForeignKey('self',blank=True,null=True,verbose_name=u"上级部门")

    def __unicode__(self):
        return self.dptName

class Authority(models.Model):
    authName = models.CharField(max_length=30,verbose_name=u"权限名")
    authDes = models.TextField(blank=True,verbose_name=u"权限描述")
    auth_parent = models.ForeignKey('self',blank=True,null=True,verbose_name=u"父权限")

    def __unicode__(self):
        return self.authName+" : "+self.authDes 

    def get_values(self):
        return {u"权限名字":self.authName,u"权限描述":self.authDes,u"父权限":self.auth_parent}

class Group(models.Model):
    groupName = models.CharField(max_length=30,unique=True,verbose_name=u"权限组名")
    groupDes = models.TextField(blank=True,verbose_name=u"组描述")
    authority = models.ManyToManyField(Authority,blank=True,null=True,verbose_name=u"权限")

    def __unicode__(self):
        return self.groupName+" : "+self.groupDes

    def get_values(self):
        return {u"组名":self.groupName,u"组描述":self.groupDes,u"拥有的权限":self.authority.all()}

    class Meta:
        ordering = ["groupName",]
   
class User(models.Model):
    userName = models.CharField(max_length=30,unique=True,verbose_name=u"用户名")
    userPassword = models.CharField(max_length=100,verbose_name=u"密码")
    group = models.ManyToManyField(Group,blank=True,null=True,verbose_name=u"权限组")
    userMail = models.EmailField(unique=True,verbose_name=u"用户邮箱")
    userPhone = models.CharField(max_length=11, blank=True,verbose_name=u"用户联系电话")
    user_dpt = models.ForeignKey(Department,verbose_name=u"用户所在部门")
    createTime = models.DateTimeField(auto_now_add=True,verbose_name=u"创建时间")
    loginLastIp = models.IPAddressField(blank=True,null=True,verbose_name=u"上次登录IP")
    loginLastTime = models.DateTimeField(blank=True,null=True,verbose_name=u"上次登录的时间")

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
        return {u"用户名":self.userName,u"邮件":self.userMail,u"权限组":self.group.all(),u"电话号码":self.userPhone,u"上次登录的IP":self.loginLastIp,u"上次登录的时间":self.loginLastTime,u"创建时间":self.createTime}

def hash_password(instance,**kwargs):
    instance.make_password(instance.userPassword)

post_save.connect(hash_password, sender=User)


class DomainApplicationForm(models.Model):

    APPCATEGORY = (
                   (u"普通","普通"),
                   (u"紧急","紧急"),
                   (u"定时","定时"),
                   
                   
                   )
    OPERCATEGORY =  (
                     (u"添加","添加"),
                     (u"删除","删除"),
                     (u"修改","修改")
                     )
    
    daDes = models.TextField(blank=True,verbose_name=u"申请表单描述")
    creater = models.ForeignKey(User)
    da_applicant = models.CharField(max_length=30,verbose_name=u"申请人")
    techRespon = models.CharField(max_length=30,verbose_name=u"技术负责人")
    proRespon = models.CharField(max_length=30,verbose_name=u"产品负责人")
    appCategory = models.CharField(max_length=10,choices=APPCATEGORY,verbose_name=u"申请类别")
    status = models.CharField(max_length=30,verbose_name=u"表单状态")
    createTime = models.DateTimeField(auto_now_add=True,verbose_name=u"创建时间")
    effectTime = models.DateTimeField(blank=True,null=True,verbose_name=u"截止日期")
    operCategory = models.CharField(max_length=30,choices=OPERCATEGORY,verbose_name=u"操作类别")
    da_dpt = models.ForeignKey(Department,verbose_name=u"域名使用部门")
    mailList = models.CharField(max_length=200,verbose_name=u"抄送邮件列表")

    def __unicode__(self):
        return "%s-%s-%s" % (self.creater,self.status,self.createTime)

    def get_values(self):
 
        return {u"申请人":self.da_applicant,
                u"技术负责人":self.techRespon,
                u"产品负责人":self.proRespon,
                u"创建时间":str(self.createTime),
                u"操作类型":self.operCategory,
                u"申请类别":self.appCategory,
                u"使用该域名的部门":self.da_dpt.dptName,
                u"申请表单描述":self.daDes,
                u"表单状态":self.status}
    class Meta:
        ordering = ["createTime",]
   
class ApplicationFormStatus(models.Model):
    status = models.CharField(max_length=30,verbose_name=u"表单状态")
    status_user = models.ForeignKey(User,verbose_name=u"将表单改变为目前状态的人")
    createTime = models.DateTimeField(auto_now_add=True,verbose_name=u"创建时间 ")
    status_da = models.ForeignKey(DomainApplicationForm,verbose_name=u"该记录对应的申请单")
    statusDes = models.CharField(max_length=50,verbose_name=u"状态改变描述",blank=True,null=True)

    class Meta:
        ordering = ["createTime",]

    def get_values(self):
        return {u"表单状态":self.status,
                u"将表单改变为目前状态的人":self.status_user.userName,
                u"状态改变描述":self.statusDes,
                u"操作时间": str(self.createTime)
                }
        
        
class Zone(models.Model):
    zoneName = models.CharField(max_length=50,verbose_name=u"域名名字")
    manageServer = models.IPAddressField(max_length=50,verbose_name=u"管理服务器")
    zone_dpt = models.ForeignKey(Department,verbose_name=u"管理该域名的部门")

    def __unicode__(self):
        return "%s-%s-%s" % (self.zoneName,self.manageServer,self.zone_dpt)

    def get_values(self):
        return {u"域名":self.zoneName,
                u"管理服务器":self.manageServer,
                u"域名所属部门":self.zone_dpt
                }
        
class DomainForm(models.Model):
    domainName = models.URLField(max_length=50,verbose_name=u"域名名字")
    domainDes = models.TextField(blank=True,verbose_name=u"域名描述")
    status = models.CharField(max_length=30,verbose_name=u"域名状态")
    domain_zone = models.ForeignKey(Zone,verbose_name=u"域名的父域名")
    da_domain = models.ManyToManyField(DomainApplicationForm,blank=True,null=True,verbose_name=u"该域名对应的申请单")

    def get_values(self):
        return {
                u"域名":self.domainName,
                u"域名描述":self.domainDes,
                u"域名状态":self.status,
                u"父域名":self.domain_zone,
                 
                }
    
    
class ServiceProvider(models.Model):
    spName = models.CharField(max_length=30,verbose_name=u"服务供应商名字")
    spNameEn = models.CharField(max_length=30,verbose_name=u"供应商英文名")
    
    def __unicode__(self):
        return self.spName

class DomainMapping(models.Model):
    dm_domain = models.ForeignKey(DomainForm,verbose_name=u"域名映射对应的域名")
    dm_sp = models.ForeignKey(ServiceProvider,verbose_name=u"服务供应商")
    mode = models.CharField(max_length=10,verbose_name=u"模式")
    aim = models.CharField(max_length=50,verbose_name=u"IP或域名")
    dm_appform = models.ForeignKey(DomainApplicationForm)
    def get_values(self):
        return {"dm_sp":self.dm_sp.spNameEn,
                 "aim":self.aim}