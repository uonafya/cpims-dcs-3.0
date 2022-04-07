
from django.test import  SimpleTestCase,Client
from django.urls import  reverse
#import cpovc_forms.models as models
#import json
class TestViews(SimpleTestCase):
     def setUp(self):
          self.client = Client()
          self.forms_url=reverse('forms')
          self.registry_urls=reverse('forms_registry')
          self.document_manager_url=reverse('documents_manager')
          self.case_record_sheet=reverse('case_record_sheet')
          self.edit_case_record_sheet=reverse('edit_case_record_sheet',args=[1])
          self.view_case_record_sheet=reverse('view_case_record_sheet',args=[1])
          self.delete_case_record_sheet=reverse('delete_case_record_sheet',args=[1])
          self.new_case_record_sheet=reverse('new_case_record_sheet',args=[1])
          self.residential_placement=reverse('residential_placement')
          self.ovc_search=reverse('ovc_search')
          self.alternative_family_care=reverse('alternative_family_care')
          self.new_alternative_family_care=reverse('new_alternative_family_care',args=[1])
          self.edit_alternative_family_care=reverse('edit_alternative_family_care',args=[1])
          self.view_alternative_family_care=reverse('view_alternative_family_care',args=[1])
          self.case_events=reverse('case_events',args=[1])
          self.save_encounter=reverse('save_encounter')
          self.view_encounter=reverse('view_encounter')
          self.edit_encounter=reverse('edit_encounter')
          self.delete_encounter=reverse('delete_encounter')
          self.save_court=reverse('save_court')
          self.view_court=reverse('view_court')
          self.edit_court=reverse('edit_court')
          self.delete_court=reverse('delete_court')

     def test_forms_home_GET(self):
          response=self.client.get(self.forms_url)
          self.assertEqual(response.status_code,302)
         # self.assertTemplateUsed(response,'forms/forms_index.html')
     def test_forms_registry_POST(self):
         response = self.client.post(self.registry_urls,
                                     {
                                         'person_type':'TBVC',
                                          'search_name':'Manu',
                                          'search_criteria':'ORG'

                                     })
         self.assertEqual(response.status_code, 302)
         #self.assertTemplateUsed(response, 'forms/forms_registry.html')
     def test_document_manager(self):
         response=self.client.post(self.document_manager_url)
         self.assertEqual(response.status_code,302)
     def test_case_record_sheet(self):
         response=self.client.post(self.case_record_sheet)
         self.assertEqual(response.status_code,302)
     def test_edit_case_record_sheet(self):
         response=self.client.post(self.case_record_sheet)
         self.assertEqual(response.status_code,302)
     def test_view_case_record_sheet(self):
         response=self.client.get(self.view_case_record_sheet)
         self.assertEqual(response.status_code,302)
     def test_delete_case_record_sheet(self):
         response=self.client.get(self.delete_case_record_sheet)
         self.assertEqual(response.status_code,302)
     def test_new_case_record_sheet(self):
         response=self.client.post(self.new_case_record_sheet)
         self.assertEqual(response.status_code,302)
     def test_residential_placement(self):
         response=self.client.post(self.residential_placement)
         self.assertEqual(response.status_code,302)
     def test_ovc_search(self):
         response=self.client.post(self.ovc_search)
         self.assertEqual(response.status_code,200)
     def test_alternative_family_care(self):
         response=self.client.post(self.alternative_family_care)
         self.assertEqual(response.status_code,302)
     def test_new_alternative_family_care(self):
         response=self.client.post(self.new_alternative_family_care)
         self.assertEqual(response.status_code,302)
     def test_edit_alternative_family_care(self):
         response=self.client.post(self.edit_alternative_family_care)
         self.assertEqual(response.status_code,302)
     def test_view_alternative_family_care(self):
         response=self.client.get(self.view_alternative_family_care)
         self.assertEqual(response.status_code,302)
     def test_case_events(self):
         response=self.client.get(self.case_events)
         self.assertEqual(response.status_code,302)
     def test_save_encounter(self):
         response=self.client.get(self.save_encounter)
         self.assertEqual(response.status_code,200)
     def test_view_encounter_get(self):
         response=self.client.get(self.view_encounter)
         self.assertEqual(response.status_code,200)
     def test_view_encounter_post(self):
         response=self.client.post(self.view_encounter)
         self.assertEqual(response.status_code,200)
     def test_edit_encounter(self):
         response=self.client.post(self.edit_encounter)
         self.assertEqual(response.status_code,200)
     def test_delete_encounter(self):
         response=self.client.post(self.delete_encounter)
         self.assertEqual(response.status_code,200)
     def test_save_court(self):
         response=self.client.post(self.save_court)
         self.assertEqual(response.status_code,200)
     def test_view_court(self):
         response=self.client.get(self.view_court)
         self.assertEqual(response.status_code,200)
     def test_edit_court(self):
         response=self.client.post(self.edit_court)
         self.assertEqual(response.status_code,302)
     def test_delete_court(self):
         response=self.client.post(self.delete_court)
         self.assertEqual(response.status_code,302)




