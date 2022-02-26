"""Urls for Settings."""
from django.conf.urls import patterns, url

# This should contain urls related to settings ONLY
urlpatterns = patterns(
    'cpovc_manage.views',
    url(r'^$', 'manage_home', name='manage_home'),
    url(r'^travel/$', 'home_travel', name='home_travel'),
    url(r'^integration/$', 'integration_home', name='integration_home'),
    url(r'^travel/edit/(?P<id>\d+)/$', 'edit_travel', name='edit_travel'),
    url(r'^travel/view/(?P<id>\d+)/$', 'view_travel', name='view_travel'),
    url(r'^travel/pdf/(?P<id>\d+)/$', 'travel_report', name='travel_report'),
    # Integrations
    url(r'^api/(?P<case_id>[0-9A-Za-z_\-{32}\Z]+)/$',
        'process_integration', name='process_integration'),
    url(r'^doc/(?P<doc_id>\d+)/(?P<case_id>[0-9A-Za-z_\-{32}\Z]+)/$',
        'get_document', name='get_document'),
    url(r'^dq/$', 'dq_home', name='dq_home'),
    url(r'^se/$', 'se_home', name='se_home'),
    url(r'^sedata/$', 'se_data', name='se_data'),
    # DQA
    url(r'^dq/$', 'dq_home', name='dq_home'),
    url(r'^dqdata/$', 'dq_data', name='dq_data'),
)
