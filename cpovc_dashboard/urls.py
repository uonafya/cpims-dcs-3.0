from django.conf.urls import patterns, url

# This should contain urls related to Dashboards ONLY

g_params = "(?P<rid>\w+)/(?P<county_id>\d+)/(?P<const_id>\d+)/(?P<ward_id>\d+)"
i_params = "(?P<ip_id>\d+)/(?P<lip_id>\d+)"
d_params = "(?P<prd>\d+)/(?P<yr>\d+)"

urlpatterns = patterns(
    'cpovc_dashboard.views',
    # Geo Settings
    url(r'^constituency/(?P<area_id>\d+)/',
        'get_constituency', name='get_constituency'),
    url(r'^ward/(?P<area_id>\d+)/', 'get_ward', name='get_ward'),
    url(r'^lip/(?P<ip_id>\d+)/', 'get_lip', name='get_lip'),
    url(r'^%s/%s/%s/' % (g_params, i_params, d_params), 'get_chart'),
    # county_id, const_id, ward_id, ip, lip
)
