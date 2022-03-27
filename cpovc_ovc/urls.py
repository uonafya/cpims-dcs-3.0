"""OVC care section urls."""
from django.urls import re_path
from . import views

# This should contain urls related to registry ONLY
urlpatterns = [
    # 'cpovc_ovc.views',
    re_path(r'^$', views.ovc_home, name='ovc_home'),
    re_path(r'^ovc/search/$', views.ovc_search, name='ovc_search'),
    re_path(r'^ovc/new/(?P<id>\d+)/$', views.ovc_register, name='ovc_register'),
    re_path(r'^ovc/edit/(?P<id>\d+)/$', views.ovc_edit, name='ovc_edit'),
    re_path(r'^ovc/view/(?P<id>\d+)/$', views.ovc_view, name='ovc_view'),
    re_path(r'^hh/view/(?P<hhid>[0-9A-Za-z_\-]+)/$', views.hh_manage, name='hh_manage'),
    ]
