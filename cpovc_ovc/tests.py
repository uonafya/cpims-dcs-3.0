from django.test import TestCase,Client,SimpleTestCase
from django.urls import reverse
import uuid
from .functions import ovc_registration
from .models import OVCUpload,OVCRegistration,OVCAggregate,OVCHouseHold,OVCHHMembers,OVCFacility,OVCSchool,OVCCluster,OVCClusterCBO,OVCEligibility,OVCEducation,OVCHealth
from .forms import OVCRegistrationForm,OVCSearchForm


#NOte:all empty values need sample data 

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


"""Test For models begins here"""

class ovcaggregate(TestCase):
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
    class Meta:
        db_table = 'ovc_aggregate'
        verbose_name = 'OVC aggregate data'
        verbose_name_plural = 'OVC aggregate data'        
    def test_unicode_OVCAggregate(self):
        self.assertEqual(str(self.ovcaggregate1.indicator_name),'indic1')
        verbose_name = self.ovcaggregate1._meta.get_field('verbose_name').unique
        verbose_name_plural = self.ovcaggregate1._meta.get_field('verbose_name_plural').unique
        self.assertEquals(db_table,'ovc_aggregate')
        self.assertEquals(verbose_name,'OVC aggregate data')
        self.assertEquals(verbose_name,'OVC aggregate data')

class ovcupload(TestCase):
    def setUp(self):
        self.ovcupload1 = OVCUpload.objects.create(
            implementing_partnerid=123,
            project_year=2014,
            reporting_period="",
            ovc_filename="accounts",
            created_at="15/09/2009"
    )
    class Meta:
        db_table = 'ovc_upload'
        verbose_name = 'OVC upload data'
        verbose_name_plural = 'OVC upload data'
    def test_unicode_OVCUpload(self):
        self.assertEqual(str(self.ovcupload1.ovc_filename,"accounts"))
        db_table = self.ovcupload1._meta.get_field('db_table').unique
        verbose_name = self.ovcupload1._meta.get_field('verbose_name').unique
        verbose_name_plural = self.ovcupload11._meta.get_field('verbose_name_plural').unique
        self.assertEquals(db_table,'ovc_upload')
        self.assertEquals(verbose_name,'OVC upload data')
        self.assertEquals(verbose_name,'OVC upload data')
class ovcregistraion(TestCase):
    def setUp(self):
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
    class Meta:
        db_table = 'ovc_registration'
        verbose_name = 'OVC Registration'
        verbose_name_plural = 'OVC Registration'
    def test_unicode_OVCUpload(self):
        self.assertEqual(str(self.ovcupload1.ovc_filename,"accounts"))
        db_table = self.ovcupload1._meta.get_field('db_table').unique
        verbose_name = self.ovcupload1._meta.get_field('verbose_name').unique
        verbose_name_plural = self.ovcupload1._meta.get_field('verbose_name_plural').unique
        self.assertEquals(db_table,'ovc_registration')
        self.assertEquals(verbose_name,'OVC Registration')
        self.assertEquals(verbose_name,'OVC Registration')
    

class ovceligibility(TestCase):
    def setUp(self):
        self.ovceligibility1 = OVCEligibility.objects.create(
            id=uuid.uuid4,
            person="",#need a foreign key
            criteria="",#need sample date
            created_at="13/09/2017",
            is_void=False
        )
        class Meta:
            db_table = 'ovc_eligibility'
            verbose_name = 'OVC Eligibility'
            verbose_name_plural = 'OVC Eligibility'
    def test_unicode_OVCEligibility(self):
        self.assertEqual(str(self.ovceligibility1.ovc_filename,"accounts"))
        db_table = self.ovceligibility1._meta.get_field('db_table').unique
        verbose_name = self.eligibility1._meta.get_field('verbose_name').unique
        verbose_name_plural = self.ovceligibility1._meta.get_field('verbose_name_plural').unique
        self.assertEquals(db_table,'ovc_eligibility')
        self.assertEquals(verbose_name,'OVC Eligibility')
        self.assertEquals(verbose_name,'OVC Eligibility')
    

        

class ovchousehold(TestCase):
    def setUp(self):
        self.ovchousehold1 = OVCHouseHold.objects.create(
            id=uuid.uuid4, 
            head_person = "",#need a foreign key
            head_identifier='',#need sample data
            created_at="15/09/2002",
            is_void=False
        )
        class Meta:
            db_table = 'ovc_household'
            verbose_name = 'OVC Registration'
            verbose_name_plural = 'OVC Registration'
        def test_unicode_OVCEligibility(self):
            self.assertEqual(str(self.ovchousehold1.ovc_filename,"accounts"))
            db_table = self.ovchousehold1._meta.get_field('db_table').unique
            verbose_name = self.ovchousehold1._meta.get_field('verbose_name').unique
            verbose_name_plural = self.ovchousehold1._meta.get_field('verbose_name_plural').unique
            self.assertEquals(db_table,'ovc_household')
            self.assertEquals(verbose_name,'OVC Registration')
            self.assertEquals(verbose_name,'OVC Registration')
class ovchhmembers(TestCase):
    def setUp(self):
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
    class Meta:
        db_table = 'ovc_household_members'
        verbose_name = 'OVC Registration'
        verbose_name_plural = 'OVC Registration'
    def test_unicode_OVCHHMembers(self):
        self.assertEqual(self.ovchhmembers1.id,uuid.uuid4)   
        db_table = self.ovchhmembers1._meta.get_field('db_table').unique
        verbose_name = self.ovchhmembers1._meta.get_field('verbose_name').unique
        verbose_name_plural = self.ovchhmembers1._meta.get_field('verbose_name_plural').unique
        self.assertEquals(db_table,'ovc_household_members')
        self.assertEquals(verbose_name,'OVC Registration')
        self.assertEquals(verbose_name,'OVC Registration')
        

