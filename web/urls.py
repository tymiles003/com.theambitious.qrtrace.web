from django.conf.urls import patterns, url, include
from django.contrib import admin 
from web.general import views as general_views
from django.views.static import serve
from web.registration import urls as registration_urls
from web.member import urls as member_urls
from web.track import urls as track_urls
from web.campaign import urls as campaign_urls
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles import views

# Admin crap
admin.autodiscover()


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),


    url(r'^$', general_views.home),
    url(r'^qr$', general_views.qr),
    url(r'^r/',  include(registration_urls)),
    url(r'^t/',  include(track_urls)),
    url(r'^m/',  include(member_urls)),
    url(r'^campaign/', include(campaign_urls))

   
]
if settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', views.serve),
    ]
