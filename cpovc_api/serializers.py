"""Serializers for the test API."""
from cpovc_auth.models import AppUser
from cpovc_registry.models import RegOrgUnit
from rest_framework import serializers
from cpovc_main.models import SetupList, SetupGeography
from cpovc_forms.models import OVCBasicCRS, OVCBasicCategory, OVCBasicPerson
from . import Country


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """User serializer."""

    class Meta:
        """Overrride parameters."""

        model = AppUser
        fields = ('first_name', 'surname', 'id')


class OrgUnitSerializer(serializers.HyperlinkedModelSerializer):
    """Organisation Unit serializer."""

    class Meta:
        """Overrride parameters."""

        model = RegOrgUnit
        fields = ('id', 'org_unit_id_vis', 'org_unit_name',
                  'org_unit_type_id')
        read_only_fields = ('org_unit_id_vis', 'org_unit_name')


class SettingsSerializer(serializers.HyperlinkedModelSerializer):
    """User serializer."""

    class Meta:
        """Overrride parameters."""

        model = SetupList
        fields = ('item_id', 'item_description',
                  'item_sub_category', 'the_order')


class GeoSerializer(serializers.HyperlinkedModelSerializer):
    """User serializer."""

    class Meta:
        """Overrride parameters."""

        model = SetupGeography
        fields = ('area_id', 'area_type_id', 'area_code',
                  'area_name', 'parent_area_id')


class CRSSerializer(serializers.ModelSerializer):
    """Case Serializer."""

    class Meta:
        model = OVCBasicCRS
        fields = ('case_id', 'case_serial', 'case_reporter',
                  'reporter_telephone', 'reporter_county',
                  'reporter_sub_county', 'reporter_ward',
                  'reporter_village', 'case_date', 'perpetrator',
                  'county', 'constituency', 'organization_unit',
                  'case_landmark', 'hh_economic_status', 'family_status',
                  'mental_condition', 'physical_condition', 'other_condition',
                  'risk_level', 'referral', 'summon', 'case_narration',
                  'account', 'case_params', 'longitude', 'latitude')


class CRSCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OVCBasicCategory
        fields = ('category_id', 'case_category', 'case_sub_category',
                  'case_date_event', 'case_nature', 'case_place_of_event',
                  'case')


class CRSPersonserializer(serializers.ModelSerializer):
    class Meta:
        model = OVCBasicPerson
        fields = ('person_id', 'relationship', 'person_type',
                  'first_name', 'surname', 'other_names',
                  'dob', 'sex', 'case')


class CountrySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    code = serializers.CharField(max_length=2)
    name = serializers.CharField(max_length=256)

    def create(self, validated_data):
        return Country(id=None, **validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance
