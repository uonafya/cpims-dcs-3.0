"""API urls."""
from django.urls import include, path, re_path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
router.register(r'country', views.CountryViewSet, basename='Country')
# Wire up our API using automatic URL routing.
urlpatterns = [
    re_path(r'^', include(router.urls)),
    path('settings/', views.SettingsViewSet.as_view()),
    path('geo/', views.GeoViewSet.as_view()),
    path('ou/', views.OrgUnitViewSet.as_view()),
    path('crs-old/', views.BasicCRSView.as_view()),
    path('crs/', views.basic_crs),
    path('lookup/', views.get_settings, name='settings_lookup'),
]
