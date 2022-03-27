"""
cpims URL Configuration.

Other urls are import
Put here only urls not specific to app
"""
from django.conf.urls import include
from django.contrib import admin

import cpims
import cpovc_access
import cpovc_auth
import cpovc_dashboard
import cpovc_registry
from cpovc_auth import urls as auth_urls
from cpovc_registry import urls as registry_urls
from cpovc_forms import urls as forms_urls
from cpovc_reports import urls as reports_urls
from cpovc_gis import urls as gis_urls
from cpovc_api import urls as api_urls
from cpovc_ovc import urls as ovc_urls
from cpovc_settings import urls as settings_urls
from cpovc_manage import urls as manage_urls
from cpovc_help import urls as help_urls
from notifications import urls as noti_urls
# from django.contrib.auth.views import (
#     password_reset_done, password_change, password_change_done)
from cpovc_auth.views import password_reset
from django.views.generic import TemplateView
from cpovc_dashboard import urls as dashboard_api_urls
from cpovc_access.forms import StrictPasswordChangeForm
from django.urls import include, path, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    # re_path(r'^admin/', include(admin.site.urls), name='admin'),
    # url(r'^$', 'cpovc_auth.views.log_in', name='home'),
    re_path(r'^$', cpims.views.home, name='home'),
    re_path(r'^accounts/request/$', cpims.views.access, name='access'),
    re_path(r'^accounts/terms/(?P<id>\d+)/$', cpovc_access.views.terms,
            name='terms'),
    re_path(r'^login/$', cpovc_auth.views.log_in, name='login'),
    re_path(r'^logout/$', cpovc_auth.views.log_out, name='logout'),
    re_path(r'^register/$', cpovc_auth.views.register, name='register'),
    re_path(r'^auth/', include(auth_urls)),
    re_path(r'^registry/', include(registry_urls)),
    re_path(r'^forms/', include(forms_urls)),
    re_path(r'^reports/', include(reports_urls)),
    re_path(r'^gis/', include(gis_urls)),
    re_path(r'^api/v1/', include(api_urls)),
    re_path(r'^ovcare/', include(ovc_urls)),
    re_path(r'^settings/', include(settings_urls)),
    re_path(r'^manage/', include(manage_urls)),
    re_path(r'^help/', include(help_urls)),
    re_path(r'^notifications/', include(noti_urls, namespace='notifications')),
    re_path(r'^dashboard/(?P<did>[A-Z{2}\\Z]+)/$',
            cpovc_registry.views.dashboard, name='dashboard'),
    re_path(r'^accounts/login/$', cpovc_auth.views.log_in, name='login'),
    re_path(r'^accounts/password/reset/$', password_reset,
            {'template_name': 'registration/password_reset.html'},
            name='password_reset'),
    # re_path(r'^accounts/password/reset/done/$', password_reset_done,
    #     {'template_name': 'registration/password_reset_done.html'},
    #     name='password_reset_done'),
    re_path(r'^accounts/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
            cpovc_auth.views.reset_confirm, name='password_reset_confirm'),
    re_path(r'^reset/$', cpovc_auth.views.reset, name='reset'),
    # re_path(r'^accounts/password/change/$', password_change,
    #     {'post_change_redirect': '/accounts/password/change/done/',
    #      'template_name': 'registration/password_change.html',
    #      'password_change_form': StrictPasswordChangeForm},
    #     name='password_change'),
    # re_path(r'^accounts/password/change/done/$', password_change_done,
    #     {'template_name': 'registration/password_change_done.html'}),
    re_path(r'^F57665A859FE7CFCDB6C8935196374AD\.txt$',
            TemplateView.as_view(template_name='comodo.txt',
                                 content_type='text/plain')),
    re_path(r'^d/$', cpovc_dashboard.views.ovc_dashboard, name='ovc_dashboard'),
    re_path(r'^d/hivstat/', cpovc_dashboard.views.ovc_dashboard_hivstat, name='hivstat_dash'),
    re_path(r'^d/services/', cpovc_dashboard.views.ovc_dashboard_services, name='services_dash'),
    re_path(r'^d/cm/', cpovc_dashboard.views.ovc_dashboard_cm, name='cm_dash'),
    re_path(r'^api/v2/', include(dashboard_api_urls)),
    re_path(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt',
                                                   content_type='text/plain'))]

handler400 = 'cpims.views.handler_400'
handler404 = 'cpims.views.handler_404'
handler500 = 'cpims.views.handler_500'

admin.site.site_header = 'CPIMS Administration'
admin.site.site_title = 'CPIMS administration'
admin.site.index_title = 'CPIMS admin'
