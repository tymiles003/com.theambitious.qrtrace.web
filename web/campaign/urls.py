from django.conf.urls import patterns, url, include
#from django.conf.urls.defaults import patterns
from web.campaign import views

urlpatterns = [
    url(r'^preview/$', views.preview),
    url(r'^set_preview/$', views.set_preview)
]
