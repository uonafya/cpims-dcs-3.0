"""Urls for Settings."""
from django.urls import re_path
from . import views

# This should contain urls related to settings ONLY
urlpatterns = [
    # 'cpovc_manage.views',
    re_path(r'^$', views.manage_home, name='manage_home'),
    re_path(r'^travel/$', views.home_travel, name='home_travel'),
    re_path(r'^integration/$', views.integration_home, name='integration_home'),
    re_path(r'^travel/edit/(?P<id>\d+)/$', views.edit_travel, name='edit_travel'),
    re_path(r'^travel/view/(?P<id>\d+)/$', views.view_travel, name='view_travel'),
    re_path(r'^travel/pdf/(?P<id>\d+)/$', views.travel_report, name='travel_report'),
    # Integrations
    re_path(r'^api/(?P<case_id>[0-9A-Za-z_\-{32}\\Z]+)/$', views.process_integration, name='process_integration'),
    re_path(r'^doc/(?P<doc_id>\d+)/(?P<case_id>[0-9A-Za-z_\-{32}\\Z]+)/$', views.get_document, name='get_document'),
    re_path(r'^dq/$', views.dq_home, name='dq_home'),
    re_path(r'^se/$', views.se_home, name='se_home'),
    re_path(r'^sedata/$', views.se_data, name='se_data'),
    # DQA
    re_path(r'^dq/$', views.dq_home, name='dq_home'),
    re_path(r'^dqdata/$', views.dq_data, name='dq_data'),
]
