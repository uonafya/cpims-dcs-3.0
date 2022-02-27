"""Urls for GIS."""

# This should contain urls related to GIS Module ONLY
from django.urls import path, include

urlpatterns = include(
    'cpovc_gis.views',
    path(r'^$', 'gis_home', name='gis_home'),
    path(r'^data/$', 'gis_data', name='gis_data'),)
