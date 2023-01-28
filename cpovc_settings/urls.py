"""Urls for Settings."""
from django.urls import path, re_path

from . import views

# This should contain urls related to settings ONLY
urlpatterns = [
    # url(r'^$', 'settings_home', name='settings_home'),
    re_path(
        r'^reports/d/(?P<file_name>[0-9_\-_A-Za-z_\._\(_\)_A-Za-z ]+)$',
        views.archived_reports, name='archived_reports'),
    re_path(
        r'^reports/r/(?P<file_name>[0-9_\-_A-Za-z_\._\(_\)_A-Za-z ]+)$',
        views.remove_reports, name='remove_reports'),
    path('reports/', views.settings_reports, name='settings_reports'),
    path('duplicates/', views.settings_duplicates, name='settings_duplicates'),
    path('facilities/', views.settings_facilities, name='settings_facilities'),
    path('schools/', views.settings_schools, name='settings_schools'),
    path('data/', views.settings_rawdata, name='settings_rawdata'),
    path('changes/', views.change_notes, name='change_notes'),
]
