from django.urls import path
from . import views
# This should contain urls related to OVC ONLY

urlpatterns = [
    path('', views.ovc_home, name='ovc_home'),
    path('ovc/search/', views.ovc_search, name='ovc_search'),
    path('ovc/new/<int:id>/', views.ovc_register, name='ovc_register'),
    path('ovc/edit/<int:id>/', views.ovc_edit, name='ovc_edit'),
    path('ovc/view/<int:id>/', views.ovc_view, name='ovc_view'),
    path('ovc/manage/', views.ovc_manage, name='ovc_manage'),
    path('hh/view/<uuid:hhid>/', views.hh_manage, name='hh_manage'),
    path('hh/edit/<uuid:hhid>/<int:id>/', views.hh_edit, name='hh_edit'),
]
