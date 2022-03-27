"""Urls for reports."""
from django.urls import re_path
from . import views
# This should contain urls related to reports ONLY
urlpatterns = [
    # 'cpovc_reports.views',
    re_path(r'^$', views.reports_home, name='reports'),
    re_path(r'^documents/$', views.reports_home, name='document_reports'),
    re_path(r'^documents/(?P<doc_id>[A-Z{3}\\Z]+)/(?P<case_id>[0-9A-Za-z_\-{32}\\Z]+)/$', views.cpims_document, name='cpims_document'),
    re_path(r'^(?P<id>\d+)/$', views.reports_cpims, name='cpims_reports'),
    re_path(r'^caseload/$', views.reports_caseload, name='caseload_reports'),
    re_path(r'^manage/$', views.manage_reports, name='manage_reports'),
    re_path(r'^dashboard/$', views.manage_dashboard, name='manage_dashboard'),
    re_path(r'^download/(?P<file_name>[0-9A-Za-z_\.=\-\(\)\' ]+)$', views.reports_download, name='download_reports'),
    re_path(r'^pdf/(?P<file_name>[0-9A-Za-z_\.=\-\(\)\' ]+)$', views.print_pdf, name='print_pdf'),
    re_path(r'^generate/$', views.reports_generate, name='generate_reports'),
    re_path(r'^pivot/$', views.reports_pivot, name='pivot_reports'),
    re_path(r'^data/$', views.reports_rawdata, name='pivot_rawdata'),
    re_path(r'^datim/$', views.reports_ovc_pivot, name='pivot_ovc_reports'),
    re_path(r'^pepfar/$', views.reports_ovc_pepfar, name='pivot_ovc_pepfar'),
    re_path(r'^kpi/$', views.reports_ovc_kpi, name='pivot_ovc_kpi'),
    re_path(r'^ovcdata/$', views.reports_ovc_rawdata, name='pivot_ovc_rawdata'),
    re_path(r'^download/$', views.reports_ovc_download, name='ovc_download'),
    re_path(r'^ovc/(?P<id>\d+)/$', views.reports_ovc, name='reports_ovc'),
    re_path(r'^dashboard/data/$', views.dashboard_details, name='dashboard_details'),
    re_path(r'^cluster/$', views.cluster, name='cluster'),
    re_path(r'^docs/(?P<id>\d+)/$', views.get_docs, name='get_docs'),
]