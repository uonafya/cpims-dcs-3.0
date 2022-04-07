from django.test import TestCase
from datetime import datetime
import unittest
from django.test import TestCase, Client
from django.test import  SimpleTestCase
from django.urls import reverse,resolve
import cpovc_registry.views as views


client = Client()
# URL Tests
class URLTests(SimpleTestCase):
    def test_registry(self):
        response =client.get('/ou/')
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


