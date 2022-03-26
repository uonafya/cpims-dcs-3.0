from django.test import TestCase
from datetime import datetime
import unittest
import urls
from django.test import TestCase, Client
client = Client()

#URL Tests for cpovc_registry
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



# Tests for models in cpovc_registry
from .models import *

class RegOrgUnit(TestCase):

    def test_org_unit_id_vis_label(self):
        unit = RegOrgUnit.objects.get(id=1)
        field_label = unit._meta.get_field('org_unit_id_vis').verbose_name
        self.assertEqual(field_label, 'org unit id vis')

    def test_org_unit_id_vis_max_length(self):
        unit = RegOrgUnit.objects.get(id=1)
        max_length = unit._meta.get_field('org_unit_id_vis').max_length
        self.assertEqual(max_length, 12)

    def test_org_unit_name_label(self):
        unit = RegOrgUnit.objects.get(id=1)
        field_label = unit._meta.get_field('org_unit_name').verbose_name
        self.assertEqual(field_label, 'org unit name')

    def test_org_unit_name_max_length(self):
        unit = RegOrgUnit.objects.get(id=1)
        max_length = unit._meta.get_field('org_unit_name').max_length
        self.assertEqual(max_length, 255)

    def test_org_unit_type_id_label(self):
        unit = RegOrgUnit.objects.get(id=1)
        field_label = unit._meta.get_field('org_unit_type_id').verbose_name
        self.assertEqual(field_label, 'org unit type id')

    def test_org_unit_type_id_max_length(self):
        unit = RegOrgUnit.objects.get(id=1)
        max_length = unit._meta.get_field('org_unit_type_id').max_length
        self.assertEqual(max_length, 4)

    def test_date_operational_label(self):
        unit = RegOrgUnit.objects.get(id=1)
        field_label = unit._meta.get_field('date_operational').verbose_name
        self.assertEqual(field_label, 'date operational')

    def test_date_closed_label(self):
        unit = RegOrgUnit.objects.get(id=1)
        field_label = unit._meta.get_field('date_closed').verbose_name
        self.assertEqual(field_label, 'date closed')


class RegOrgUnitContactTestCase(TestCase):

    def setUpTestData(cls):
        RegOrgUnitContact.objects.create(contact_detail_type_id="DS01", contact_detail="0758008788")

    def test_contact_detail_type_id_label(self):
        contact = RegOrgUnitContact.objects.get(id=1)
        field_label = contact._meta.get_field('contact_detail_type_id').verbose_name
        self.assertEqual(field_label, 'contact detail type id')

    def test_contact_detail_type_id_max_length(self):
        contact = RegOrgUnitContact.objects.get(id=1)
        max_length = contact._meta.get_field('contact_detail_type_id').max_length
        self.assertEqual(max_length, 12)

    def test_contact_detail_name_label(self):
        contact = RegOrgUnitContact.objects.get(id=1)
        field_label = contact._meta.get_field('contact_detail').verbose_name
        self.assertEqual(field_label, 'org unit name')

    def test_contact_detail_max_length(self):
        contact = RegOrgUnitContact.objects.get(id=1)
        max_length = contact._meta.get_field('contact_detail').max_length
        self.assertEqual(max_length, 255)

class RegOrgUnitExternalIDTestCase(TestCase):

    def setUpTestData(cls):
        RegOrgUnitExternalID.objects.create(identifier_type_id="001", identifier_value="NationalID")

    def test_string_method(self):
        ExternalId = RegOrgUnitExternalID.objects.get(id=1)
        expected_output = f"IdentifierType: {RegOrgUnitExternalID.identifier_type_id} {RegOrgUnitExternalID.identifier_value}"
        self.assertEqual(str(RegOrgUnitExternalID), expected_output)

class RegOrgUnitGeographyTestCase(TestCase):
    def test_date_linked_label(self):
        unitGeo = RegOrgUnitGeography.objects.get(id=1)
        field_label = unitGeo._meta.get_field('date_linked').verbose_name
        self.assertEqual(field_label, 'linked')
    def test_date_delinked_label(self):
        unitGeo = RegOrgUnitGeography.objects.get(id=1)
        field_label = unitGeo._meta.get_field('date_delinked').verbose_name
        self.assertEqual(field_label, 'delinked')

class RegPersonTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        RegPerson.objects.create(designation='Kabarak', first_name='Captain', surname='Nepapa')

    def test_first_name_label(self):
        person = RegPerson.objects.get(id=1)
        field_label = person._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_surname_label(self):
        person = RegPerson.objects.get(id=1)
        field_label = person._meta.get_field('surname').verbose_name
        self.assertEqual(field_label, 'surname')

    def test_designation_label(self):
        person = RegPerson.objects.get(id=1)
        field_label = person._meta.get_field('designation').verbose_name
        self.assertEqual(field_label, 'designation')

    def test_first_name_max_length(self):
        person = RegPerson.objects.get(id=1)
        max_length = person._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 255)

    def test_designation_max_length(self):
        person = RegPerson.objects.get(id=1)
        max_length = person._meta.get_field('designation').max_length
        self.assertEqual(max_length, 25)

#class RegBiometricTestCase(TestCase):

class RegPersonsGuardiansTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        RegPersonsGuardians.objects.create(relationship='Uncle')

    def test_relationship_label(self):
        guardian = RegPersonsGuardians.objects.get(id=1)
        field_label = guardian._meta.get_field('relationship').verbose_name
        self.assertEqual(field_label, 'relationship')

    def test_relationship_label_length(self):
        guardian = RegPersonsGuardians.objects.get(id=1)
        max_length = guardian._meta.get_field('relationship').max_length
        self.assertEqual(max_length, 5)

    def test_date_linked_label(self):
        guardian = RegPersonsGuardians.objects.get(id=1)
        field_label = guardian._meta.get_field('date_linked').verbose_name
        self.assertEqual(field_label, 'linked')

    def test_date_delinked_label(self):
        guardian = RegPersonsGuardians.objects.get(id=1)
        field_label = guardian._meta.get_field('date_delinked').verbose_name
        self.assertEqual(field_label, 'delinked')


class RegPersonsTypesTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        RegPersonsTypes.objects.create(person_type_id= '001')

    def test_person_type_id_label(self):
        person_type = RegPersonsTypes.objects.get(id=1)
        field_label = person_type._meta.get_field('person_type_id').verbose_name
        self.assertEqual(field_label, 'person type id')

    def test_person_type_id_max_length(self):
        person_type = RegPersonsTypes.objects.get(id=1)
        max_length = person_type._meta.get_field('person_type_id').max_length
        self.assertEqual(max_length, 4)

    def test_date_began_label(self):
        person_type = RegPersonsTypes.objects.get(id=1)
        field_label = person_type._meta.get_field('date_began').verbose_name
        self.assertEqual(field_label, 'date began')

    def test_date_ended_label(self):
        person_type = RegPersonsTypes.objects.get(id=1)
        field_label = person_type._meta.get_field('date_ended').verbose_name
        self.assertEqual(field_label, 'date ended')

class RegPersonsGeoTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        RegPersonsGeo.objects.create(area_type='area')

    def test_area_type_label(self):
        personsgeo = RegPersonsGeo.objects.get(id=1)
        field_label = personsgeo._meta.get_field('area_type').verbose_name
        self.assertEqual(field_label, 'area type')

    def test_area_type_max_length(self):
        personsgeo = RegPersonsGeo.objects.get(id=1)
        max_length = personsgeo._meta.get_field('area_type').max_length
        self.assertEqual(max_length, 4)

    def test_date_linked_label(self):
        personsgeo = RegPersonsGuardians.objects.get(id=1)
        field_label = personsgeo._meta.get_field('date_linked').verbose_name
        self.assertEqual(field_label, 'linked')

    def test_date_delinked_label(self):
        personsgeo = RegPersonsGuardians.objects.get(id=1)
        field_label = personsgeo._meta.get_field('date_delinked').verbose_name
        self.assertEqual(field_label, 'delinked')



class RegPersonsExternalIdsTestCase(TestCase):

    def test_identifier_type_id_label(self):
        externalid = RegPersonsExternalIds.objects.get(id=1)
        field_label = externalid._meta.get_field('identifier_type_id').verbose_name
        self.assertEqual(field_label, 'identifier type id')

    def test_identifier_label(self):
        externalid = RegPersonsExternalIds.objects.get(id=1)
        field_label = externalid._meta.get_field('identifier').verbose_name
        self.assertEqual(field_label, 'identifier')

    def test_identifier_type_id_max_length(self):
        externalid = RegPersonsExternalIds.objects.get(id=1)
        max_length = externalid._meta.get_field('identifier_type_id').max_length
        self.assertEqual(max_length, 4)

    def test_identifier_max_length(self):
        externalid = RegPersonsExternalIds.objects.get(id=1)
        max_length = externalid._meta.get_field('identifier').max_length
        self.assertEqual(max_length, 255)

