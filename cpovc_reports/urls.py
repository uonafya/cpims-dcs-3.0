from django.urls import path # conf.urls removed
from cpovc_reports.views import (
    reports_home, reports_home, cpims_document, reports_cpims, reports_caseload, manage_reports,
    manage_dashboard, reports_download, print_pdf, reports_generate, reports_pivot, reports_rawdata,
    reports_ovc_pivot, reports_ovc_pepfar, reports_ovc_kpi, reports_ovc_rawdata, reports_ovc_download,
    reports_ovc, dashboard_details, cluster, get_docs
)

# changed to latest 4.2.0 paths

urlpatterns = [
    path(r'^$', reports_home, name='reports'),
    path(r'^documents/$', reports_home,
        name='document_reports'),
    path(r'^documents/(?P<doc_id>[A-Z{3}\Z]+)/(?P<case_id>[0-9A-Za-z_\-{32}\Z]+)/$', cpims_document,
        name='cpims_document'),
    path(r'^(?P<id>\d+)/$', reports_cpims,
        name='cpims_reports'),
    path(r'^caseload/$', reports_caseload,
        name='caseload_reports'),
    path(r'^manage/$', manage_reports,
        name='manage_reports'),
    path(r'^dashboard/$', manage_dashboard,
        name='manage_dashboard'),
    path(r'^download/(?P<file_name>[0-9A-Za-z_\.=\-\(\)\' ]+)$',
        reports_download, name='download_reports'),
    path(r'^pdf/(?P<file_name>[0-9A-Za-z_\.=\-\(\)\' ]+)$', print_pdf, name='print_pdf'),
    path(r'^generate/$', reports_generate,
        name='generate_reports'),
    path(r'^pivot/$', reports_pivot,
        name='pivot_reports'),
    path(r'^data/$', reports_rawdata,
        name='pivot_rawdata'),
    path(r'^datim/$', reports_ovc_pivot,
        name='pivot_ovc_reports'),
    path(r'^pepfar/$', reports_ovc_pepfar,
        name='pivot_ovc_pepfar'),
    path(r'^kpi/$', reports_ovc_kpi,
        name='pivot_ovc_kpi'),
    path(r'^ovcdata/$', reports_ovc_rawdata,
        name='pivot_ovc_rawdata'),
    path(r'^download/$', reports_ovc_download,
        name='ovc_download'),
    path(r'^ovc/(?P<id>\d+)/$', reports_ovc,
        name='reports_ovc'),
    path(r'^dashboard/data/$', dashboard_details,
        name='dashboard_details'),
    path(r'^cluster/$', cluster,
        name='cluster'),
    path(r'^docs/(?P<id>\d+)/$', get_docs,
        name='get_docs')
]

# ----------------------------------------------------------#