from django.test import SimpleTestCase
from cpovc_forms.models import RegOrgUnit
from cpovc_forms.forms import OVCSchoolForm,OVCBursaryForm,DocumentsManager,SearchForm,ResidentialFollowupForm
class TestForms(SimpleTestCase):
    def test_ovc_school_form(self):
        form=OVCSchoolForm(data={"type_of_school":"1",
                                 "school_subcounty":"4",
                                  "school_ward'":"5",
                                    })
        self.assertTrue(form.is_valid())
    def test_ovc_bursary_form(self):
        form=OVCBursaryForm(data=
                            {
                              "bursary_type":"",
                              "disbursement_date":"",
                              "amount":"",
                               "year":"",
                               "term":"",
                               "person_id":"",
                               "bursary_id":"",
                               "operation_mode":""


                            })
        self.assertTrue(form.is_valid())

    def test_documents_manaager(self):
        form=DocumentsManager(data={
            "document_type":"",
            "document_description":"",
            "search_name":"",
            "file_name":"",
            "search_criteria":"",
            "person":""
        })
        self.assertTrue(form.is_valid())
    def test_search_form(self):
        form=SearchForm(data=
                        {
                        "form_type":"",
                         "form_person":"",
                         "case_serial":""

                        })
        self.assertTrue(form.is_valid())
    def test_ovc_search_form(self):
        form=SearchForm(data={
            "person_type":"",
            "search_name":"",
            "search_criteria":"",
            "form_type_search":""
        })
        self.assertTrue(form.is_valid())
    def test_residential_followupForm(self):
     form=ResidentialFollowupForm(data={
         "org_unit_ids":"TNRH",
         "org_units_list":"",
         "discharge_destination":"",
         "name_of_school":"",
         "casecategorys":"",
         "person":"",
         "child_age":"10",

     })
     self.assertTrue(form.is_valid())