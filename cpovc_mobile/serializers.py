from django.db import models
from rest_framework import serializers

from cpovc_forms.models import OVCCaseRecord, OVCCaseCategory
from cpovc_registry.models import RegPerson, RegPersonsGuardians, RegPersonsSiblings


class PerpetratorField(serializers.Field):

    def to_representation(self, value):
        ret = {
            "first_name": value.perpetrator_first_name,
            "surname": value.perpetrator_surname,
            "ovc_other_names": value.perpetrator_other_names,
            "relationship_type": value.perpetrator_relationship_type
        }
        return [ret]

class CaseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OVCCaseCategory
        fields = ['case_category', 'date_of_event', 'case_nature',
                  'place_of_event']

class CaseRecordSerializer(serializers.ModelSerializer):
    # categories = CaseCategorySerializer(many=True, read_only=True)
    ovc_cpims_id = serializers.IntegerField(source='person.id')
    ovc_first_name = serializers.CharField(source='person.first_name')
    ovc_surname = serializers.CharField(source='person.surname')
    ovc_other_names = serializers.CharField(source='person.other_names')
    ovc_sex = serializers.CharField(source='person.sex_id')


    caregivers = serializers.SerializerMethodField(source='get_caregivers')
    siblings = serializers.SerializerMethodField(source='get_siblings')
    case_categories = serializers.SerializerMethodField(source='get_case_categories')
    perpetrators = PerpetratorField(source='*')

    class Meta:
        model = OVCCaseRecord
        fields = ['case_id', 'case_serial', 'case_reporter',
                  'ovc_cpims_id', 'ovc_first_name', 'ovc_surname',
                  'ovc_other_names', 'ovc_sex',
                  'perpetrator_status', 'perpetrators',
                  'risk_level', 'date_case_opened',
                  'case_status', 'case_categories', 'case_remarks',
                  'caregivers', 'siblings']

    def get_caregivers(self, obj):
        # Get Caregivers
        cgs = {'caregiver_cpims_id':'guardian_person_id',
               'relationship_type': 'relationship'
               }
        caregivers = RegPersonsGuardians.objects.filter(
            is_void=False, child_person_id=obj.person.id).extra(
            select=cgs)
        return caregivers.values(
            'caregiver_cpims_id', 'guardian_person', 'date_linked', 'relationship_type')

    def get_siblings(self, obj):
        # Get siblings
        siblings = RegPersonsSiblings.objects.filter(
            is_void=False, child_person_id=obj.person.id)
        return siblings.values()


    def get_case_categories(self, obj):
        # Get Categories
        categories = OVCCaseCategory.objects.filter(
            is_void=False, case_id_id=obj.case_id)
        return categories.values(
            'case_category', 'date_of_event', 'place_of_event', 'case_nature')
