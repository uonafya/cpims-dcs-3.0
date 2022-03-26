from django.test import TestCase,Client,SimpleTestCase
from django.urls import reverse
import uuid
from .functions import ovc_registration
from .models import OVCUpload,OVCRegistration,OVCAggregate,OVCHouseHold,OVCHHMembers,OVCFacility,OVCSchool,OVCCluster,OVCClusterCBO,OVCEligibility,OVCEducation,OVCHealth
from .forms import OVCRegistrationForm,OVCSearchForm

class TestViews(TestCase):
    """Test for cpovc_ovc.views"""
    def test_urls(self):
        self.home_url = reverse("")
        self.ovc_search_url = reverse("ovc/search/")
        self.ovc_new = reverse("ovc/new/",kwargs={'id': 1})
        self.ovc_edit = reverse("ovc/edit/",kwargs={'id': 1})
        self.ovc_view = reverse("ovc/view/",kwargs={'id': 1})
        self.hh_manage = reverse(r'^hh/view/',kwargs={'id':1})
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

class TestForms(SimpleTestCase):
    """Test for cpovc_ovc.forms"""
    def test_ovc_search_form(self):
        form = OVCSearchForm(data={
            'search_name':'Albert',
            'search_criteria':'0',
            'person_exited':'23',
            'form_type':'0'
        })
        self.assertTrue(form.is_valid())
    def test_ovc_search_no_data(self):
        form = OVCSearchForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),4) #len of errors should be equal to number to 4 each for each field

    def test_ovc_registration_form(self):
        form = OVCRegistration(data={
            'gstatus':'0',
            'astatus':'AYES',
            'cstatus':'AYES', 
            'sgstatus':'0',
            'sastatus':'AYES',
            'reg_date':'15/09/2010',
            'has_bcert':'',#need sample data
            'is_exited':'',#need sample data no initial given
            'bcert_no':'',#need sample data no initial given
            'ncpwd_no':'',#need sample data
            'disp':'',#need sample data
            'cbo_uid':'00001',
            'cbo_uid_check':'00001',
            'cbo_id':'',#need sample data
            'immunization':'0',
            'eligibility':'0',
            'exit_reason':'0',
            'hiv_status':'0',
            'school_level':'0',
            'facility':'',#need sample data
            'art_status':'0',
            'link_date':'',#need sample data
            'ccc_number':'', #need sample data
            'facility_id':'',#need sample data
            'school_id':'',#need sample data
            'admission_type':'0',
            'school_class':'0'
        })
        self.assertTrue(form.is_valid())
    def test_ovc_search_no_data(self):
        form = OVCSearchForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),27) 

class TestModels(TestCase):
    """Test For models"""
    def setUp(self):
        self.ovcaggregate1 = OVCAggregate.objects.create(
            indicator_name='indic1',
            project_year=2010,
            reporting_period='',
            cbo='',
            sub_county='',
            county='Nakuru',
            ward='',
            implementing_partnerid=123,
            implementing_partner='USAID',
            indicator_count=434,
            age=44,
            gender="",
            county_active="Nakuru",
            subcounty_active="",
            ward_active="",
            created_at="22/09/2009"
        )
        self.ovcupload1 = OVCUpload.objects.create(
            implementing_partnerid=123,
            project_year=2014,
            reporting_period="",
            ovc_filename="accounts",
            created_at="15/09/2009"
        )
        self.ovcregistraion1 = OVCRegistration.objects.create(
        id=uuid.uuid4,
        person="", #need a foreign key
        registration_date="22/09/2009",
        has_bcert=False,
        is_disabled=False,
        hiv_status="",
        school_level="",
        immunization_status="",
        org_unique_id="",
        caretaker="",
        child_cbo="",#need foreign key
        child_chv ="",#need foreign key
        exit_reason="",
        exit_date="",
        create_at="22/09/2009",
        is_active=True, 
        is_void=False

        )
        self.ovceligibility1 = OVCEligibility.objects.create(
            id=uuid.uuid4,
            person="",#need a foreign key
            criteria="",#need sample date
            created_at="13/09/2017",
            is_void=False
        )
        self.ovchousehold1 = OVCHouseHold.objects.create(
            id=uuid.uuid4, 
            head_person = "",#need a foreign key
            head_identifier='',#need sample data
            created_at="15/09/2002",
            is_void=False
        )
        self.ovchhmembers1 = OVCHHMembers.objects.create(
            id=uuid.uuid4,
            house_hold_id=uuid.uuid4,
            person="",#need a foreign key
            hh_head= True,
            member_type="",#need sample data
            member_alive="AYES",
            death_cause="",
            hiv_status="",
            date_linked="22/09/2009",
            is_void=False
        )
        self.ovcfacility1 = OVCFacility.objects.create(
            sub_county="",#need sample data
            facility_code="",#need sample data
            facility_name="",#need sample data
            is_void=False
        )
        self.ovchealth1 = OVCHealth.objects.create(
            id =uuid.uuid4,
            person="",#need a foreign key
            facility="",#need a foreign key
            art_status="",#need sample data
            date_linked ="15/09/2017",
            ccc_number = "32",#need sample data
            created_at = "",#need sample data
            is_void=False,
            
        )
        self.ovcschool1 = OVCSchool.objects.create(
            sub_county="",#need sample data
            school_level="",#need sample data
            school_name="",#need sample data
            is_void=False
        )
        self.ovceducation1 = OVCEducation.objects.create(
            id=uuid.uuid4,
            person="",#need a foreign key
            school="",#need sample data
            school_level="",#need sample data
            school_class = "",#need sample data
            admission_type = "",#need sample data
            created_at ="15/09/2009",
            is_void=False
        )
        self.ovccluster1 = OVCCluster.objects.create(
            id=uuid.uuid4,
            cluster_name="",#need sample data
            created_by="",#need foreign data
            created_at ="15/09/2009",
            is_void=False


        )
        self.ovcclustercbo1 = OVCClusterCBO.objects.create(
            id=uuid.uuid4,
            cluster="",#need a foreign key
            cbo = "",#need a foreign key
            added_at="",#need sample data
            is_void=False
        )

    def test_unicode_OVCAggregate(self):
        self.assertEqual(str(self.ovcaggregate1.indicator_name),'indic1')
    
    def test_unicode_OVCUpload(self):
        self.assertEqual(str(self.ovcupload1.ovc_filename,"accounts"))
    def test_unicode_OVCHHMembers(self):
        self.assertEqual(self.ovchhmembers1.id,uuid.uuid4)
    def test_unicode_OVCRegistration(self):
        self.assertEqual(str(self.ovcregistraion1.org_unique_id),22)
    def test_unicode_OVCEligibility(self):
        self.assertEqual(str(self.ovceligibility1.id,uuid.uuid4))
    def test_unicode_OVCHousehold(self):
        self.assertEqual(str(self.ovchousehold1.id,uuid.uuid4))
    def test_unicode_OVCFacility(self):
        self.assertEqual(str(self.ovcfacility1.facility_name," "))
    def test_unicode_OVCHealth(self):
        self.assertEqual(str(self.ovchealth1.id,uuid.uuid4))
    def test_unicode_OVCSchool(self):
        self.assertEqual(str(self.ovcschool1.school_name," "))
    def test_unicode_OVCEducation(self):
        self.assertEqual(str(self.ovceducation1.id,uuid.uuid4))
    def test_unicode_OVCCluster(self):
        self.assertEqual(str(self.ovccluster1.cluster_name," "))
    def test_unicode_OVCEClusterCBO(self):
        self.assertEqual(str(self.ovcclustercbo1.cbo,""))



    