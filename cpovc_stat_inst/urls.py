from django.urls import path, re_path
from . import views

# This should contain urls related to Institution module ONLY
fm = '(?P<form_id>[0-9A-Z]{8})/(?P<id>[0-9]+)/(?P<ev_id>[0-9A-Za-z_\\-{32}]+)/'
urlpatterns = [
    path('', views.si_home, name='SI_home'),
    # path('new/<uuid:case_id>/', views.SI_admissions, name='new_si_admit'),

    path('view/<int:id>/', views.SI_child_view, name='new_si_child_view'),

    # New Forms from August
    re_path('(?P<form_id>[0-9A-Z]{8})/(?P<id>[0-9]+)/$',
            views.si_forms, name='si_form'),
    re_path(fm, views.si_forms_edit, name='si_form_edit'),
    path('delete/', views.si_forms_delete, name='si_form_delete'),
    path('action/', views.si_forms_action, name='si_form_action'),
    re_path(
        'document/(?P<form_id>[0-9A-Z]{8})/',
        views.si_document, name='si_document'),
    path('doc/<uuid:event_id>/', views.si_file, name='si_file'),

    # Dahsboards
    path('dashboard/<int:id>/', views.SI_dash_view, name='si_dash_view'),
]
