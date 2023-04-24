import uuid
from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.shortcuts import get_object_or_404
from .serializers import (
    UserSerializer, OrgUnitSerializer, SettingsSerializer, GeoSerializer,
    CRSSerializer, CountrySerializer, CRSPersonserializer,
    CRSCategorySerializer, SchoolSerializer, FacilitySerializer)
from cpovc_auth.models import AppUser
from cpovc_registry.models import RegOrgUnit
from cpovc_main.models import SetupList, SetupGeography
from cpovc_forms.models import OVCBasicCRS, OVCBasicCategory, OVCBasicPerson
from cpovc_main.country import COUNTRIES as CLISTS

from cpovc_ovc.models import OVCFacility, OVCSchool, OVCRegistration, OVCHealth
from . import Country


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint that allows users to be viewed or edited."""

    queryset = AppUser.objects.all().order_by('-last_login')[:10]
    serializer_class = UserSerializer


class CountryViewSet(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    permission_classes = []
    serializer_class = CountrySerializer

    def list(self, request):
        countries = {}
        cnt = 0
        for ccode in CLISTS:
            cnt += 1
            print(ccode)
            cname = CLISTS[ccode].encode()
            countries[cnt] = Country(id=cnt, code=ccode, name=cname)
        serializer = CountrySerializer(
            instance=countries.values(), many=True)
        return Response(serializer.data)


class SettingsViewSet(generics.ListAPIView):
    permission_classes = []
    serializer_class = SettingsSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned values to a given prameter.
        """
        queryset = SetupList.objects.all()
        field_name = self.request.query_params.get(
            'field_name', 'case_category_id')
        if field_name is not None:
            queryset = queryset.filter(field_name=field_name)
        return queryset


class GeoViewSet(generics.ListAPIView):
    permission_classes = []
    serializer_class = GeoSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned values to a given prameter.
        """
        queryset = SetupGeography.objects.all()
        field_name = self.request.query_params.get('area_type_id', None)
        parent_id = self.request.query_params.get('parent_area_id', None)
        if field_name is not None:
            queryset = queryset.filter(area_type_id=field_name)
        if parent_id is not None:
            queryset = queryset.filter(parent_area_id=parent_id)
        return queryset


class OrgUnitViewSet(generics.ListAPIView):
    permission_classes = []
    serializer_class = OrgUnitSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned values to a given prameter.
        """
        queryset = RegOrgUnit.objects.filter(
            is_void=False).order_by('org_unit_name')
        unit_type_id = self.request.query_params.get('org_unit_type_id', None)
        parent_id = self.request.query_params.get('parent_org_unit_id', None)
        if unit_type_id is not None:
            queryset = queryset.filter(org_unit_type_id=unit_type_id)
        if parent_id is not None:
            queryset = queryset.filter(parent_org_unit_id=parent_id)
        return queryset


