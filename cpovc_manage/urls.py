"""Urls for Settings."""
from django.urls import include, path

# This should contain urls related to settings ONLY
urlpatterns = include(
    'cpovc_manage.views',
    path(r'^$', 'manage_home', name='manage_home'),
    path(r'^travel/$', 'home_travel', name='home_travel'),
    path(r'^integration/$', 'integration_home', name='integration_home'),
    path(r'^travel/edit/(?P<id>\d+)/$', 'edit_travel', name='edit_travel'),
    path(r'^travel/view/(?P<id>\d+)/$', 'view_travel', name='view_travel'),
    path(r'^travel/pdf/(?P<id>\d+)/$', 'travel_report', name='travel_report'),
    # Integrations
    path(r'^api/(?P<case_id>[0-9A-Za-z_\-{32}\Z]+)/$',
        'process_integration', name='process_integration'),
    path(r'^doc/(?P<doc_id>\d+)/(?P<case_id>[0-9A-Za-z_\-{32}\Z]+)/$',
        'get_document', name='get_document'),
    path(r'^dq/$', 'dq_home', name='dq_home'),
    path(r'^se/$', 'se_home', name='se_home'),
    path(r'^sedata/$', 'se_data', name='se_data'),
    # DQA
    path(r'^dq/$', 'dq_home', name='dq_home'),
    path(r'^dqdata/$', 'dq_data', name='dq_data'),
)
