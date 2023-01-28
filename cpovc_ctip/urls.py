from django.urls import path, re_path
from . import views

# This should contain urls related to CTiP ONLY
urlpatterns = [
    path('', views.ctip_home, name='ctip_home'),
    re_path(r'^case/(?P<case_id>[0-9A-Za-z_\-{32}]+)/$', views.view_ctip_case, name='view_ctip_case'),
    re_path(r'^form/(?P<form_id>[A-Z{1}]+)/(?P<case_id>[0-9A-Za-z_\-{32}]+)/(?P<id>\d+)/$',
            views.ctip_forms, name='ctip_forms'),
    re_path(r'^form/(?P<form_id>[A-Z{1}]+)/(?P<case_id>[0-9A-Za-z_\-{32}]+)/$',
            views.ctip_form, name='ctip_form'),
    re_path(r'^form/view/(?P<form_id>[A-Z{1}]+)/(?P<case_id>[0-9A-Za-z_\-{32}]+)/$',
            views.view_ctip_form, name='view_ctip_form'),
    path('new/<uuid:case_id>/', views.new_ctip_case, name='new_ctip_case'),
    path('edit/<uuid:case_id>/', views.edit_ctip_case, name='edit_ctip_case'),
]
