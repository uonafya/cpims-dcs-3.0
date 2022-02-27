"""Urls for Settings."""
from django.urls import include, path

# This should contain urls related to settings ONLY
urlpatterns = include(
    'cpovc_settings.views',
    # path(r'^$', 'settings_home', name='settings_home'),
    path(r'^reports/d/(?P<file_name>[0-9_\-_A-Za-z_\._A-Za-z]+)$',
        'archived_reports', name='archived_reports'),
    path(r'^reports/r/(?P<file_name>[0-9_\-_A-Za-z_\._A-Za-z]+)$',
        'remove_reports', name='remove_reports'),
    path(r'^reports/$', 'settings_reports', name='settings_reports'),
    path(r'^duplicates/$', 'settings_duplicates', name='settings_duplicates'),
    path(r'^facilities/$', 'settings_facilities', name='settings_facilities'),
    path(r'^schools/$', 'settings_schools', name='settings_schools'),
    path(r'^data/$', 'settings_rawdata', name='settings_rawdata'),
    path(r'^changes/$', 'change_notes', name='change_notes'),
)
