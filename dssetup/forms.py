#coding=utf-8
from django import forms
from dssetup.models import Account,Group,Authority
class AccountForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:     
        model = Account
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
class AuthorityForm(forms.ModelForm):
    class Meta:
        model = Authority