from django.urls import path, re_path
from . import views

# This should contain urls related to Care reforms ONLY
urlpatterns = [
    path('', views.alt_care_home, name='alternative_care'),
    path(
        'new/<uuid:case_id>/', views.new_alternative_care,
        name='new_alt_care'),
    path(
        'view/<uuid:care_id>/', views.view_alternative_care,
        name='view_alt_care'),
    path(
        'edit/<uuid:care_id>/', views.edit_alternative_care,
        name='edit_alt_care'),
    re_path(r'^(?P<cid>[A-Z{2}]+)/(?P<form_id>\d+[A-Z_\-{1}]+)/(?P<care_id>[0-9A-Za-z_\-{32}]+)/$',
            views.alt_care_form, name='alt_care_form'),
    re_path(r'^(?P<cid>[A-Z{2}]+)/(?P<form_id>\d+[A-Z_\-{1}]+)/(?P<care_id>[0-9A-Za-z_\-{32}]+)/(?P<ev_id>\d+)/$',
            views.edit_alt_care_form, name='edit_alt_care_form'),
    re_path(r'^(?P<form_id>\d+[A-Z_\-{1}]+)/(?P<event_id>[0-9A-Za-z_\-{32}]+)/$',
            views.delete_alt_care_form, name='delete_alt_care_form'),
]
