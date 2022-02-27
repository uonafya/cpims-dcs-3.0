from django.urls import reverse, resolve

import views
from django.test import TestCase


# Create your tests here.

# Form home test
class ViewTests(TestCase):
    def test_home_form(self):
        response = self.client.get("forms/forms_home", {'person_type': 'TBVC'})
        self.assertEqual(response.status_code, 200)

    def test_form_registry(self):
        response = self.client.get("forms/forms_registry", {'form': {'placeholder': "CCO/XX/XXX/5/29/XX/YYYY",
                                                                     'class': 'form-control',
                                                                     'id': 'case_serial',
                                                                     'data-parsley-required': 'false'}})
        self.assertEqual(response.status_code, 200)


class TestViewUrl(TestCase):
    def test_home_form(self):
        result = reverse(views.forms_home)
        self.assertEqual(resolve(result).func, views.forms_home.func)

    def test_registry_form(self):
        result = reverse(views.forms_registry)
        self.assertEqual(resolve(result).func, views.forms_registry)

    def test_documents_manager_search(self):
        result = reverse(views.documents_manager_search)
        self.assertEqual(resolve(result).func, views.documents_manager_search)

    def test_documents_manager(self):
        result = reverse(views.documents_manager)
        self.assertEqual(resolve(result).func, views.documents_manager)

    def test_case_record_sheet(self):
        result = reverse(views.case_record_sheet)
        self.assertEqual(resolve(result).func, views.case_record_sheet)

    def test_edit_case_record_sheet(self):
        result = reverse(views.edit_case_record_sheet)
        self.assertEqual(resolve(result).func, views.edit_case_record_sheet)

    def test_view_case_record_sheet(self):
        result = reverse(views.view_case_record_sheet)
        self.assertEqual(resolve(result).func, views.view_case_record_sheet)

    def test_delete_case_record_sheet(self):
        result = reverse(views.delete_case_record_sheet)
        self.assertEqual(resolve(result).func, views.delete_case_record_sheet)

    def test_new_case_record_sheet(self):
        result = reverse(views.new_case_record_sheet)
        self.assertEqual(resolve(result).func, views.new_case_record_sheet)

    def test_residential_placement(self):
        result = reverse(views.residential_placement)
        self.assertEqual(resolve(result).func, views.residential_placement)

    def test_ovc_search(self):
        result = reverse(views.ovc_search)
        self.assertEqual(resolve(result).func, views.ovc_search)

    def test_alternative_family_care(self):
        result = reverse(views.alternative_family_care)
        self.assertEqual(resolve(result).func, views.alternative_family_care)

    def test_edit_alternative_family_care(self):
        result = reverse(views.edit_alternative_family_care)
        self.assertEqual(resolve(result).func, views.edit_alternative_family_care)

    def test_view_alternative_family_care(self):
        result = reverse(views.view_alternative_family_care)
        self.assertEqual(resolve(result).func, views.view_alternative_family_care)

    def test_case_events(self):
        result = reverse(views.case_events)
        self.assertEqual(resolve(result).func, views.case_events)

    def test_save_encounter(self):
        result = reverse(views.save_encounter)
        self.assertEqual(resolve(result).func, views.save_encounter)

    def test_view_encounter(self):
        result = reverse(views.view_encounter)
        self.assertEqual(resolve(result).func, views.view_encounter)

    def test_edit_encounter(self):
        result = reverse(views.edit_encounter)
        self.assertEqual(resolve(result).func, views.edit_encounter)

    def test_save_court(self):
        result = reverse(views.save_court)
        self.assertEqual(resolve(result).func, views.save_court)

    def test_view_court(self):
        result = reverse(views.view_court)
        self.assertEqual(resolve(result).func, views.view_court)

    def test_edit_court(self):
        result = reverse(views.edit_court)
        self.assertEqual(resolve(result).func, views.edit_court)

    def test_delete_court(self):
        result = reverse(views.delete_court)
        self.assertEqual(resolve(result).func, views.delete_court)

    def test_save_closure(self):
        result = reverse(views.save_closure)
        self.assertEqual(resolve(result).func, views.save_closure)

    def test_edit_closure(self):
        result = reverse(views.edit_closure)
        self.assertEqual(resolve(result).func, views.edit_closure)

    def test_view_closure(self):
        result = reverse(views.view_closure)
        self.assertEqual(resolve(result).func, views.view_closure)

    def test_delete_closure(self):
        result = reverse(views.delete_closure)
        self.assertEqual(resolve(result).func, views.delete_closure)

    def test_save_summon(self):
        result = reverse(views.save_summon)
        self.assertEqual(resolve(result).func, views.save_summon)

    def test_edit_summon(self):
        result = reverse(views.edit_summon)
        self.assertEqual(resolve(result).func, views.edit_summon)

    def test_view_summon(self):
        result = reverse(views.view_summon)
        self.assertEqual(resolve(result).func, views.view_summon)

    def test_delete_summon(self):
        result = reverse(views.delete_summon)
        self.assertEqual(resolve(result).func, views.delete_summon)

    def test_delete_referral(self):
        result = reverse(views.delete_referral)
        self.assertEqual(resolve(result).func, views.delete_referral)

    def test_placement(self):
        result = reverse(views.placement)
        self.assertEqual(resolve(result).func, views.placement)

    def test_placement_followup(self):
        result = reverse(views.placement_followup)
        self.assertEqual(resolve(result).func, views.placement_followup)

    def test_save_placementfollowup(self):
        result = reverse(views.save_placementfollowup)
        self.assertEqual(resolve(result).func, views.save_placementfollowup)

    def test_view_placementfollowup(self):
        result = reverse(views.view_placementfollowup)
        self.assertEqual(resolve(result).func, views.view_placementfollowup)

    def test_edit_placementfollowup(self):
        result = reverse(views.edit_placementfollowup)
        self.assertEqual(resolve(result).func, views.edit_placementfollowup)

    def test_delete_placementfollowup(self):
        result = reverse(views.delete_placementfollowup)
        self.assertEqual(resolve(result).func, views.delete_placementfollowup)

    def test_save_placement(self):
        result = reverse(views.save_placement)
        self.assertEqual(resolve(result).func, views.save_placement)

    def test_view_placement(self):
        result = reverse(views.view_placement)
        self.assertEqual(resolve(result).func, views.view_placement)

    def test_edit_placement(self):
        result = reverse(views.edit_placement)
        self.assertEqual(resolve(result).func, views.edit_placement)

    def test_delete_placement(self):
        result = reverse(views.delete_placement)
        self.assertEqual(resolve(result).func, views.delete_placement)

    def test_manage_placementfollowup(self):
        result = reverse(views.manage_placementfollowup)
        self.assertEqual(resolve(result).func, views.manage_placementfollowup)

    def test_background_details(self):
        result = reverse(views.background_details)
        self.assertEqual(resolve(result).func, views.background_details)

    def test_edit_education_info(self):
        result = reverse(views.edit_education_info)
        self.assertEqual(resolve(result).func, views.edit_education_info)

    def test_view_education_info(self):
        result = reverse(views.view_education_info)
        self.assertEqual(resolve(result).func, views.view_education_info)

    def test_delete_education_info(self):
        result = reverse(views.delete_education_info)
        self.assertEqual(resolve(result).func, views.delete_education_info)

    def test_edit_bursary_info(self):
        result = reverse(views.edit_bursary_info)
        self.assertEqual(resolve(result).func, views.edit_bursary_info)

    def test_view_bursary_info(self):
        result = reverse(views.view_bursary_info)
        self.assertEqual(resolve(result).func, views.view_bursary_info)

    def test_delete_bursary_info(self):
        result = reverse(views.delete_bursary_info)
        self.assertEqual(resolve(result).func, views.delete_bursary_info)
