from django.urls import path, re_path
from . import views

fm = '(?P<form_id>[0-9A-Z]{8})/(?P<id>[0-9]+)/(?P<ev_id>[0-9A-Za-z_\\-{32}]+)/'
urlpatterns = [
    path('', views.cci_home, name='cci_home'),
    path('view/<int:id>/', views.cci_child_view, name='new_cci_child_view'),
    re_path('(?P<form_id>[0-9A-Z]{8})/(?P<id>[0-9]+)/$',
            views.cci_forms, name='cci_form'),
    re_path(fm, views.cci_forms_edit, name='cci_form_edit'),
    path('delete/', views.cci_forms_delete, name='cci_form_delete'),
    path('action/', views.cci_forms_action, name='cci_form_action'),
    # Dahsboards
    path('dashboard/<int:id>/', views.cci_dash_view, name='cci_dash_view'),
    ]