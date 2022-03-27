from django.urls import re_path
from . import views
# This should contain urls related to Dashboards ONLY

g_params = "(?P<rid>\w+)/(?P<county_id>\d+)/(?P<const_id>\d+)/(?P<ward_id>\d+)"
i_params = "(?P<ip_id>\d+)/(?P<lip_id>\d+)"
d_params = "(?P<prd>\d+)/(?P<yr>\d+)"

urlpatterns = [
    # 'cpovc_dashboard.views',
    # Geo Settings
    re_path(r'^constituency/(?P<area_id>\d+)/', views.get_constituency, name='get_constituency'),
    re_path(r'^ward/(?P<area_id>\d+)/', views.get_ward, name='get_ward'),
    re_path(r'^lip/(?P<ip_id>\d+)/', views.get_lip, name='get_lip'),
    re_path(r'^%s/%s/%s/' % (g_params, i_params, d_params), views.get_chart),
    # county_id, const_id, ward_id, ip, lip
]
