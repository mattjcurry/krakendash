from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kraken.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/login/$', login),
    (r'^accounts/logout/$', logout),
    url(r'^$', 'status.views.cluster_health', name='cluster_health'),
    url(r'^cluster-fsid/', 'status.views.cluster_fsid', name='cluster_fsid'),
    url(r'^monitor-status/', 'status.views.monitor_status', name='monitor_status'),
    url(r'^osd-crush-dump/', 'status.views.osd_crush_dump', name='osd_crush_dump'),
    url(r'^osd-map-summary/', 'status.views.osd_map_summary', name='osd_map_summary'),
    url(r'^osd-listids/', 'status.views.osd_listids', name='osd_listids'),
    url(r'^pools/$', 'status.views.pools', name='pools'),
    url(r'^pools/(.*)/$', 'status.views.pool_detail', name='pool_detail'),
    url(r'^osd/pgmap/(\d+)/$', 'status.views.pg_osd_map', name='pg_osd_map'),
    url(r'^osd-tree/', 'status.views.osd_tree', name='osd_tree'),
    url(r'^pg-status/', 'status.views.pg_status', name='pg_status'),
    url(r'^crush/$', 'status.views.crush', name='crush'),
    url(r'^crush/rules/$', 'status.views.crush_rules', name='crush_rules'),
    url(r'^crush/map/$', 'status.views.crushmap', name='crushmap'),
    url(r'^osd/$', 'status.views.osd_list', name='osd_list'),
    url(r'^osd/(\d+)/$', 'status.views.osd_details', name='osd_details'),
)
