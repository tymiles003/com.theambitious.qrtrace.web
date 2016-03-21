from django.db import models
from django.contrib.auth.models import User

CAMPAIGN_TYPE = (
    ('S', 'Standard'),
    ('P', 'Mini-Site'),
)

STATUS = (
    ('A', 'Active'),
    ('I', 'Inactive'),
)

PCAMPAIGN_LINK = (
    ('FB', 'Facebook Page'),
    ('TW', 'Twitter Page'),
    ('NOTE', 'Send us a Note'),
    ('WEB', 'Visit Website'),
                  
)

THEME_LOOKUP = {
    'a': 'Black',
    'b': 'Blue',
    'c': 'Dark Gray',
    'd': 'Light Gray',
    'e': 'Yellow',
}
PCAMPAIGN_LINK_TEXT_LOOKUP = {
    'FB': 'Facebook Page',
    'TW': 'Twitter Page',
    'NOTE': 'Send us a Note',
    'WEB': 'Visit Website',     
}


class Campaign(models.Model):
    user = models.ForeignKey(User, db_index=True)
    name = models.CharField(max_length=80,)
    data = models.CharField(max_length=7089,)
    campaign_type = models.CharField(max_length=1, choices=CAMPAIGN_TYPE, default='S') 
    premium_title = models.CharField(max_length=40, default='', null=True, blank=True)
    premium_theme = models.CharField(max_length=1, default='', null=True, blank=True)
    premium_header_theme = models.CharField(max_length=1, default='', null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS, default='A')
    updated_at = models.DateTimeField(auto_now=True)    
    created_at = models.DateTimeField(auto_now_add=True)

    def d_status(self):
        
        for k,v in STATUS:
            if k == self.status:
                return v
        return 'N/A'

    def d_campaign_type(self):
        
        for k,v in CAMPAIGN_TYPE:
            if k == self.campaign_type:
                return v
        return 'N/A'

    def d_premium_theme(self):
        if self.premium_theme in THEME_LOOKUP:
            return THEME_LOOKUP[self.premium_theme]
        else:
            return 'N/A'
        
        
    def d_premium_header_theme(self):
        if self.premium_header_theme in THEME_LOOKUP:
            return THEME_LOOKUP[self.premium_header_theme]
        else:
            return 'N/A'
        

class Note(models.Model):
    campaign = models.ForeignKey(Campaign, db_index=True)
    ip = models.CharField(max_length=39,)
    email = models.EmailField(max_length=75)
    note = models.CharField(max_length=1024) 
    user_agent = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class Premium(models.Model):
    campaign = models.ForeignKey(Campaign, db_index=True)
    seq = models.PositiveSmallIntegerField(default=1)
    name = models.CharField(max_length=10, choices=PCAMPAIGN_LINK)
    val = models.CharField(max_length=255, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def d_name(self):
        if self.name in PCAMPAIGN_LINK_TEXT_LOOKUP:
            return PCAMPAIGN_LINK_TEXT_LOOKUP[self.name]
        else:
            return 'N/A'
            
            
class Scan(models.Model):
    campaign = models.ForeignKey(Campaign, db_index=True)
    ip = models.CharField(max_length=39,)
    refer = models.CharField(max_length=255) 
    user_agent = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class Click(models.Model):
    campaign = models.ForeignKey(Campaign, db_index=True)
    click_type = models.CharField(max_length=10, choices=PCAMPAIGN_LINK)
    ip = models.CharField(max_length=39,)
    refer = models.CharField(max_length=255) 
    user_agent = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def d_click_type(self):
        if self.click_type in PCAMPAIGN_LINK_TEXT_LOOKUP:
            return PCAMPAIGN_LINK_TEXT_LOOKUP[self.click_type]
        else:      
            return 'N/A'
