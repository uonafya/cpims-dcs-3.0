
from django.test import  SimpleTestCase,Client
from django.urls import  reverse
#import cpovc_forms.models as models
#import json
class TestViews(SimpleTestCase):
     def setUp(self):
          self.client = Client()
          self.home_url=reverse('registry')
          self.registry_urls=reverse('registry_new')
          self.register_edit_url=reverse('registry_edit',args=[1])
          self.register_details=reverse('register_details',args=[1])
          self.new_person=reverse('new_person')
          self.persons_search=reverse('search_persons')
          self.view_person=reverse('view_person',args=[1])
          self.edit_person=reverse('edit_person',args=[1])
          self.new_user=reverse('new_user',args=[1])
     def test_view_home_GET(self):
          response=self.client.get(self.home_url)
          self.assertEqual(response.status_code,302)
         # self.assertTemplateUsed(response,'forms/forms_index.html')
     def test_view_registry_POST(self):
         response = self.client.post(self.registry_urls,
                                     {
                                         ' org_unit_type':'TBVC',
                                          'org_unit_name':'Manu',
                                          'handle_ovc':'ORG',
                                           'reg_date':'2021',
                                           'county':"Baringo",
                                           'sub_county':'Baringo central',
                                           'ward':'Kabarnet',
                                           'parent_org_unit':'',
                                           'org_reg_type':'private',
                                           'legal_reg_number':'1234',
                                              })
         self.assertEqual(response.status_code, 302)
         #self.assertTemplateUsed(response, 'forms/forms_registry.html')
     def test_register_edit(self):
         response = self.client.post(self.register_edit_url,
                                     {
                                         ' org_unit_type': 'TBVC',
                                         'org_unit_name': 'Manu',
                                         'handle_ovc': 'ORG',
                                         'reg_date': '2021',
                                         'county': "Baringo",
                                         'sub_county': 'Baringo central',
                                         'ward': 'Kabarnet',
                                         'parent_org_unit': '',
                                         'org_reg_type': 'private',
                                         'legal_reg_number': '1234',
                                     })
         self.assertEqual(response.status_code, 302)
     def test_register_details(self):
         response = self.client.post(self.register_edit_url,
                                     {
                                         ' org_unit_type': 'TBVC',
                                         'org_unit_name': 'Manu',
                                         'handle_ovc': 'ORG',
                                         'reg_date': '2021',
                                         'county': "Baringo",
                                         'sub_county': 'Baringo central',
                                         'ward': 'Kabarnet',
                                         'parent_org_unit': '',
                                         'org_reg_type': 'private',
                                         'legal_reg_number': '1234',
                                     })
         self.assertEqual(response.status_code, 302)
     def test_new_person(self):
         response=self.client.post(self.new_person,
                                   {
                                     'person_uid':'1DE45',
                                     'unique_id' :'213',
                                     'first_name':"Joe",
                                      'other_names':'Doe'

                                   })
         self.assertEqual(response.status_code,302)
     def test_persons_search(self):
         response=self.client.post(self.persons_search)
         self.assertEqual(response.status_code,302)
     def test_view_person(self):
         response=self.client.get(self.view_person,{})
         self.assertEqual(response.status_code,302)
     def test_edit_person(self):
         response=self.client.post(self.edit_person,args=[1])
         self.assertEqual(response.status_code,302)
     def test_new_user(self):
         response=self.client.post(self.new_user,{})
         self.assertEqual(response.status_code,302)
