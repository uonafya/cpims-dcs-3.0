"""Urls for Settings."""
from django.urls import path, re_path

from . import views

# This should contain urls related to settings ONLY
urlpatterns = [
    path('', views.manage_home, name='manage_home'),
    path('travel/', views.home_travel, name='home_travel'),
    path('integration/', views.integration_home, name='integration_home'),
    path('travel/edit/<int:id>/', views.edit_travel, name='edit_travel'),
    path('travel/view/<int:id>/', views.view_travel, name='view_travel'),
    path('travel/pdf/<int:id>/', views.travel_report, name='travel_report'),
    # Integrations
    path(
        'api/<uuid:case_id>/',
        views.process_integration, name='process_integration'),
    re_path(
        r'^doc/(?P<doc_id>\d+)/(?P<case_id>[0-9A-Za-z_\-{32}]+)/$',
        views.get_document, name='get_document'),
    path('dq/', views.dq_home, name='dq_home'),
    path('se/', views.se_home, name='se_home'),
    path('sedata/', views.se_data, name='se_data'),
    # DQA
    path('dq/', views.dq_home, name='dq_home'),
    path('dqdata/', views.dq_data, name='dq_data'),
    # Bug reporting
    path('bugs/', views.manage_bugs, name='manage_bugs'),
]
