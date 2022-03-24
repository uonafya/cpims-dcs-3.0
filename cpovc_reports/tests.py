import pandas as pd
from django.test import TestCase
from django.urls import reverse, resolve
from cpovc_reports import views


# urls tests
class Testurls(TestCase):

    def test_report_home_urls(self):
        url = reverse('reports')
        self.assertEqual(resolve(url).func, views.reports_home)
    def test_report_document_reports_urls(self):
        url = reverse('documents')
        self.assertEqual(resolve(url).func, views.reports_home)
    def test_report_cpims_urls(self):
        url = reverse('cpims_reports')
        self.assertEqual(resolve(url).func, views.reports_cpims)
    def test_report_caseload_urls(self):
        url = reverse('caseload_reports')
        self.assertEqual(resolve(url).func, views.reports_caseload)
    def test_report_reports_urls(self):
        url = reverse('reports')
        self.assertEqual(resolve(url).func, views.reports_home)
    def test_report_manage_urls(self):
        url = reverse('manage')
        self.assertEqual(resolve(url).func, views.manage_reports)
    def test_report_dashboard_urls(self):
        url = reverse('dashboard')
        self.assertEqual(resolve(url).func, views.manage_dashboard)
    def test_report_generate_urls(self):
        url = reverse('generate')
        self.assertEqual(resolve(url).func, views.reports_generate)
    def test_report_datim_urls(self):
        url = reverse('pivot_ovc_reports')
        self.assertEqual(resolve(url).func, views.reports_ovc_pivot)
    def test_report_pivot_urls(self):
        url = reverse('pivot')
        self.assertEqual(resolve(url).func, views.reports_pivot)
    def test_report_data_urls(self):
        url = reverse('pivot_rawdata')
        self.assertEqual(resolve(url).func, views.reports_rawdata)
    def test_report_pepfar_urls(self):
        url = reverse('pivot_ovc_pepfar')
        self.assertEqual(resolve(url).func, views.reports_ovc_pepfar)
    def test_report_kpi_urls(self):
        url = reverse('kpi')
        self.assertEqual(resolve(url).func, views.reports_ovc_kpi)
    def test_report_ovcdata_urls(self):
        url = reverse('ovcdata')
        self.assertEqual(resolve(url).func, views.reports_ovc_rawdata)
    def test_report_download_urls(self):
        url = reverse('download')
        self.assertEqual(resolve(url).func, views.reports_ovc_download)
    def test_report_dashboard_data_urls(self):
        url = reverse('dashboard/data')
        self.assertEqual(resolve(url).func, views.dashboard_details)
    def test_report_cluster_urls(self):
        url = reverse('cluster')
        self.assertEqual(resolve(url).func, views.cluster)
    
    
    