from django.test import TestCase


# Create your tests here.

# Form home test
class ViewTests(TestCase):
    def test_home_form(self):
        response = self.client.get("forms/forms_home",{'person_type': 'TBVC'})
        self.assertEqual(response.status_code, 200)

    def test_form_registry(self):
        response = self.client.get("forms/forms_registry", {'form': {'placeholder': ('CCO/XX/XXX/5/29/XX/YYYY'),
               'class': 'form-control',
               'id': 'case_serial',
               'data-parsley-required': 'false'}})
        self.assertEqual(response.status_code, 200)
