from django.test import SimpleTestCase
from cpovc_forms.models import RegOrgUnit
from cpovc_registry.forms import FormRegistry,FormRegistryNew,RegistrationForm,LoginForm

class User(object):
      pass
class TestForms(SimpleTestCase):
    def setUp(self):
        self.user=User()
        self.user.reg_person_id=1
        self.user.is_superuser=True
    def test_form_registry(self):
        form=FormRegistry(data={ "reg_list":"123",
                                 "org_category":"small",
                                 "org_type":"",
                                  "handle_ovc":"",
                                  "org_unit_name":"",
                                  "org_closed":""
                                 })
        self.assertTrue(form.is_valid())
    def test_form_registry_new(self):
        form=FormRegistryNew(user=self.user,data={})
        self.assertTrue(form.is_valid())
    def test_registration_form(self):
        form=RegistrationForm(user=self.user,data={})
        self.assertTrue(form.is_valid())
    def test_login_form(self):
         form=LoginForm(use_required_attribute=1)
         self.assertTrue(form.is_valid())