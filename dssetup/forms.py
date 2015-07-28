#coding=utf-8
from django import forms
from django.core.exceptions import ValidationError
from dssetup.models import User,Group,Authority,DomainApplication,ServiceProvider,Zone,DomainForm
from django.core.validators import validate_email,validate_ipv46_address
import re

def validate_url(value):
    """
                     验证URL是否合法、
       
    """
    regex = re.compile(
                r'(\w+)(\.(\w+))*$', re.IGNORECASE) 
    if(not regex.match(value)):
        raise ValidationError(u"请输入空格为间隔的url列表  如： url1 url2 url3")
   
def InvalidRootDomain(value):
    """
                    验证申请的主域名是否存在
      
    """
    try:
       
        Zone.objects.get(zoneName=value)
    
    except Zone.DoesNotExist:
 
        raise ValidationError(u"域名不存在")
    
def InvalidIpList(value):
    """
                         验证ip,ip是否合法

    """
    ips = value.split(",")
    try: 
        for ip in ips:
            validate_ipv46_address(ip)
            
    except ValidationError:
        raise ValidationError(u"请输入 iplist　如格式： ip1,ip2,ip3")
    
def InvalidMailList(value):
    """
                     验证邮件列表是否合法
      
    """
    emails = value.split(",")
  
    try:
        
        for email in emails:
 
            validate_email(email)
         
    except ValidationError:
      
        raise ValidationError(u"请输入maillist 如格式：exmaple@xxx.com,example@xxx.com")
    
def InvalidUsername(value):
    if('@' in value or '+' in value or '-' in value or ' ' in value): 
        raise ValidationError(u"请输入合法的用户名")

   
def TooEasyPasswordValidator(value):
    if(len(value)<6):
        raise ValidationError(u"密码应该长于6位")
    

def InvalidPhoneNumber(value):
    """
                         验证手机号码的合法性
      
    """
    isMatched = bool(re.match(r"^\d{11}$",value))
    if(not isMatched):
        raise ValidationError(u"请输入合法的11位数字")
    
class UserForm(forms.ModelForm):
    """
                   用户表单
       
    """
    userPassword =forms.CharField(widget=forms.PasswordInput(),label=u"密码")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), 
                                          label=u"确认密码",
                                          required=True)
  
     
    class Meta:     
        model = User
        fields = ("userName",
                  "group",
                  "user_dpt",
                  "userPhone",
                  "userMail",
                  "userPassword")
    
    def __init__(self,*args,**kwargs):
        super(UserForm,self).__init__(*args,**kwargs)
        self.fields["userName"].validators.append(InvalidUsername)
        self.fields["userPhone"].validators.append(InvalidPhoneNumber)
        self.fields["userPassword"].validators.append(TooEasyPasswordValidator)
    
    def full_clean(self):
        """
                                  去掉了空格
          
        """
        data = self.data.copy() 
        for k,vs in data.lists():
            new_vs=[]
            for v in vs:
                new_vs.append(v.strip())
            data.setlist(k,new_vs)
     
        self.data = data
         
        super(UserForm,self).full_clean()
        
    def clean(self):
        super(UserForm,self).clean()
        password =  self.cleaned_data.get("userPassword")
        confirm_password = self.cleaned_data.get("confirm_password")
        if(password and password != confirm_password):
            self._errors["userPassword"] = self.error_class([u"密码不匹配 "])
        return self.cleaned_data

class GroupForm(forms.ModelForm):
    """
                              群 组表单
          
    """
    authority = forms.ModelMultipleChoiceField(queryset=Authority.objects.all(),widget=forms.CheckboxSelectMultiple,label=u"权限")
    class Meta:
        model = Group
    
    def full_clean(self):
        """
                             去掉了空格
          
        """
        data = self.data.copy() 
        for k,vs in data.lists():
            new_vs=[]
            for v in vs:
                new_vs.append(v.strip())
            data.setlist(k,new_vs)
     
        self.data = data
      
        super(GroupForm,self).full_clean()
      
class AuthorityForm(forms.ModelForm):
    """
                  权限表单
       
    """
    class Meta:
        model = Authority
    
    def full_clean(self):
        """
                            去掉了空格
          
        """
        data = self.data.copy() 
        for k,vs in data.lists():
            new_vs=[]
            for v in vs:
                new_vs.append(v.strip())
            data.setlist(k,new_vs)
     
        self.data = data
         
        super(AuthorityForm,self).full_clean()

