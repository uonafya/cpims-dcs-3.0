"""Urls for Settings."""
from django.urls import path, re_path

from . import views

# This should contain urls related to settings ONLY
urlpatterns = [
    path('downloads/', views.help_downloads, name='help_downloads'),
    re_path(
        r'^download/(?P<name>[0-9A-Za-z_\-\.]+)$',
        views.doc_download, name='doc_download'),
    path('faq/', views.help_faq, name='help_faq'),
]