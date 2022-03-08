from django.test import TestCase
from datetime import datetime
import unittest
import urls
from django.test import TestCase, Client
client = Client()

#URL Tests
class URLTests(TestCase):
    def test_registry(self):
        response = self.client.get('ou/registry')
        self.assertEqual(response.status_code, 200)
        
    def test_registry_new(self):
        response = self.client.get('ou/new/registry_new')
        self.assertEqual(response.status_code, 200)

    def test_register_details(self):
        response = self.client.get('ou/view/register_details')
        self.assertEqual(response.status_code, 200)

    def test_registry_edit(self):
        response = self.client.get('ou/edit/registry_edit')
        self.assertEqual(response.status_code, 200)

    def test_search_persons(self):
        response = self.client.get('person/search/search_persons')
        self.assertEqual(response.status_code, 200)

    def test_new_user(self):
        response = self.client.get('person/user/new_user')
        self.assertEqual(response.status_code, 200)

    def test_person_actions(self):
        response = self.client.get('person/person_actions')
        self.assertEqual(response.status_code, 200)

    def test_new_person(self):
        response = self.client.get('person/new/new_person')
        self.assertEqual(response.status_code, 200)

    def test_edit_person(self):
        response = self.client.get('person/edit/edit_person')
        self.assertEqual(response.status_code, 200)

    def test_view_person(self):
        response = self.client.get('person/view/view_person')
        self.assertEqual(response.status_code, 200)

    def test_delete_person(self):
        response = self.client.get('person/delete/delete_person')
        self.assertEqual(response.status_code, 200)

    def test_reg_lookup(self):
        response = self.client.get('lookup/reg_lookup')
        self.assertEqual(response.status_code, 200)

    def test_person_api(self):
        response = self.client.get('person/api/person_api')
        self.assertEqual(response.status_code, 200)

    def test_person_profile(self):
        response = self.client.get('person/profile/person_profile')
        self.assertEqual(response.status_code, 200)

    ###Below are the Complete Model tests;;
from django.test import TestCase

from catalog.models import Author

class RegPerson(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        RegPerson.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        regperson = RegPerson.objects.get(id=1)
        field_label = regperson._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_date_of_death_label(self):
        regperson = RegPerson.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'died')

    def test_first_name_max_length(self):
        regperson = RegPerson.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        regperson = RegPerson.objects.get(id=1)
        expected_object_name = f'{author.last_name}, {author.first_name}'
        self.assertEqual(str(author), expected_object_name)

    def test_get_absolute_url(self):
        regperson = RegPerson.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(author.get_absolute_url(), 'include path to regperson')
    
    ### RegPersonGaurdianDetails

class RegPersonGaurdianDetails(TestCase):
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        RegPersonGaurdianDetails.objects.create(first_name='Michoma', last_name='Saruni')

    def test_child_person_label(self):
        regpersongaurdiandetails = RegPersonGaurdianDetails.objects.get(id=1)
        field_label = regpersongaurdiandetails._meta.get_field('child_person').verbose_name
        self.assertEqual(field_label, 'child_person')

    def test_gaurdian_person_label(self):
        regpersongaurdiandetails = RegPersonGaurdianDetails.objects.get(id=1)
        field_label = regpersongaurdiandetails._meta.get_field('gaurdian_person').verbose_name
        self.assertEqual(field_label, 'gaurdian_person')

    def test_first_name_max_length(self):
        regpersongaurdiandetails = RegPersonGaurdianDetails.objects.get(id=1)
        max_length = regpersongaurdiandetails._meta.get_field('relationship').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        regpersongaurdiandetails = RegPersonGaurdianDetails.objects.get(id=1)
        expected_object_name = f'{regpersongaurdiandetails.last_name}, {regpersongaurdiandetails.first_name}'
        self.assertEqual(str(regpersongaurdiandetails), expected_object_name)

    def test_get_absolute_url(self):
        regpersongaurdiandetails = RegPersonGaurdianDetails.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(author.get_absolute_url(), 'path to the regpersongaurdiandetails')

    
   ###RegPersonsGeo details
class RegPersonsGeo (TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        RegPersonGeo.objects.create(first_name='Michoma', last_name='Saruni')

    def test_person_label(self):
        regpersonsgeo = RegPersonGeo.objects.get(id=1)
        field_label = regpersonsgeo._meta.get_field('person').verbose_name
        self.assertEqual(field_label, 'person')

    def test_area_label(self):
        regpersonsgeo = Author.objects.get(id=1)
        field_label = refpersonsgeo._meta.get_field('area').verbose_name
        self.assertEqual(field_label, 'area')

    def test_area_type_length(self):
        regpersonsgeo = RegPersonsGeo.objects.get(id=1)
        max_length = regpersonsgeo._meta.get_field('are_type').max_length
        self.assertEqual(max_length, 4)

    def test_object_name_is_last_name_comma_first_name(self):
        regpersonsgeo = RegPersonGeo.objects.get(id=1)
        expected_object_name = f'{regpersongeo.last_name}, {regpersonsgeo.first_name}'
        self.assertEqual(str(regpersonsgeo), expected_object_name)

    def test_get_absolute_url(self):
        regpersonsgeo = RegPersonsGeo.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(author.get_absolute_url(), 'path to reg personsgeo')

    def test_person_timeline(self):
        response = self.client.get('person/tl/person_timeline')
        self.assertEqual(response.status_code, 200)



start_date = '2002-01-01'
fmt = '%Y-%m-%d'

new_date = datetime.strptime(start_date, fmt)
todate = datetime.now()

print(new_date)
