from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", min_length=6, max_length=128, widget=forms.PasswordInput())


class ChangePasswordForm(forms.ModelForm):
    password = forms.CharField(label="Password", initial="", min_length=6, max_length=128, widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('password',)