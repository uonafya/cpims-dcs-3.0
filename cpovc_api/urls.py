"""API urls."""
from django.conf.urls import url, include
from rest_framework import routers
from .views import (
    SettingsViewSet, GeoViewSet, BasicCRSView, CountryViewSet,
    basic_crs, OrgUnitViewSet)

router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
router.register(r'country', CountryViewSet, base_name='Country')
# Wire up our API using automatic URL routing.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^settings/$', SettingsViewSet.as_view()),
    url(r'^geo/$', GeoViewSet.as_view()),
    url(r'^ou/$', OrgUnitViewSet.as_view()),
    url(r'^crs-old/$', BasicCRSView.as_view()),
    url(r'^crs/$', basic_crs),
]
