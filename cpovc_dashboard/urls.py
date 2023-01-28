from django.urls import re_path
from . import views

# This should contain urls related to Dashboards ONLY

g_params = "(?P<rid>\w+)/(?P<county_id>\d+)/(?P<const_id>\d+)/(?P<ward_id>\d+)"
i_params = "(?P<ip_id>\d+)/(?P<lip_id>\d+)"
d_params = "(?P<prd>\d+)/(?P<yr>\d+)"

urlpatterns = [
    re_path('constituency/<int:area_id>/',
            views.get_constituency, name='get_constituency'),
    re_path('ward/<int:area_id>/', views.get_ward, name='get_ward'),
    re_path('lip/<int:ip_id>/', views.get_lip, name='get_lip'),
    re_path(
        r'^%s/%s/%s/' % (g_params, i_params, d_params),
        views.get_chart, name='get_chart'),
]