class SchoolViewSet(generics.ListAPIView):
    permission_classes = []
    serializer_class = SchoolSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned values to a given prameter.
        """
        queryset = OVCSchool.objects.filter(
            is_void=False).order_by('school_name')
        unit_id = self.request.query_params.get('id', None)
        unit_level = self.request.query_params.get('school_level', None)
        start = int(self.request.query_params.get('start', 0))
        limit = int(self.request.query_params.get('limit', 1000))
        if unit_id is not None:
            queryset = queryset.filter(id=unit_id)
        if unit_level is not None:
            queryset = queryset.filter(school_level=unit_level)
        return queryset[start:limit]


class HealthFacilityViewSet(generics.ListAPIView):
    permission_classes = []
    serializer_class = FacilitySerializer

    def get_queryset(self):
        """
        Optionally restricts the returned values to a given prameter.
        """
        queryset = OVCFacility.objects.filter(
            is_void=False).order_by('facility_name')
        unit_id = self.request.query_params.get('id', None)
        unit_code = self.request.query_params.get('facility_code', None)
        start = int(self.request.query_params.get('start', 0))
        limit = int(self.request.query_params.get('limit', 1000))
        if unit_id is not None:
            queryset = queryset.filter(id=unit_id)
        if unit_code is not None:
            queryset = queryset.filter(facility_code=unit_code)
        return queryset[start:limit]


class BasicCRSView(generics.ListAPIView):
    # queryset = OVCBasicCRS.objects.all()
    serializer_class = CRSSerializer

    def create(self, serializer):
        author = get_object_or_404(
            AppUser, id=self.request.data.get('author_id'))
        return serializer.save(author=author)

    def get(self, request, *args, **kwargs):
        # return self.list(request, *args, **kwargs)
        return Response({'message': "Listing not available"})

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@api_view(['GET', 'POST'])
def basic_crs(request):
    try:
        print(request.method)
        if request.method == 'GET':
            account_id = request.user.id
            queryset = OVCBasicCRS.objects.filter(account=account_id)
            case_id = request.query_params.get('case_id')
            if case_id:
                queryset = queryset.filter(case_id=case_id)
            if queryset:
                cases = list(queryset.values())[0]
                qs = OVCBasicCategory.objects.filter(case_id=case_id)
                ps = OVCBasicPerson.objects.filter(case_id=case_id)
                categories = list(qs.values())
                persons = list(ps.values())
                cases['categories'] = []
                cases['caregivers'] = []
                cases['perpetrators'] = []
                cases['children'] = []
                cases['reporters'] = []
                del cases['is_void']
                for category in categories:
                    del category['category_id']
                    del category['is_void']
                    cases['categories'].append(category)
                for person in persons:
                    del person['case_id']
                    del person['person_id']
                    del person['is_void']
                    ptype = person['person_type']
                    if ptype == 'PTPD':
                        cases['perpetrators'].append(person)
                    if ptype == 'PTCG':
                        cases['caregivers'].append(person)
                    if ptype == 'PTCH':
                        cases['children'].append(person)
                    if ptype == 'PTRD':
                        cases['reporters'].append(person)
                return Response(cases)
            else:
                return Response({'details': 'Case Does not Exist'})
        # Insert a new record for CRS
        elif request.method == 'POST':
            # print (request.user.username)
            case_uid = uuid.uuid1()
            account_id = request.user.id
            perpetrators = request.data.get('perpetrators')
            perpetrator = request.data.get('perpetrator')
            caregivers = request.data.get('caregivers')
            reporter = request.data.get('reporter')
            reporter_tel = request.data.get('reporter_telephone')
            lon = request.data.get('longitude')
            lat = request.data.get('latitude')
            hes = request.data.get('hh_economic_status')
            risk_level = request.data.get('risk_level')
            physical_condition = request.data.get('physical_condition')
            family_statuses = request.data.get('family_status')
            case_id = request.data.get('case_id', case_uid)
            print('lon', lon, 'lat', lat)
            print('-*-' * 50)
            print(request.data)
            print('-*-' * 50)
            print(request.META)
            print('-*-' * 50)
            family_status = family_statuses.split(
                ',')[0] if family_statuses else ''
            data = {'case_category': request.data.get('case_category'),
                    'county': request.data.get('county'),
                    'constituency': request.data.get('constituency'),
                    'child_dob': request.data.get('child_dob'),
                    'perpetrator': perpetrator,
                    'case_landmark': request.data.get('case_landmark'),
                    'case_narration': request.data.get('case_narration'),
                    'child_sex': request.data.get('child_sex'),
                    'reporter_telephone': reporter_tel,
                    'case_reporter': request.data.get('case_reporter'),
                    'organization_unit': request.data.get('organization_unit'),
                    'hh_economic_status': hes,
                    'family_status': family_status,
                    'mental_condition': request.data.get('mental_condition'),
                    'physical_condition': physical_condition,
                    'other_condition': request.data.get('other_condition'),
                    'case_date': request.data.get('case_date'),
                    'case_params': str(request.data), 'case_id': case_id,
                    'account': account_id, "risk_level": risk_level
                    }
            if lon and lat:
                data["longitude"] = round(Decimal(float(lon)), 7)
                data["latitude"] = round(Decimal(float(lat)), 7)
            print(data)
            case_data = OVCBasicCRS(case_id=case_id)
            if case_data:
                serializer = CRSSerializer(case_data, data=data)
            else:
                serializer = CRSSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                case_id = serializer.data['case_id']
                case_details = request.data.get('case_details')
                for case in case_details:
                    category = case['category']
                    sub_category = None
                    if 'sub_category' in case:
                        sub_category = case['sub_category']
                    print('CASE', category, case)
                    cat_data = {'case': case_id, 'case_category': category,
                                'case_date_event': case['date_of_event'],
                                'case_nature': case['nature_of_event'],
                                'case_place_of_event': case['place_of_event'],
                                'case_sub_category': sub_category}
                    cserializer = CRSCategorySerializer(data=cat_data)
                    if cserializer.is_valid():
                        cserializer.save()
                    else:
                        print(cserializer.errors)
                if perpetrator == 'PKNW':
                    for data in perpetrators:
                        save_person(case_id, 'PTPD', data)
                if caregivers:
                    for data in caregivers:
                        save_person(case_id, 'PTCG', data)
                if reporter != 'CRSF':
                    save_person(case_id, 'PTRD', request.data)
                # Child details
                save_person(case_id, 'PTCH', request.data)
                print('CASE OK', serializer.data)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                print('CASE ERROR', serializer.errors)
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print('Error submitting API Case - %s' % str(e))
        return Response({'details': 'Error saving Case details'})


@csrf_exempt
def basic_mobi_crs(request):
    """Method for Mobile devices."""
    try:
        print(request.POST)
        results = {'results': 'This is good'}
        return JsonResponse(results, content_type='application/json',
                            safe=False)
    except Exception as e:
        results = {'results': 'There was an error - %s' % str(e)}
        print(results)
        return JsonResponse(results, content_type='application/json',
                            safe=False)


def save_person(case_id, person_type, req_data):
    try:
        if person_type == 'PTCH':
            data = {'first_name': req_data.get('child_first_name')}
            data['surname'] = req_data.get('child_surname')
            data['other_names'] = req_data.get('child_other_names')
            data['dob'] = req_data.get('child_dob')
            data['sex'] = req_data.get('child_sex')
            data['relationship'] = 'TBVC'
        elif person_type == 'PTRD':
            data = {'first_name': req_data.get('reporter_first_name')}
            data['surname'] = req_data.get('reporter_surname')
            data['other_names'] = req_data.get('reporter_other_names')
            data['dob'] = req_data.get('reporter_dob')
            data['sex'] = req_data.get('reporter_sex')
            data['relationship'] = req_data.get('relation')
        else:
            data = req_data
        data['person_type'] = person_type
        data['case'] = case_id
        # print data
        serializer = CRSPersonserializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            print(person_type, serializer.errors)
    except Exception as e:
        print('Error saving data - %s' % str(e))
        pass


def get_settings(request, param='', filter_id=''):
    """Method to get settings."""
    try:
        param_id = request.POST.get('domain', None)
        # case_id = request.POST.get('case_id')
        results = {}
        itm = {'item_id': '', 'item_name': 'Please Select'}
        goals, gaps, services = [itm], [itm], [itm]
        if param_id:
            itms = SetupList.objects.filter(
                item_id=param_id, field_name__istartswith='afc_domain')
            field_name = itms[0].field_name
            field_sub_cat = itms[0].item_sub_category
            print('field name', field_name, field_sub_cat)
            goals_id = '%s_goals' % (field_sub_cat)
            gaps_id = '%s_gaps' % (field_sub_cat)
            services_id = '%s_services' % (field_sub_cat)
            itms_id = [goals_id, gaps_id, services_id]
            items = SetupList.objects.filter(field_name__in=itms_id)
            for item in items:
                item_id = item.item_id
                item_name = item.item_description
                item_field = item.field_name
                print('Field', item_field)
                itm_dict = {'item_id': item_id, 'item_name': item_name}
                if item_field == goals_id:
                    goals.append(itm_dict)
                if item_field == gaps_id:
                    gaps.append(itm_dict)
                if item_field == services_id:
                    services.append(itm_dict)
        results['goals'] = goals
        results['gaps'] = gaps
        results['services'] = services
        print(results)
    except Exception:
        return JsonResponse([], content_type='application/json',
                            safe=False)
    else:
        return JsonResponse(results, content_type='application/json',
                            safe=False)


@api_view(['GET', 'POST'])
def dreams(request):
    """Method to handle DREAMS."""
    try:
        results = {}
        if request.method == 'GET':
            ovc_id = request.query_params.get('cpims_id')
            dreams_id = request.query_params.get('dreams_id')
            print('ID', ovc_id)
            if dreams_id:
                print('Get the corresponding cpims id from ext ids')
            qs = OVCRegistration.objects.filter(
                person_id=ovc_id, is_void=False)
            if qs:
                queryset = qs[0]
                if queryset.hiv_status == 'HSTP':
                    health = OVCHealth.objects.get(
                        person_id=ovc_id, is_void=False)
                    if health:
                        facility_name = health.facility.facility_name
                        results['ccc_number'] = health.ccc_number
                        results['date_of_linkage'] = health.date_linked
                        results['facility_name'] = facility_name
                results['registration_date'] = queryset.registration_date
                msg = 'OVC details Found'
            else:
                msg = 'OVC details Found'
        else:
            msg = 'Method not Implemented'
        results['details'] = msg
    except Exception as e:
        msg = 'Error getting OVC details - %s' % (str(e))
        return Response({'details': msg})
    else:
        return Response(results)
