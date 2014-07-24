#coding=utf-8
from django import forms
from django.core.exceptions import ValidationError
from dssetup.models import User,Group,Authority,DomainApplicationForm,ServiceProvider
from django.core.validators import EmailValidator,validate_ipv46_address

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
            EmailValidator(email)
    except ValidationError:
        raise ValidationError("Please enter maillist like exmaple@xxx.com,example@xxx.com") 
def InvalidUsername(value):
    if('@' in value or '+' in value or '-' in value or ' ' in value): 
        raise ValidationError("Please enter valid username")

   
def TooEasyPasswordValidator(value):
    if(len(value)<6):
        raise ValidationError("Password should at least longer than 6")
    

def InvalidPhoneNumber(value):
    import re
    isMatched = bool(re.match(r"^\d{11}$",value))
    if(not isMatched):
        raise ValidationError("Please enter a phone number with 11 digits")
class UserForm(forms.ModelForm): 
    userPassword =forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput(), 
                                          label="Confirm your password",
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
        if(User.objects.filter(userName__iexact=self.userName).exists()):
            raise ValidationError("User with this Username already exists.") 
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
    class Meta:
        model = DomainApplicationForm
        fields = ["da_applicant","techRespon","proRespon","appCategory","operCategory","da_dpt","mailList","daDes"]
    def __init__(self,*args,**kwargs):
        super(DomainApplicationFormForm,self).__init__(*args,**kwargs)
        self.fields["mailList"].validators.append(InvalidMailList)

  
class DomainForm(forms.Form):
    MODE = (
            ("cname","cname"),
            ("a","a")
            )
    
    SPNAME = ((sp.spName,sp.spName) for sp in ServiceProvider.objects.all())
    
    spName = forms.MultipleChoiceField(choices=SPNAME,widget=forms.CheckboxSelectMultiple)
    mode = forms.ChoiceField(choices=MODE)
    aim = forms.CharField(max_length=100) 
    
    def __init__(self,*args,**kwargs):
        super(DomainForm,self).__init__(*args,**kwargs)
    def excludeSelected(self,selected):
        validChoices = ((sp.spName,sp.spName) for sp in ServiceProvider.objects.all() if sp.spName not in selected)
        self.fields["spName"]  = forms.MultipleChoiceField(choices=validChoices,widget=forms.CheckboxSelectMultiple)
         
    def isAllowedToAdd(self):
        if(self.fields["spName"].choices):
            return True
        else:
            return False