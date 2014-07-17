#coding=utf-8
from django import forms
from django.core.exceptions import ValidationError
from dssetup.models import User,Group,Authority,DomainApplicationForm
from django.core.validators import EmailValidator
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

def UniqueUsernameIgnoreCaseValidator(value):
    if(User.objects.filter(userName__iexact=value).exists()):
        raise ValidationError("User with this Username already exists.")
def TooEasyPasswordValidator(value):
    if(len(value)<6):
        raise ValidationError("Password should at least longer than 6")
    

def InvalidPhoneNumber(value):
    import re
    isMatched = bool(re.match(r"^\d{11}$",value))
    if(not isMatched):
        raise ValidationError("Please enter a phone number with 11 digits")
class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), 
                                          label="Confirm your password",
                                          required=True)
  
     
    class Meta:     
        model = User
        fields = ("userName","group","user_dpt","userPhone","userMail","userPassword")
    
    def __init__(self,*args,**kwargs):
        super(UserForm,self).__init__(*args,**kwargs)
        self.fields["userName"].validators.append(InvalidUsername)
        self.fields["userName"].validators.append(UniqueUsernameIgnoreCaseValidator)
        self.fields["userPhone"].validators.append(InvalidPhoneNumber)
        self.fields["userPassword"].validators.append(TooEasyPasswordValidator)
    
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

class AuthorityForm(forms.ModelForm):
    class Meta:
        model = Authority

class DomainApplicationFormForm(forms.ModelForm):
    class Meta:
        model = DomainApplicationForm
        fields = ["da_applicant","techRespon","proRespon","appCategory","operCategory","da_dpt","mailList"]
    def __init__(self,*args,**kwargs):
        super(DomainApplicationFormForm,self).__init__(*args,**kwargs)
        self.fields["mailList"].validators.append(InvalidMailList)

class DomainForm(forms.Form):
    MODE = (
            ("1","cname"),
            ("2","add")
            )
    SPNAME = (
              ("1","dx"),
              ("2","liantong"),
              ("3","tietong"),
              ("4","haiwai"),
              ("5","yidong"),
              
              )
    domainName = forms.URLField(max_length=50)
    spName1 = forms.ChoiceField(choices=SPNAME)
    mode1 = forms.ChoiceField(choices=MODE)
    aim1 = forms.IPAddressField(max_length=50)
    spName2 = forms.ChoiceField(choices=SPNAME)
    mode2 = forms.ChoiceField(choices=MODE)
    aim2 = forms.IPAddressField(max_length=50)
    
    spName3 = forms.ChoiceField(choices=SPNAME)
    mode3 = forms.ChoiceField(choices=MODE)
    aim3 = forms.IPAddressField(max_length=50)
    
    spName4 = forms.ChoiceField(choices=SPNAME)
    mode4 = forms.ChoiceField(choices=MODE)
    aim4 = forms.IPAddressField(max_length=50)
    
    