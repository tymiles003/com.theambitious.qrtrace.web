from django.conf.urls import patterns, url, include
#from django.conf.urls.defaults import patterns
from web.registration import views

urlpatterns = [
    url(r'^standard/$', views.standard),
    url(r'^premium/$', views.premium),
    url(r'^premium/(?P<campaign_id>\d+)$',views.premium),

    url(r'^premium_next/$', views.premium_next),
    url(r'^premium_create_account/$', views.premium_create_account),
    url(r'^premium_upgrade_account/$', views.premium_upgrade_account),
    url(r'^premium_create_campaign/$', views.premium_create_campaign),
]
