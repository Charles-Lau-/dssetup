#coding=utf-8
from django import forms
from django.core.exceptions import ValidationError
from dssetup.models import User,Group,Authority,DomainApplicationForm,ServiceProvider,Zone,DomainForm
from django.core.validators import validate_email,validate_ipv46_address
import re
def validate_url(value):
    regex = re.compile(
        r'^((?:http|ftp)s://)?'  # http:// or https://
        r'(localhost)?'  # localhost...
        r'(\w*[A-Za-z_]\w*)\.(\w*[A-Za-z_]\w*)\.(\w*[A-Za-z_]\w*)(.(\w*[A-Za-z_]\w*))*'  # ...or ipv4
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE) 
    if(not value):
        raise ValidationError("This field is required")
    if(not regex.match(value)):
        raise ValidationError("Invalid URL")
def InvalidRootDomain(value):
    try:
       
        Zone.objects.get(zoneName=value)
    
    except Zone.DoesNotExist:
 
        raise ValidationError("This root does not exist")
def InvalidIpList(value):
    ips = value.split(",")
    try: 
        for ip in ips:
            validate_ipv46_address(ip)
            
    except ValidationError:
        raise ValidationError("Please enter iplist like ip1,ip2,ip3")
def InvalidMailList(value):
    emails = value.split(",")
  
    try:
        
        for email in emails:
 
            validate_email(email)
         
    except ValidationError:
      
        raise ValidationError("Please enter maillist like exmaple@xxx.com,example@xxx.com") 
def InvalidUsername(value):
    if('@' in value or '+' in value or '-' in value or ' ' in value): 
        raise ValidationError("Please enter valid username")

   
def TooEasyPasswordValidator(value):
    if(len(value)<6):
        raise ValidationError("Password should at least longer than 6")
    

def InvalidPhoneNumber(value):
    
    isMatched = bool(re.match(r"^\d{11}$",value))
    if(not isMatched):
        raise ValidationError("Please enter a phone number with 11 digits")
class UserForm(forms.ModelForm): 
    userPassword =forms.CharField(widget=forms.PasswordInput(),label=u"密码")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), 
                                          label=u"确认密码",
                                          required=True)
  
     
    class Meta:     
        model = User
        fields = ("userName","group","user_dpt","userPhone","userMail","userPassword")
    
    def __init__(self,*args,**kwargs):
        super(UserForm,self).__init__(*args,**kwargs)
        self.fields["userName"].validators.append(InvalidUsername)
        self.fields["userPhone"].validators.append(InvalidPhoneNumber)
        self.fields["userPassword"].validators.append(TooEasyPasswordValidator)
    
    def full_clean(self):
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
            self._errors["userPassword"] = self.error_class(["password does not match"])
        return self.cleaned_data
class GroupForm(forms.ModelForm):
    authority = forms.ModelMultipleChoiceField(queryset=Authority.objects.all(),widget=forms.CheckboxSelectMultiple,label=u"权限")
    class Meta:
        model = Group
    
    def full_clean(self):
        data = self.data.copy() 
        for k,vs in data.lists():
            new_vs=[]
            for v in vs:
                new_vs.append(v.strip())
            data.setlist(k,new_vs)
     
        self.data = data
      
        super(GroupForm,self).full_clean()
      
class AuthorityForm(forms.ModelForm):
    class Meta:
        model = Authority
    
    def full_clean(self):
        data = self.data.copy() 
        for k,vs in data.lists():
            new_vs=[]
            for v in vs:
                new_vs.append(v.strip())
            data.setlist(k,new_vs)
     
        self.data = data
         
        super(AuthorityForm,self).full_clean()

class DomainApplicationFormForm(forms.ModelForm):
    RootDomain = forms.CharField(max_length=100,label=u"主域名")
    effectTime = forms.DateTimeField(input_formats=["%Y-%m-%d %H:%M",],label=u"截止时间",error_messages={"required":"This field is required","invalid":"please input like yy-mm-dd HH:MM"},required=False)
    class Meta:
        model = DomainApplicationForm
        fields = ["da_applicant","techRespon","proRespon","appCategory","operCategory","da_dpt","mailList","effectTime","daDes"]
    def __init__(self,*args,**kwargs):
        super(DomainApplicationFormForm,self).__init__(*args,**kwargs)
        self.fields["mailList"].validators.append(InvalidMailList)
        self.fields["RootDomain"].validators.append(InvalidRootDomain)
     
  
class DomainMappingForm(forms.Form):
    MODE = (
            ("cname","cname"),
            ("a","a")
            )
    
    SPNAME = ((sp.spName,sp.spName) for sp in ServiceProvider.objects.all())
    
   
    mode = forms.ChoiceField(choices=MODE,label=u"模式")
    aim = forms.CharField(max_length=100,label=u"IP或域名",required=True) 
    spName = forms.MultipleChoiceField(choices=SPNAME,widget=forms.CheckboxSelectMultiple,label=u"服务供应商")
    
    def __init__(self,*args,**kwargs):
        super(DomainMappingForm,self).__init__(*args,**kwargs)
    def clean(self):
        super(DomainMappingForm,self).clean()
        print self.cleaned_data
        if(self.cleaned_data["mode"]=="cname"):
            try:
                if(self.cleaned_data.get("aim")):
                    validate_url(self.cleaned_data["aim"])
              
            except  ValidationError:
               
                self._errors["aim"] = self.error_class(["This field should input valid URL when the mode is cname"])
                
        else:
            try:
                validate_ipv46_address(self.cleaned_data["aim"])
            except ValidationError:
                self._errors["aim"] = self.error_class(["This field should input IP when the mode is a"])
        
        return self.cleaned_data
    
    def excludeSelected(self,selected):
        validChoices = ((sp.spName,sp.spName) for sp in ServiceProvider.objects.all() if sp.spName not in selected)
        self.fields["spName"]  = forms.MultipleChoiceField(choices=validChoices,widget=forms.CheckboxSelectMultiple)
         
    def isAllowedToAdd(self):
        if(self.fields["spName"].choices):
            return True
        else:
            return False
   
   
            
class ZoneForm(forms.ModelForm):
    class Meta:
        model = Zone
        
class DomainFormForm(forms.ModelForm):
    class Meta:
        model = DomainForm
        