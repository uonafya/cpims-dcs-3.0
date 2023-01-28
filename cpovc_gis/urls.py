"""Urls for GIS."""
from django.urls import path
from . import views

# This should contain urls related to GIS Module ONLY
urlpatterns = [
    path('', views.gis_home, name='gis_home'),
    path('data/', views.gis_data, name='gis_data'),
]
