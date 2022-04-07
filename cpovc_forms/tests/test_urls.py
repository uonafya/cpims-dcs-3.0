from django.test import  SimpleTestCase
from django.urls import reverse,resolve
import cpovc_forms.views as views

class TestUrls(SimpleTestCase):
     def test_form_home_urls(self):
         url=reverse('forms')
         self.assertEqual(resolve(url).func,views.forms_home)
     def  test_form_registry_urls(self):
         url = reverse('forms_registry')
         self.assertEqual(resolve(url).func, views.forms_registry)
     def  test_form_documents_manager_urls(self):
         url = reverse('documents_manager')
         self.assertEqual(resolve(url).func,views.documents_manager)
     def test_form_document_manager_search(self):
         url=reverse('documents_manager_search')
         self.assertEqual(resolve(url).func,views.documents_manager_search)
     def test_form_crs(self):
         url=reverse('case_record_sheet')
         self.assertEqual(resolve(url).func,views.case_record_sheet)
     def test_new_case_record_sheet(self):
         url=reverse('new_case_record_sheet',args=[1])
         self.assertEqual(resolve(url).func,views.new_case_record_sheet)
     def test_view_case_record_sheet(self):
         url=reverse('view_case_record_sheet',args=[1])
         self.assertEqual(resolve(url).func,views.view_case_record_sheet)
     def test_edit_case_record_sheet(self):
         url=reverse('edit_case_record_sheet',args=[1])
         self.assertEqual(resolve(url).func,views.edit_case_record_sheet)
     def test_delete_case_record_sheet(self):
         url=reverse('delete_case_record_sheet',args=[1])
         self.assertEqual(resolve(url).func,views.delete_case_record_sheet)

     def test_alternative_family_care_urls(self):
         url = reverse('alternative_family_care')
         self.assertEqual(resolve(url).func, views.alternative_family_care)

     def test_new_alternative_family_care_urls(self):
         url = reverse('alternative_family_care')
         self.assertEqual(resolve(url).func, views.alternative_family_care)

     def test_edit_alternative_family_care_urls(self):
         url = reverse('edit_alternative_family_care',args=[1])
         self.assertEqual(resolve(url).func, views.edit_alternative_family_care)

     def test_view_alternative_family_care_urls(self):
         url = reverse('view_alternative_family_care',args=[1])
         self.assertEqual(resolve(url).func, views.view_alternative_family_care)

     def test_save_placement_urls(self):
         url = reverse('save_placement')
         self.assertEqual(resolve(url).func, views.save_placement)

     def view_placement_urls(self):
         url = reverse('view_placement', args=[1])
         self.assertEqual(resolve(url).func, views.view_placement)

     def test_edit_placements(self):
         url = reverse('edit_placement', args=[1])
         self.assertEqual(resolve(url).func, views.edit_placement)

     def test_delete_placement(self):
         url = reverse('delete_placement')
         self.assertEqual(resolve(url).func, views.delete_placement)

     def test_residential_placement(self):
         url = reverse('residential_placement')
         self.assertEqual(resolve(url).func, views.residential_placement)