"""OVC care section urls."""
from django.conf.urls import *
from django.contrib import admin
admin.autodiscover()

# This should contain urls related to registry ONLY

urlpatterns = [
    'cpovc_ovc.views',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'ovc_home', name='ovc_home'),
    url(r'^ovc/search/$', 'ovc_search', name='ovc_search'),
    url(r'^ovc/new/(?P<id>\d+)/$',
        'ovc_register', name='ovc_register'),
    url(r'^ovc/edit/(?P<id>\d+)/$',
        'ovc_edit', name='ovc_edit'),
    url(r'^ovc/view/(?P<id>\d+)/$',
        'ovc_view', name='ovc_view'),
    url(r'^hh/view/(?P<hhid>[0-9A-Za-z_\-]+)/$',
        'hh_manage', name='hh_manage')
]
