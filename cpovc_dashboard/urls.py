from django.urls import include, path

# This should contain urls related to Dashboards ONLY

g_params = "(?P<rid>\w+)/(?P<county_id>\d+)/(?P<const_id>\d+)/(?P<ward_id>\d+)"
i_params = "(?P<ip_id>\d+)/(?P<lip_id>\d+)"
d_params = "(?P<prd>\d+)/(?P<yr>\d+)"

urlpatterns = include(
    'cpovc_dashboard.views',
    # Geo Settings
    path(r'^constituency/(?P<area_id>\d+)/',
        'get_constituency', name='get_constituency'),
    path(r'^ward/(?P<area_id>\d+)/', 'get_ward', name='get_ward'),
    path(r'^lip/(?P<ip_id>\d+)/', 'get_lip', name='get_lip'),
    path(r'^%s/%s/%s/' % (g_params, i_params, d_params), 'get_chart'),
    # county_id, const_id, ward_id, ip, lip
)
