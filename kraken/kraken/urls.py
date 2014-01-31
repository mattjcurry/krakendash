from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout),
    url(r'^$', 'status.views.home', name='home'),
    url(r'^ops/$', 'status.views.ops', name='ops'),
    url(r'^osd/(\d+)/$', 'status.views.osd_details', name='osd_details'),
)
