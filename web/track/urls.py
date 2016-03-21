from django.conf.urls import patterns, url, include
#from django.conf.urls.defaults import patterns
from web.track import views

urlpatterns = [
    url(r'^$', views.track),
    url(r'^save_note/$', views.save_note),
    url(r'^save_click/$', views.save_click)
]