class RegPersonsContactTestCase(TestCase):

    def test_contact_detail_type_id_label(self):
        contact = RegPersonsContact.objects.get(id=1)
        field_label = contact._meta.get_field('contact_detail_type_id').verbose_name
        self.assertEqual(field_label, 'contact')

    def test_contact_detail_label(self):
        contact = RegPersonsContact.objects.get(id=1)
        field_label = contact._meta.get_field('contact_detail').verbose_name
        self.assertEqual(field_label, 'contact detail')

    def test_contact_detail_max_length(self):
        contact = RegPersonsContact.objects.get(id=1)
        max_length = contact._meta.get_field('contact_detail').max_length
        self.assertEqual(max_length, 4)

    def test_contact_detail_type_id_max_length(self):
        contact = RegPersonsContact.objects.get(id=1)
        max_length = contact._meta.get_field('contact_detail_type_id').max_length
        self.assertEqual(max_length, 255)

class RegPersonsOrgUnitsTestCase(TestCase):

    def test_date_linked_label(self):
        personsunit = RegPersonsOrgUnits.objects.get(id=1)
        field_label = personsunit._meta.get_field('date_linked').verbose_name
        self.assertEqual(field_label, 'linked')

    def test_date_delinked_label(self):
        personsunit = RegPersonsOrgUnits.objects.get(id=1)
        field_label = personsunit._meta.get_field('date_delinked').verbose_name
        self.assertEqual(field_label, 'delinked')

class RegPersonsWorkforceIdsTestCase(TestCase):

    def test_workforce_id_label(self):
        workforce = RegPersonsWorkforceIds.objects.get(id=1)
        field_label = workforce._meta.get_field('workforce_id').verbose_name
        self.assertEqual(field_label, 'workforce id')

    def test_workforce_id_max_length(self):
        workforce = RegPersonsWorkforceIds.objects.get(id=1)
        max_length = workforce._meta.get_field('workforce_id').max_length
        self.assertEqual(max_length, 8)

class RegPersonsBeneficiaryIdsTestCase(TestCase):

    def test_workforce_id_label(self):
        beneficiary = RegPersonsBeneficiaryIds.objects.get(id=1)
        field_label = beneficiary._meta.get_field('beneficiary_id').verbose_name
        self.assertEqual(field_label, 'beneficiary id')

    def test_workforce_id_max_length(self):
        beneficiary = RegPersonsBeneficiaryIds.objects.get(id=1)
        max_length = beneficiary._meta.get_field('beneficiary_id').max_length
        self.assertEqual(max_length, 10)

class RegOrgUnitsAuditTrailTestCase(TestCase):

    def test_transaction_type_id_label(self):
        audit_trail = RegOrgUnitsAuditTrail.objects.get(id=1)
        field_label = audit_trail._meta.get_field('transaction_type_id').verbose_name
        self.assertEqual(field_label, 'transaction type')

    def test_transaction_type_id_max_length(self):
        audit_trail = RegOrgUnitsAuditTrail.objects.get(id=1)
        max_length = audit_trail._meta.get_field('transaction_type_id').max_length
        self.assertEqual(max_length, 4)

    def test_interface_id_label(self):
        audit_trail = RegOrgUnitsAuditTrail.objects.get(id=1)
        field_label = audit_trail._meta.get_field('interface_id').verbose_name
        self.assertEqual(field_label, 'interface id')

    def test_interface_id_max_length(self):
        audit_trail = RegOrgUnitsAuditTrail.objects.get(id=1)
        max_length = audit_trail._meta.get_field('interface_id').max_length
        self.assertEqual(max_length, 4)

