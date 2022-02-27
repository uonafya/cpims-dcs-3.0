from django.test import TestCase,Client
from django.urls import reverse
import uuid
from .functions import ovc_registration
from .. import models
#OVCUpload,models.OVCRegistration,models.OVCAggregate,models.OVCHouseHold,models.OVCHHMembers,models.OVCFacility,models.OVCSchool,models.OVCCluster,models.OVCClusterCBO,models.O,models.OVCEligibility,models.OVCEducation,models.OVCHealth

class TestViews:
    def test_urls(self):
        self.home_url = reverse("")
        self.ovc_search_url = reverse("ovc/search/")
        self.ovc_new = reverse("ovc/new/",args=[1])
        self.ovc_edit = reverse("ovc/edit/",args=[1])
        self.ovc_view = reverse("ovc/view/",args=[1])
        self.hh_manage = reverse(r'^hh/view/',args=[1])
    def test_home_GET(self):
        client = Client()
        response = client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'ovc/home.html')
    
    def test_ovc_search(self):
        client = Client()
        response = self.client.post(self.ovc_search_url,'searchitem')#just a search item
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'status': 'success'}
        ) 
    def test_ovc_register_POST(self):
        client = Client()
        models.OVCRegistration.objects.create(
            id=uuid.uuid4
        )
        response = self.client.post(self.ovc_new,{
            id:uuid.uuid4,
            person:"mike",
            registration_date :"22/2/2022",
            has_bcert :"False",
            is_disabled:"False",
            hiv_status: "" ,
            school_level : "",
            immunization_status:"",
            org_unique_id : "",
            caretaker :"",
            child_cbo : "", #cant be null and Foreign key==RegOrgUnit
            child_chv : " " ,#cant be null and Foreign key==RegPerson
            exit_reason : " ",
            exit_date : " ",
            created_at :22/2/2022,
            is_active : "True",
            is_void : "False"
        })
        self.assertEquals(response.status_code, 200)
        
    def hh_manage_GET(self):
        client = Client()
        response = client.get(self.hh_manage)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'ovc/household.html')
    def test_ovc_view(self):
        client = Client()
        response = client.get(self.ovc_view)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,"vc/view_child.html")


"""      
    def test_ovc_edit_POST(self):
        client = Client()
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,"ovc/edit_child.html")
"""


    
