from django.conf.urls import patterns, url, include
#from django.conf.urls.defaults import patterns
from web.member import views

urlpatterns = [
    url(r'^dash/$', views.dash),
    url(r'^campaign/$', views.campaign),
    url(r'^campaign_new_edit/$', views.campaign_new_edit),
    url(r'^campaign_new_edit/(?P<campaign_id>\d+)$', views.campaign_new_edit),
    url(r'^campaign/(?P<campaign_type>[-\w\+]+)$', views.campaign),
    url(r'^campaign_details/(?P<campaign_id>\d+)$', views.campaign_details),    
    url(r'^campaign_export/(?P<campaign_id>\d+)$', views.campaign_export),   
    url(r'^thanks/$', views.thanks),

    url(r'^account/$', views.account),
    url(r'^log_out/$', views.log_out),
    #url(r'^(?P<meal_title5>[-\w\+]+)/(?P<meal_id>\d+)/$', 'meal_ideas_seo),
]
