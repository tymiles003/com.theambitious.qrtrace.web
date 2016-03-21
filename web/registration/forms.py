from django import forms


class StdRegForm(forms.Form):
    
    email = forms.EmailField(label="Email", initial="", required=True)
    password = forms.CharField(label="Password", initial="", min_length=4, max_length=128, widget=forms.PasswordInput(), required=True)
    name = forms.CharField(label="Name", initial="", max_length=80, required=True)
    data = forms.CharField(label="Data", initial="", max_length=7089, required=True)


class PRegForm(forms.Form):
    
    email = forms.EmailField(label="Email", initial="", required=True)
    password = forms.CharField(label="Password", initial="", min_length=4, max_length=128, widget=forms.PasswordInput(), required=True)
    name = forms.CharField(label="Name", initial="", max_length=80, required=True)
    data = forms.CharField(label="Data", initial="", max_length=7089, required=True)


class P1RegForm(forms.Form):
    
    title = forms.CharField(label="title", initial="", max_length=40, required=True)
    campaign_name = forms.CharField(label="Name", initial="", max_length=80, required=True)
    url = forms.URLField(required=True, initial='')
    
class P2RegForm(forms.Form):
    
    FB = forms.CharField(label="Facebook Page", initial="", max_length=255,  required=False)
    TW = forms.CharField(label="Twitter Username", initial="", max_length=255, required=False)
    
'''prem1 title/url (form for validation)
prem2 additional fields
if logged in and premium:
    create
elif logged and not prem
    upgrade 
else
    not logged in
'''