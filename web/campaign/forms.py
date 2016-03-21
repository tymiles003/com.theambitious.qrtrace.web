from django import forms
from web.campaign.models import Note, Campaign, Click


class ClickForm(forms.ModelForm):
      
    class Meta:
        model = Click
        fields = ('click_type','campaign', 'ip', 'user_agent', )



class NoteForm(forms.ModelForm):
    
    email = forms.EmailField(label="Email", initial="", required=True)
    note = forms.CharField(label="Note", initial="", max_length=1024, required=True)
    
    class Meta:
        model = Note
        fields = ('campaign', 'email', 'note', 'ip', 'user_agent', )


class NewStdCampaignForm(forms.ModelForm):
    
    name = forms.CharField(label="Name", initial="", max_length=80, required=True)
    data = forms.CharField(label="Data", initial="", max_length=7089, required=True)
    
    class Meta:
        model = Campaign
        fields = ('name', 'data', 'campaign_type', 'user' )
