"""Urls for Settings."""
from django.urls import include, path

# This should contain urls related to settings ONLY
urlpatterns = include(
    'cpovc_help.views',
    path(r'^downloads/$', 'help_downloads', name='help_downloads'),
    path(r'^download/(?P<name>[0-9A-Za-z_\-\.]+)$', 'doc_download', name='doc_download'),
    path(r'^faq/$', 'help_faq', name='help_faq'),
)