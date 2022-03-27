"""Urls for Settings."""
from django.urls import re_path
from . import views

# This should contain urls related to settings ONLY
urlpatterns = [
    # 'cpovc_settings.views',
    # url(r'^$', views.settings_home, name='settings_home'),
    re_path(r'^reports/d/(?P<file_name>[0-9_\-_A-Za-z_\._A-Za-z]+)$', views.archived_reports, name='archived_reports'),
    re_path(r'^reports/r/(?P<file_name>[0-9_\-_A-Za-z_\._A-Za-z]+)$', views.remove_reports, name='remove_reports'),
    re_path(r'^reports/$', views.settings_reports, name='settings_reports'),
    re_path(r'^duplicates/$', views.settings_duplicates, name='settings_duplicates'),
    re_path(r'^facilities/$', views.settings_facilities, name='settings_facilities'),
    re_path(r'^schools/$', views.settings_schools, name='settings_schools'),
    re_path(r'^data/$', views.settings_rawdata, name='settings_rawdata'),
    re_path(r'^changes/$', views.change_notes, name='change_notes'),
]
