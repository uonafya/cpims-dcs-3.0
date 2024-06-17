"""API urls."""
from django.urls import include, path, re_path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()

router.register(r'country', views.CountryViewSet, basename='Country')

urlpatterns = [
    re_path(r'^', include(router.urls)),
    path('settings/', views.SettingsViewSet.as_view()),
    path('geo/', views.GeoViewSet.as_view()),
    path('ou/', views.OrgUnitViewSet.as_view()),
    path('school/', views.SchoolViewSet.as_view()),
    path('health_facility/', views.HealthFacilityViewSet.as_view()),
    # path('crs-old/', views.BasicCRSView.as_view()),
    path('crs/', views.basic_crs),
    path('lookup/', views.get_settings, name='settings_lookup'),
    path('dreams/', views.dreams),  
]
