"""API urls."""
from django.conf.urls import include
from django.urls import path, re_path
from rest_framework import routers
from .views import (
    SettingsViewSet, GeoViewSet, BasicCRSView, CountryViewSet,
    basic_crs, OrgUnitViewSet, OVCCaseRecordViewSet, OVCCaseCategoryViewSet)

router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'country', CountryViewSet, base_name='Country')
# Wire up our API using automatic URL routing.
# router.register(r'country', CountryViewSet)


urlpatterns = {
    re_path(r'^', include(router.urls)),
    re_path(r'^settings/$', SettingsViewSet.as_view()),
    re_path(r'^geo/$', GeoViewSet.as_view()),
    re_path(r'^ou/$', OrgUnitViewSet.as_view()),
    re_path(r'^crs-old/$', BasicCRSView.as_view()),
    re_path(r'^crs/$', basic_crs),
    re_path(r'OVCCaseRecord/$', OVCCaseRecordViewSet.as_view()),
    re_path('ovccasecategories/', OVCCaseCategoryViewSet.as_view({"post": "create", "get": "list", })),
    path('single-ovccasecategory/<uuid:pk>/', OVCCaseCategoryViewSet.as_view(
        {"put": "update", "delete": "destroy", "get": "retrieve", }), ),
}
