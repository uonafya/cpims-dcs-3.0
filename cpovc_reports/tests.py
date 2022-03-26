import pandas as pd
from django.test import TestCase, Client
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

    # views test


class Testviews(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.forms_url = reverse('reports')
        self.document_manager_url = reverse('documents')
        return super().setUp()
    #models test
from django.test import TestCase

import pandas as pd
from django.test import TestCase, Client
from django.urls import reverse, resolve
from .models import RPTCaseLoad, RPTIPopulation

class RPTCaseLoadTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        RPTCaseLoad.objects.create(first_name='Big', last_name='Bob')

    def test_case_serial_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('case_serial').verbose_name
        self.assertEqual(field_label, 'case serial')

    def test_case_serial_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('case_serial').max_length
        self.assertEqual(max_length, 40)

    def test_case_reporter_id_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('case_reporter_id').verbose_name
        self.assertEqual(field_label, 'case reporter id')

    def test_case_reporter_id_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('case_reporter_id').max_length
        self.assertEqual(max_length, 4)

    def test_case_reporter_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('case_reporter').verbose_name
        self.assertEqual(field_label, 'case reporter')

    def test_case_reporter_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('case_reporter').max_length
        self.assertEqual(max_length, 250)

    def test_case_perpetrator_id_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('case_perpetrator_id').verbose_name
        self.assertEqual(field_label, 'case perpetrator id')

    def test_case_perpetrator_id_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('case_perpetrator_id').max_length
        self.assertEqual(max_length, 4)

    def test_case_perpetrator_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('case_perpetrator').verbose_name
        self.assertEqual(field_label, 'case perpetrator')

    def test_case_perpetrator_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('case_perpetrator_max').max_length
        self.assertEqual(max_length, 250)

    def test_case_category_id_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('case_category_id').verbose_name
        self.assertEqual(field_label, 'case category id')

    def test_case_category_id_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('case_category_id').max_length
        self.assertEqual(max_length, 4)

    def test_case_category_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('case_category').verbose_name
        self.assertEqual(field_label, 'case category')

    def test_case_category_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('case_category').max_length
        self.assertEqual(max_length, 250)

    def test_place_of_event_id_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('place_of_event_id').verbose_name
        self.assertEqual(field_label, 'place of event id')

    def test_place_of_event_id_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('place_of_event_id').max_length
        self.assertEqual(max_length, 4)

    def test_place_of_event_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('place_of_event').verbose_name
        self.assertEqual(field_label, 'place of event')

    def test_place_of_event_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('place_of_event').max_length
        self.assertEqual(max_length, 250)

    def test_sex_id_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('sex_id').verbose_name
        self.assertEqual(field_label, 'sex id')

    def test_sex_id_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('sex_id').max_length
        self.assertEqual(max_length, 4)

    def test_sex_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('sex').verbose_name
        self.assertEqual(field_label, 'sex')

    def test_sex_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('sex').max_length
        self.assertEqual(max_length, 10)

    def test_county_id_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('county_id').verbose_name
        self.assertEqual(field_label, 'county id')

    def test_county_id_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('county_id').max_length
        self.assertEqual(max_length, 0)

    def test_county_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('county').verbose_name
        self.assertEqual(field_label, 'county')

    def test_county_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('county').max_length
        self.assertEqual(max_length, 250)

    def test_sub_county_id_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('sub_county_id').verbose_name
        self.assertEqual(field_label, 'sub_county_id')

    def test_sub_county_id_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('sub_county_id').max_length
        self.assertEqual(max_length, 0)

    def test_sub_county_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('sub_county').verbose_name
        self.assertEqual(field_label, 'sub_county')

    def test_sub_county_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('sub_county').max_length
        self.assertEqual(max_length, 250)

    def test_org_unit_name_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('org_unit_name').verbose_name
        self.assertEqual(field_label, 'org unit name')

    def test_org_unit_name_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('org_unit_name').max_length
        self.assertEqual(max_length, 250)

    def test_intervention_id_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('intervention_id').verbose_name
        self.assertEqual(field_label, 'intervention id')

    def test_intervention_id_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('intervention_id').max_length
        self.assertEqual(max_length, 4)

    def test_intervention_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('intervention').verbose_name
        self.assertEqual(field_label, 'intervention')

    def test_intervention_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('intervention').max_length
        self.assertEqual(max_length, 250)

    def test_case_year_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('case_year').verbose_name
        self.assertEqual(field_label, 'case year')

    def test_case_year_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('case_year').max_length
        self.assertEqual(max_length, 0)

    def test_case_month_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('case_month').verbose_name
        self.assertEqual(field_label, 'case month')

    def test_case_month_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('case_month').max_length
        self.assertEqual(max_length, 0)

    def test_case_quota_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('case_quota').verbose_name
        self.assertEqual(field_label, 'case quota')

    def test_case_quota_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('case_quota').max_length
        self.assertEqual(max_length, 0)

    def test_case_count_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('case_count').verbose_name
        self.assertEqual(field_label, 'case count')

    def test_case_count_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('case_count').max_length
        self.assertEqual(max_length, 1)

    def test_age_range_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('age_range').verbose_name
        self.assertEqual(field_label, 'age range')

    def test_age_range_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('age_range').max_length
        self.assertEqual(max_length, 20)

    def test_knbs_age_range_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('knbs_age_range').verbose_name
        self.assertEqual(field_label, 'knbs age range')

    def test_knbs_age_range_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('knbs_age_range').max_length
        self.assertEqual(max_length, 20)

    def test_age_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('age').verbose_name
        self.assertEqual(field_label, 'age')

    def test_age_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('age').max_length
        self.assertEqual(max_length, 0)

class RPTIPopulation(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        RPTIPopulation.objects.create(first_name='Big', last_name='Bob')

    def test_case_serial_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('case_serial').verbose_name
        self.assertEqual(field_label, 'case serial')

    def test_case_serial_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('case_serial').max_length
        self.assertEqual(max_length, 40)

    def test_admission_number_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('admission_number').verbose_name
        self.assertEqual(field_label, 'admission number')

    def test_admission_number_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('admission_number').max_length
        self.assertEqual(max_length, 40)

    def test_org_unit_name_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('org_unit_name').verbose_name
        self.assertEqual(field_label, 'org unit name')

    def test_org_unit_name_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('org_unit_name').max_length
        self.assertEqual(max_length, 250)

    def test_org_unit_type_id_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('org_unit_type_id').verbose_name
        self.assertEqual(field_label, 'org unit type id')

    def test_org_unit_type_id_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('org_unit_type_id').max_length
        self.assertEqual(max_length, 4)

    def test_sex_id_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('sex_id').verbose_name
        self.assertEqual(field_label, 'sex id')

    def test_sex_id_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('sex_id').max_length
        self.assertEqual(max_length, 4)

    def test_sex_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('sex').verbose_name
        self.assertEqual(field_label, 'sex')

    def test_sex_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('sex').max_length
        self.assertEqual(max_length, 10)

    def test_age_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('age').verbose_name
        self.assertEqual(field_label, 'age')

    def test_age_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('age').max_length
        self.assertEqual(max_length, 0)

    def test_age_now_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('age_now').verbose_name
        self.assertEqual(field_label, 'age now')

    def test_age_now_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('age_now').max_length
        self.assertEqual(max_length, 0)

    def test_age_range_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('age_range').verbose_name
        self.assertEqual(field_label, 'age range')

    def test_age_range_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('age_range').max_length
        self.assertEqual(max_length, 20)

    def test_knbs_age_range_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('knbs_age_range').verbose_name
        self.assertEqual(field_label, 'knbs age range')

    def test_knbs_age_range_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('knbs_age_range').max_length
        self.assertEqual(max_length, 20)

    def test_county_clabel(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('county').verbose_name
        self.assertEqual(field_label, 'county')

    def test_county_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('county').max_length
        self.assertEqual(max_length, 250)

    def test_admission_type_id_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('admission_type_id').verbose_name
        self.assertEqual(field_label, 'admission type id')

    def test_admission_type_id_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('admission_type_id').max_length
        self.assertEqual(max_length, 4)

    def test_admission_type_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('admission_type').verbose_name
        self.assertEqual(field_label, 'admission type')

    def test_admission_type_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('admission_type').max_length
        self.assertEqual(max_length, 0)

    def test_admission_reason_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('admission_reason').verbose_name
        self.assertEqual(field_label, 'admission reason')

    def test_admission_reason_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('admission_reason').max_length
        self.assertEqual(max_length, 4)

    def test_case_status_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('case_status').verbose_name
        self.assertEqual(field_label, 'case status')

    def test_case_status_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('case_status').max_length
        self.assertEqual(max_length, 20)

    def test_case_category_id_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('case_category_id').verbose_name
        self.assertEqual(field_label, 'case category id')

    def test_case_category_id_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('case_category_id').max_length
        self.assertEqual(max_length, 4)

    def test_case_category_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('case_category').verbose_name
        self.assertEqual(field_label, 'case category')

    def test_case_category_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('case_category').max_length
        self.assertEqual(max_length, 250)

    def test_sub_category_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('sub_category').verbose_name
        self.assertEqual(field_label, 'sub category')

    def test_sub_category_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('sub_category').max_length
        self.assertEqual(max_length, 250)

    def test_county_id_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('county_id').verbose_name
        self.assertEqual(field_label, 'county id')

    def test_county_id_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('county_id').max_length
        self.assertEqual(max_length, 0)

    def test_discharge_type_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('discharge_type').verbose_name
        self.assertEqual(field_label, 'discharge type')

    def test_discharge_type_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('discharge_type').max_length
        self.assertEqual(max_length, 250)

    def test_sub_county_id_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('sub_county_id').verbose_name
        self.assertEqual(field_label, 'sub county id')

    def test_sub_county_id_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('sub_county_id').max_length
        self.assertEqual(max_length, 250)

    def test_sub_county_label(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        field_label = caseload._meta.get_field('sub_county').verbose_name
        self.assertEqual(field_label, 'sub county')

    def test_sub_county_max_length(self):
        caseload = RPTCaseLoad.objects.get(id=1)
        max_length = caseload._meta.get_field('sub_county').max_length
        self.assertEqual(max_length, 0)    