class ovcfacility(TestCase):
    def setUp(self):
        self.ovcfacility1 = OVCFacility.objects.create(
            sub_county="",#need sample data
            facility_code="",#need sample data
            facility_name="",#need sample data
            is_void=False
        )
    class Meta:
        db_table = 'ovc_facility'
        verbose_name = 'OVC Facility'
        verbose_name_plural = 'OVC Facilities'
    def test_unicode_OVCFacility(self):
        self.assertEqual(str(self.ovcfacility1.ovc_filename,"accounts"))
        db_table = self.ovcfacility1._meta.get_field('db_table').unique
        verbose_name = self.ovcfacility1._meta.get_field('verbose_name').unique
        verbose_name_plural = self.ovcfacility1._meta.get_field('verbose_name_plural').unique
        self.assertEquals(db_table,'ovc_facility')
        self.assertEquals(verbose_name,'OVC Facility')
        self.assertEquals(verbose_name,'OVC Facility')

class ovchealth(TestCase):
    def setUp(self):
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
        class Meta:
            db_table = 'ovc_care_health'
            verbose_name = 'OVC Care Health'
            verbose_name_plural = 'OVC Care Health'
        def test_unicode_OVCHealth(self):
            self.assertEqual(str(self.ovchealth1.id,uuid.uuid4))
            db_table = self.ovchealth1._meta.get_field('db_table').unique
            verbose_name = self.ovchealth1._meta.get_field('verbose_name').unique
            verbose_name_plural = self.ovchealth1._meta.get_field('verbose_name_plural').unique
            self.assertEquals(db_table,'ovc_care_health')
            self.assertEquals(verbose_name,'OVC Care Health')
            self.assertEquals(verbose_name,'OVC Care Health')          

class ovcschool(TestCase):
    def setUp(self):
        self.ovcschool1 = OVCSchool.objects.create(
            sub_county="",#need sample data
            school_level="",#need sample data
            school_name="",#need sample data
            is_void=False
        )
    class Meta:
        db_table = 'ovc_school'
        verbose_name = 'OVC school'
        verbose_name_plural = 'OVC Schools'
    def test_unicode_OVCSchool(self):
        self.assertEqual(str(self.ovcschool1.school_name," "))
        db_table = self.ovcschool1._meta.get_field('db_table').unique
        verbose_name = self.ovcschool1._meta.get_field('verbose_name').unique
        verbose_name_plural = self.ovcschool1._meta.get_field('verbose_name_plural').unique
        self.assertEquals(db_table,'ovc_school')
        self.assertEquals(verbose_name,'OVC Schools')
        self.assertEquals(verbose_name,'OVC Schools')


class ovceducation(TestCase):
    def setUp(self):
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
    class Meta:
        db_table = 'ovc_care_education'
        verbose_name = 'OVC Care Education'
        verbose_name_plural = 'OVC Care Education'
    def test_unicode_OVCEducation(self):
        self.assertEqual(str(self.ovceducation1.id,uuid.uuid4))
        db_table = self.ovceducation1._meta.get_field('db_table').unique
        verbose_name = self.ovcducation1._meta.get_field('verbose_name').unique
        verbose_name_plural = self.ovceducation1._meta.get_field('verbose_name_plural').unique
        self.assertEquals(db_table,'ovc_care_education')
        self.assertEquals(verbose_name,'OVC Care Education')
        self.assertEquals(verbose_name,'OVC Care Education')


class ovccluster(TestCase):
    def setUp(self):
        self.ovccluster1 = OVCCluster.objects.create(
            id=uuid.uuid4,
            cluster_name="",#need sample data
            created_by="",#need foreign data
            created_at ="15/09/2009",
            is_void=False


        )
    class Meta:
        db_table = 'ovc_cluster'
        verbose_name = 'OVC Cluster'
        verbose_name_plural = 'OVC Clusters'  
    def test_unicode_OVCCluster(self):
        self.assertEqual(str(self.ovccluster1.cluster_name," "))  
        db_table = self.ovccluster1._meta.get_field('db_table').unique
        verbose_name = self.ovccluster1._meta.get_field('verbose_name').unique
        verbose_name_plural = self.ovccluster1._meta.get_field('verbose_name_plural').unique
        self.assertEquals(db_table,'ovc_cluster')
        self.assertEquals(verbose_name,'OVC Cluster')
        self.assertEquals(verbose_name,'OVC Cluster')

class ovcclustercbo(TestCase):
    def setUp(self):
        self.ovcclustercbo1 = OVCClusterCBO.objects.create(
            id=uuid.uuid4,
            cluster="",#need a foreign key
            cbo = "",#need a foreign key
            added_at="",#need sample data
            is_void=False
        )
    class Meta:
        db_table = 'ovc_cluster_cbo'
        verbose_name = 'OVC Cluster CBO'
        verbose_name_plural = 'OVC Cluster CBOs'
    def test_unicode_OVCEClusterCBO(self):
        self.assertEqual(str(self.ovcclustercbo1.cbo,""))
        db_table = self.ovcclustercbo1._meta.get_field('db_table').unique
        verbose_name = self.ovcclustercbo1._meta.get_field('verbose_name').unique
        verbose_name_plural = self.ovcclustercbo1._meta.get_field('verbose_name_plural').unique
        self.assertEquals(db_table,'ovc_cluster_cbo')
        self.assertEquals(verbose_name,'OVC Cluster CBO')
        self.assertEquals(verbose_name,'OVC Cluster CBO')  

   