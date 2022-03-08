from django.test import TestCase
from datetime import datetime


# Create your tests here.
 ###Complete Url test Cases;;

  from django import.test import TestCase
     class URLTests(TestCase):
         def test_testhomepage(self):
             response = self.client.get('/')
             self.assertEqual(response. status code ,200)
         def test_profile(self):
             response =self.client.get('person/profile/')
             self.assertEqual(response. status code ,200)
        def test_api(self):
             response =self.client.get('person/api/')
             self.assertEqual(response. status code ,200)
        def  test_lookup(self):
            response = self.client.get('lookup/')
            self.assertEqual(response.status code ,200)
        def  test_search(self):
            response = self.client.get('person/search/')
            self.assertEqual(response. status code ,200)
        def  new_user(self):
            response = self.client.get('person/user/<int:id>/')
            self.assertEqual(response. status code ,200)
        def  edit_person(self):
            response = self.client.get('person/edit/<int:id>/')
            self.assertEqual(response. status code ,200)
        def  view_person(self):
            response = self.client.get('person/view/<int:id>/')
            self.assertEqual(response. status code ,200)
         def  delete_person(self):
            response = self.client.get('person/delete/<id>/'')
            self.assertEqual(response. status code ,200)

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
    @classmethod
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
