from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from views import *
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import settings
admin.autodiscover()

urlpatterns = patterns('',

     url(r'^$', add),
     url(r'^send_postcard/', send_postcard),
     url(r'^pixlr/', pixlr),
     url(r'^add/', add),
     url(r'^picmonkey/', picmonkey), 
     url(r'^picasion/', picasion), 
     url(r'^orsay/', orsay),
     url(r'^ninona/', ninona),
     url(r'^collectorsweekly/', collectorsweekly),
     url(r'^view/(.*)/(.*)', view),
     url(r'^admin/', include(admin.site.urls)),
     (r'^accounts/login/$',  login),
     (r'^accounts/logout/$', logout , {'next_page':'/'}),
     url(r'^ulogin/', include('django_ulogin.urls')),
     url(r'^check_capcha/', check_capcha),
   
)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()