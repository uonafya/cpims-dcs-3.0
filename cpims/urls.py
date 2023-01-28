"""
cpims URL Configuration.

Other urls are import
Put here only urls not specific to app
"""
from . import views
import cpovc_auth
import cpovc_access
from django.urls import include, path, re_path
from django.contrib import admin
from cpovc_auth import urls as auth_urls
from cpovc_registry import urls as registry_urls
from cpovc_registry import views as registry_views

from cpovc_forms import urls as forms_urls
from cpovc_reports import urls as reports_urls
from cpovc_gis import urls as gis_urls
from cpovc_api import urls as api_urls
from cpovc_ovc import urls as ovc_urls
from cpovc_settings import urls as settings_urls
from cpovc_manage import urls as manage_urls
from cpovc_help import urls as help_urls
from notifications import urls as noti_urls
from cpovc_ctip import urls as ctip_urls
from cpovc_afc import urls as ac_urls

from django.views.generic import TemplateView
# For dashboard
from cpovc_dashboard import urls as dashboard_api_urls
from cpovc_dashboard import views as dash_views


urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r'^$', 'cpovc_auth.views.log_in', name='home'),
    path('', views.home, name='home'),
    path('accounts/request/', views.access, name='access'),
    path('accounts/terms/<int:id>/', cpovc_access.views.terms,
         name='terms'),
    path('register/', cpovc_auth.views.register, name='register'),
    path('auth/', include(auth_urls)),
    path('registry/', include(registry_urls)),
    path('forms/', include(forms_urls)),
    path('reports/', include(reports_urls)),
    path('gis/', include(gis_urls)),
    path('api/v1/', include(api_urls)),
    path('ovc_care/', include(ovc_urls)),
    path('settings/', include(settings_urls)),
    path('manage/', include(manage_urls)),
    path('help/', include(help_urls)),
    path('forms/ctip/', include(ctip_urls)),
    path('forms/altcare/', include(ac_urls)),
    path('notifications/', include(noti_urls, namespace='notifications')),
    re_path(r'^dashboard/(?P<did>[A-Z{2}]+)/$',
            registry_views.dashboard, name='dashboard'),
    # Accounts management
    path('accounts/', include(cpovc_auth.urls)),
    # Override Login and Logout not to use the /accounts/*
    path('login/', cpovc_auth.views.log_in, name='login'),
    path('logout/', cpovc_auth.views.log_out, name='logout'),
    path('d/', dash_views.ovc_dashboard, name='ovc_dashboard'),
    re_path(r'^api/v2/', include(dashboard_api_urls)),
    re_path(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt',
                                                   content_type='text/plain'))]

handler400 = 'cpims.views.handler_400'
handler404 = 'cpims.views.handler_404'
handler500 = 'cpims.views.handler_500'

admin.site.site_header = 'CPIMS Administration'
admin.site.site_title = 'CPIMS administration'
admin.site.index_title = 'CPIMS admin'
