from django.test import  TestCase,Client
from django.urls import  reverse
import cpovc_forms.models as models
import json
class TestViews(TestCase):
     def setUp(self):
          self.client = Client()
          self.forms_url=reverse('forms')
          self.registry_urls=reverse('forms_registry')
          self.document_manager_url=reverse('documents_manager')
     def test_forms_home_GET(self):
          response=self.client.get(self.forms_url)
          self.assertEqual(response.status_code,200)
          self.assertTemplateUsed(response,'forms/forms_index.html')
     def test_forms_registry_POST(self):
         response = self.client.post(self.registry_urls,
                                     {
                                         'person_type':'TBVC',
                                          'search_name':'Manu',
                                          'search_criteria':'ORG'

                                     })
         self.assertEqual(response.status_code, 200)
         self.assertTemplateUsed(response, 'forms/forms_registry.html')