class DomainApplicationForm(forms.ModelForm):
    """
                   域名申请表单的主要部分对应的表单
      
    """
    ROOT = ((zone.zoneName,zone.zoneName) for zone in Zone.objects.all())
    
    RootDomain = forms.ChoiceField(choices=ROOT,label=u"主域名")
    effectTime = forms.DateTimeField(input_formats=["%Y-%m-%d %H:%M",],label=u"截止时间",
                                     error_messages={"required":"This field is required",
                                                     "invalid":"please input like yy-mm-dd HH:MM"},
                                     required=False)
    class Meta:
        model = DomainApplication
        fields = ["da_applicant",
                  "techRespon",
                  "proRespon",
                  "appCategory",
                  "operCategory",
                  "da_dpt",
                  "mailList",
                  "effectTime",
                  "daDes"]
        
    def __init__(self,*args,**kwargs):
        super(DomainApplicationForm,self).__init__(*args,**kwargs)
        self.fields["mailList"].validators.append(InvalidMailList)
        self.fields["RootDomain"].validators.append(InvalidRootDomain)
     
  
class DomainMappingForm(forms.Form):
    """
                    域名申请单中的映射部分对应的表单
      
    """
    MODE = (
            ("cname","cname"),
            ("a","a")
            )
    
    SPNAME = ((sp.spName,sp.spName) for sp in ServiceProvider.objects.all())
    
   
    mode = forms.ChoiceField(choices=MODE,label=u"模式")
    aim = forms.CharField(max_length=100,label=u"IP或域名",required=True) 
    spName = forms.MultipleChoiceField(label=u"服务供应商",choices=SPNAME,widget=forms.CheckboxSelectMultiple)
    
    def clean(self):
        """
                                验证aim 和 mode字段的值是否一致。a mode对应 ip,cname对应url
    
        """
        super(DomainMappingForm,self).clean()
        if(self.cleaned_data["mode"]=="cname"):
            try:
                if(self.cleaned_data.get("aim")):
                    for url in self.cleaned_data.get("aim").split(" "):
                        validate_url(url)
              
            except  ValidationError,e:
               
                self._errors["aim"] = self.error_class([e.message])
            else:
                try:
                    for url in self.cleaned_data.get("aim").split(","):
                        validate_ipv46_address (url)
                except ValidationError:
                    pass
                else:
                    self._errors["aim"] = self.error_class([u"当为cname格式的时候 请输入url列表"])    
                    
        else:
            try:
                InvalidIpList(self.cleaned_data["aim"])
            except ValidationError:
                self._errors["aim"] = self.error_class([u"当为a格式的时候 请输入逗号分隔的ipList"])
        
        return self.cleaned_data
    
    def excludeSelected(self,selected):
        """
                                        为了实现 当sp供应商选择了以后  就不再出现在页面供大家选择的功能
                                         
           selected: 已经选择的sp服务供应商的列表                              
        """
        validChoices = ((sp.spName,sp.spName) for sp in ServiceProvider.objects.all() if sp.spName not in selected)
        self.fields["spName"]  = forms.MultipleChoiceField(choices=validChoices,widget=forms.CheckboxSelectMultiple)
         
    def isAllowedToAdd(self):
        """
                                     当所有的服务供应商被选择完毕后 我们不再允许其添加域名映射
          
        """
        if(self.fields["spName"].choices):
            return True
        else:
            return False
   
   
            
class ZoneForm(forms.ModelForm):
    """
                        主域名表单，后台管理的时候使用  用来add 和 edit 主域名
       
    """
    class Meta:
        model = Zone
        
    def __init__(self,*args,**kwargs):
        super(ZoneForm,self).__init__(*args,**kwargs)
        self.fields["zoneName"].validators.append(validate_url)
  
class DomainFormForm(forms.ModelForm):
    """
                     域名表单，后台管理的时候使用  用来edit域名

    """
    class Meta:
        model = DomainForm
        fields = ["domainName",
                  "status",
                  "domain_zone",
                  "domainType"]
        
