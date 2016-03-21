from django.conf.urls import patterns, url, include
from django.contrib import admin 
from web.general import views as general_views
from django.views.static import serve
from web.registration import urls as registration_urls
from web.member import urls as member_urls
from web.track import urls as track_urls
from web.campaign import urls as campaign_urls
from settings import MEDIA_ROOT, STATIC_ROOT


# Admin crap
admin.autodiscover()


urlpatterns = patterns('',

    #url(r'^api/', include('web.api.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # On deployment we should remove these lines and have Apache serve the files
    url(r'^robots.txt$', serve, {'path': 'robots.txt', 'document_root': STATIC_ROOT}),
    url(r'^favicon.ico$', serve, {'path': 'favicon.ico', 'document_root': STATIC_ROOT}),
    url(r'^media/images/(.*)$', serve, {'document_root': MEDIA_ROOT + 'images/'}),
    url(r'^images/(.*)$', serve, {'document_root': STATIC_ROOT + 'images/'}),
    url(r'^static/(.*)$', serve, {'document_root': STATIC_ROOT}),  # Admin
    url(r'^fonts/(.*)$', serve, {'document_root': STATIC_ROOT + 'fonts/'}),
    url(r'^js/(.*)$', serve, {'document_root': STATIC_ROOT + 'js/'}),
    url(r'^css/(.*)$', serve, {'document_root': STATIC_ROOT + 'css/'}),

    url(r'^$', general_views.home),
    url(r'^qr$', general_views.qr),
    url(r'^r/',  include(registration_urls)),
    url(r'^t/',  include(track_urls)),
    url(r'^m/',  include(member_urls)),
    url(r'^campaign/', include(campaign_urls)),

   
)
