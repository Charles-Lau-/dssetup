#coding=utf-8
from django import forms
from django.core.exceptions import ValidationError
from dssetup.models import User,Group,Authority
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
    