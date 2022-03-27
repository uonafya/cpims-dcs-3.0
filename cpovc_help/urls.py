"""Urls for Settings."""
from django.urls import re_path
from . import views

# This should contain urls related to settings ONLY
urlpatterns = [
    # 'cpovc_help.views',
    re_path(r'^downloads/$', views.help_downloads, name='help_downloads'),
    re_path(r'^download/(?P<name>[0-9A-Za-z_\-\.]+)$', views.doc_download, name='doc_download'),
    re_path(r'^faq/$', views.help_faq, name='help_faq'),
]