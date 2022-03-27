"""Urls for GIS."""
from django.urls import re_path
from . import views
# This should contain urls related to GIS Module ONLY
urlpatterns = [
    # 'cpovc_gis.views',
    re_path(r'^$', views.gis_home, name='gis_home'),
    re_path(r'^data/$', views.gis_data, name='gis_data'),
    ]