class RegPersonsAuditTrailTestCase(TestCase):

    def test_transaction_type_id_label(self):
        PersonAudit = RegPersonsAuditTrail.objects.get(id=1)
        field_label = PersonAudit._meta.get_field('transaction_type_id').verbose_name
        self.assertEqual(field_label, 'transaction type')

    def test_transaction_type_id_max_length(self):
        PersonAudit = RegPersonsAuditTrail.objects.get(id=1)
        max_length = PersonAudit._meta.get_field('transaction_type_id').max_length
        self.assertEqual(max_length, 4)

    def test_interface_id_label(self):
        PersonAudit = RegPersonsAuditTrail.objects.get(id=1)
        field_label = PersonAudit._meta.get_field('interface_id').verbose_name
        self.assertEqual(field_label, 'interface id')

    def test_interface_id_max_length(self):
        PersonAudit = RegPersonsAuditTrail.objects.get(id=1)
        max_length = PersonAudit._meta.get_field('interface_id').max_length
        self.assertEqual(max_length, 4)

    def test_date_recorded_paper_label(self):
        PersonAudit = RegPersonsAuditTrail.objects.get(id=1)
        field_label = PersonAudit._meta.get_field('date_recorded_paper').verbose_name
        self.assertEqual(field_label, 'date recorded paper')

class OVCSiblingTestCase(TestCase):

    def test_first_name_label(self):
        sibling = OVCSibling.objects.get(id=1)
        field_label = sibling._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_first_name_max_length(self):
        sibling = OVCSibling.objects.get(id=1)
        max_length = sibling._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 50)

    def test_other_names_label(self):
        sibling = OVCSibling.objects.get(id=1)
        field_label = sibling._meta.get_field('other_names').verbose_name
        self.assertEqual(field_label, 'other names')

    def test_other_names_max_length(self):
        sibling = OVCSibling.objects.get(id=1)
        max_length = sibling._meta.get_field('other_names').max_length
        self.assertEqual(max_length, 50)

    def test_surname_label(self):
        sibling = OVCSibling.objects.get(id=1)
        field_label = sibling._meta.get_field('surname').verbose_name
        self.assertEqual(field_label, 'surname')

    def test_surname_max_length(self):
        sibling = OVCSibling.objects.get(id=1)
        max_length = sibling._meta.get_field('surname').max_length
        self.assertEqual(max_length, 50)

    def test_date_of_birth_label(self):
        sibling = OVCSibling.objects.get(id=1)
        field_label = sibling._meta.get_field('date_of_birth').verbose_name
        self.assertEqual(field_label, 'date of birth')

    def test_sex_id_label(self):
        sibling = OVCSibling.objects.get(id=1)
        field_label = sibling._meta.get_field('sex_id').verbose_name
        self.assertEqual(field_label, 'sex id')

    def test_sex_id_max_length(self):
        sibling = OVCSibling.objects.get(id=1)
        max_length = sibling._meta.get_field('sex_id').max_length
        self.assertEqual(max_length, 4)

    def test_class_level_label(self):
        sibling = OVCSibling.objects.get(id=1)
        field_label = sibling._meta.get_field('class_level').verbose_name
        self.assertEqual(field_label, 'class level')

    def test_class_level_max_length(self):
        sibling = OVCSibling.objects.get(id=1)
        max_length = sibling._meta.get_field('class_level').max_length
        self.assertEqual(max_length, 50)

    def test_remarks_label(self):
        sibling = OVCSibling.objects.get(id=1)
        field_label = sibling._meta.get_field('remarks').verbose_name
        self.assertEqual(field_label, 'remarks')

    def test_remarks_max_length(self):
        sibling = OVCSibling.objects.get(id=1)
        max_length = sibling._meta.get_field('remarks').max_length
        self.assertEqual(max_length, 50)

#class OVCCheckinTestCase(TestCase)

#class OVCHouseHoldTestcase(TestCase)

class PersonsMasterTestCase(TestCase):

    def test_person_type_label(self):
        master = PersonsMaster.objects.get(id=1)
        field_label = master._meta.get_field('person_type').verbose_name
        self.assertEqual(field_label, 'person type')

    def test_person_type_max_length(self):
        master = PersonsMaster.objects.get(id=1)
        max_length = master._meta.get_field('person_type').max_length
        self.assertEqual(max_length, 5)

    def test_system_id_label(self):
        master = PersonsMaster.objects.get(id=1)
        field_label = master._meta.get_field('system_id').verbose_name
        self.assertEqual(field_label, 'system id')

    def test_system_id_max_length(self):
        master = PersonsMaster.objects.get(id=1)
        max_length = master._meta.get_field('system_id').max_length
        self.assertEqual(max_length, 50)













start_date = '2002-01-01'
fmt = '%Y-%m-%d'

new_date = datetime.strptime(start_date, fmt)
todate = datetime.now()

print(new_date)
