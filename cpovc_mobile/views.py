import json
import uuid
from decimal import Decimal
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib import messages
from rest_framework import viewsets, generics, status
from django.core.paginator import Paginator

from rest_framework.views import APIView

from cpovc_api.functions import dcs_dashboard, get_attached_orgs
from cpovc_forms.models import OVCCaseRecord, OVCCaseGeo

from cpovc_mobile.models import OVCBasicCRSMobile, OVCBasicCategoryMobile, OVCBasicPersonMobile
from cpovc_mobile.serializers import CRSCategorySerializerMobile, CRSPersonserializerMobile, CRSSerializerMobile, CaseRecordSerializer, MobileUserSerializer
from cpovc_registry.models import RegOrgUnit



# functions
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
        serializer = CRSPersonserializerMobile(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            print(person_type, serializer.errors)
    except Exception as e:
        print('Error saving data - %s' % str(e))
        passfrom django.shortcuts import render, redirect
from cpovc_forms.views import forms_registry

from django.contrib.auth.decorators import login_required

from cpovc_registry.models import (AppUser, RegPerson, RegPersonsSiblings, RegPersonsGuardians, )
from cpovc_forms.models import (OVCEconomicStatus, OVCFamilyStatus, OVCFriends, OVCHobbies,OVCMedical, OVCCaseCategory,
                                OVCNeeds, OVCReferral, OVCMedicalSubconditions, OVCCaseSubCategory,OVCCaseLocation, OvcCasePersons,)

from cpovc_main.functions import (get_dict, translate)


@api_view(["POST", "GET"])
def ovc_mobile_home(request):
    """Method to handle Mobile endpoints."""
    try:
        return Response(
            {"message": "Method not allowed"}, status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        raise e
    else:
        pass


class CaseloadViewSet(generics.ListAPIView):
    serializer_class = CaseRecordSerializer

    def get_queryset(self):
        """
        This view should return a list of all the cases
        for the currently authenticated user.
        """
        user = self.request.user
        cases = OVCCaseGeo.objects.filter(is_void=False).values("case_id_id")[:10]
        case_obj = OVCCaseRecord.objects.filter(case_id__in=cases, case_status="ACTIVE")
        return case_obj


# @api_view(["POST", 'PUT', 'PATCH', 'DELETE'])
# def ovc_mobile_crs(request):
#     """Method to handle Mobile CRS endpoints."""
#     try:
#         results = {"message": "Saved Successfull"}

#         return(Response(results, status=201 ))
#     except Exception as e:
#         raise e
#     else:
#         pass


@api_view(['GET', 'POST', 'PATCH'])
def ovc_mobile_crs(request):
    try:
        print(request.method)
        if request.method == 'GET':
            account_id = request.user.id
            queryset = OVCBasicCRSMobile.objects.filter(account=account_id,is_accepted=1).values()
            case_id = request.query_params.get('case_id')
            if case_id:
                queryset = queryset.filter(case_id=case_id,account=account_id,is_accepted=1)
            response_list = []
            if queryset:
                for  query in queryset:
                    cases = query
                    print("cases...........",cases['app_form_metadata'])
                    
                    qs = OVCBasicCategoryMobile.objects.filter(case_id=case_id)
                    ps = OVCBasicPersonMobile.objects.filter(case_id=case_id)
                    categories = list(qs.values())
                    persons = list(ps.values())
                    cases['categories'] = []
                    cases['caregivers'] = []
                    cases['perpetrators'] = []
                    cases['children'] = []
                    cases['reporters'] = []
                    cases['app_form_metadata'] = json.loads(cases['app_form_metadata'].replace("'", "\""))
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
                    response_list.append(cases)
                #paginate
                paginator = Paginator(response_list, 50)
                page_number = request.GET.get("page")
                page_obj = paginator.get_page(page_number)
                current_page = list(page_obj)
                
                return Response({
                "results": current_page,
                "page": page_obj.number,
                "total_pages": paginator.num_pages
                })
                
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
                    'account': account_id, "risk_level": risk_level,
                    'app_form_metadata':json.dumps(request.data.get('app_form_metadata'))
                    }
            if lon and lat:
                data["longitude"] = round(Decimal(float(lon)), 7)
                data["latitude"] = round(Decimal(float(lat)), 7)
            print(data)
            case_data = OVCBasicCRSMobile(case_id=case_id)
            if case_data:
                serializer = CRSSerializerMobile(case_data, data=data)
            else:
                serializer = CRSSerializerMobile(data=data)
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
                    cserializer = CRSCategorySerializerMobile(data=cat_data)
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
        # update 
        elif request.method == 'PATCH':
            case_id = request.data.get('case_id')
            is_accepted = request.data.get('is_accepted')
            case_data = OVCBasicCRSMobile.objects.get(case_id=case_id)
            case_data.is_accepted = is_accepted
            
            case_data.save()
            return Response({'Case Updated': 'Is accepted field updated'},)
    
    except Exception as e:
        print('Error submitting API Case - %s' % str(e))
        return Response({'details': 'Error saving Case details'})


@api_view(['POST', 'PUT', 'PATCH', 'DELETE'])
def ovc_mobile_follow_up(request):
    """Method to handle Mobile CRS endpoints."""
    try:
        results = {"message": "Saved Successfull"}

        return Response(results, status=201)
    except Exception as e:
        raise e
    else:
        pass


@api_view(["POST", 'PUT', 'PATCH', 'DELETE'])
def ovc_mobile_forms(request):
    """Method to handle Mobile CRS endpoints."""
    try:
        results = {"message": "Saved Successfull"}

        return Response(results, status=201)
    except Exception as e:
        raise e
    else:
        pass


# Mobile approval loading
@login_required
def mobile_app_home(request):
    print(f"user id id {request.user.id}")
    context = {
        "cases": [
            {
                "id": "749fc18f2cbf11efb24922a3499bfe31",
                "care_id": "749fc18f2cbf11efb24922a3499bfe33",
                "case": "CCO/47/287/5/29/4423/2024",
                "first_name": "Boniface",
                "case_date": "2024-01-01",
                "case_level": 2,
            },
            {
                "id": "749fc18f2cbf11efb24922a3499bfe32",
                "care_id": "2323",
                "case": "CCO/47/287/5/29/4425/2024",
                "first_name": "John",
                "case_date": "2024-01-01",
                "case_level": 2,
            },
            {
                "id": "749fc18f2cbf11efb24922a3499bfe33",
                "care_id": "2323",
                "case": "CCO/47/287/5/29/4426/2024",
                "first_name": "Jane",
                "case_date": "2024-01-01",
                "case_level": 2,
            },
            {
                "id": "749fc18f2cbf11efb24922a3499bfe33",
                "care_id": "2323",
                "case": "CCO/47/287/5/29/4427/2024",
                "first_name": "Jude",
                "case_date": "2024-01-01",
                "case_level": 2,
            },
        ]
    }
    return render(request, "mobile/home.html", context=context)


def view_mobile_case_record_sheet(request, id):
    # csr_id = id
    # print(f"CSR-ID: {csr_id}")
    # context = {
       
    # }
    # return render(request, "mobile/preview_csr.html", context=context)
    try:
        """Get Initial Data"""
        # f = FormsLog.objects.get(form_id=id, is_void=False)
        ovccr = OVCCaseRecord.objects.get(case_id=id, is_void=False)
        person_id = int(ovccr.person_id)
        # init_data = RegPerson.objects.filter(pk=person_id)
        appuser = AppUser.objects.filter(pk=ovccr.created_by).first()
        f = {'form_id': id}

        # Get Siblings
        init_data = RegPerson.objects.filter(pk=person_id)
        reg_personsiblings = []

        regpersonsiblings = RegPersonsSiblings.objects.filter(
            child_person_id=person_id)
        for regpersonsibling in regpersonsiblings:
            reg_personsiblings.append(regpersonsibling.sibling_person)
        init_data.siblingpersons = reg_personsiblings

        reg_caregivers = []
        caregivers = RegPersonsGuardians.objects.filter(
            child_person_id=person_id)
        for caregiver in caregivers:
            caregiver_details = caregiver.guardian_person
            setattr(caregiver_details, 'relation', caregiver.relationship)
            reg_caregivers.append(caregiver_details)
        init_data.caregivers = reg_caregivers

        check_fields = ['sex_id',
                        'family_status_id',
                        'household_economics',
                        'mental_condition_id',
                        'mental_subcondition_id',
                        'physical_condition_id',
                        'physical_subcondition_id',
                        'other_condition_id',
                        'other_subcondition_id',
                        'case_reporter_id',
                        'perpetrator_status_id',
                        'relationship_type_id',
                        'perpetrator_id', 'risk_level_id',
                        'referral_destination_id',
                        'intervention_id',
                        'case_category_id', 'core_item_id',
                        'yesno_id', 'relationship_type_id',
                        'case_reporter_relationship_to_child',
                        'long_term_support_id',
                        'immediate_need_id']

        vals = get_dict(field_name=check_fields)

        ovcd = OVCEconomicStatus.objects.get(case_id=id, is_void=False)
        ovcfam = OVCFamilyStatus.objects.filter(case_id=id, is_void=False)
        ovccr = OVCCaseRecord.objects.get(case_id=id, is_void=False)
        ovcgeo = OVCCaseGeo.objects.get(case_id=id, is_void=False)
        ovcfrnds = OVCFriends.objects.filter(case_id=id, is_void=False)
        ovchobs = OVCHobbies.objects.filter(case_id=id, is_void=False)
        ovcmed = OVCMedical.objects.get(case_id=id, is_void=False)
        ovcccats = OVCCaseCategory.objects.filter(case_id=id, is_void=False)
        ovcneeds = OVCNeeds.objects.filter(case_id=id, is_void=False)
        ovcrefa = OVCReferral.objects.filter(case_id=id, is_void=False)
        perpetrators = OvcCasePersons.objects.filter(
            case_id=id, person_type='PERP')
        ovclocs = OVCCaseLocation.objects.filter(case_id=id, is_void=False)

        # Retrieve Medical Subconditions
        medical_id = ovcmed.medical_id
        ovcphymeds = OVCMedicalSubconditions.objects.filter(
            medical_id=medical_id, medical_condition='Physical', is_void=False)
        ovcmentmeds = OVCMedicalSubconditions.objects.filter(
            medical_id=medical_id, medical_condition='Mental', is_void=False)
        ovcothermeds = OVCMedicalSubconditions.objects.filter(
            medical_id=medical_id, medical_condition='Other', is_void=False)

        # Get OVCCaseCategory
        case_grouping_ids = []
        jsonCategorysData = []
        jsonSubCategorysData = []
        str_jsonsubcategorydata = ''
        resultsets = []
        ovcccats = OVCCaseCategory.objects.filter(
            case_id=id, is_void=False)
        """ Get case_grouping_ids[] """
        for ovcccat in ovcccats:
            case_grouping_id = str(ovcccat.case_grouping_id)
            if not case_grouping_id in case_grouping_ids:
                case_grouping_ids.append(str(case_grouping_id))

        """ Get Case Categories """
        ovcccats2 = None
        for case_grouping_id in case_grouping_ids:
            ovcccats2 = OVCCaseCategory.objects.filter(
                case_grouping_id=case_grouping_id)

            for ovcccat in ovcccats2:
                # OVCCaseSubCategory
                ovccasesubcategorys = OVCCaseSubCategory.objects.filter(
                    case_grouping_id=case_grouping_id)
                for ovccasesubcategory in ovccasesubcategorys:
                    jsonSubCategorysData.append(
                        translate(str(ovccasesubcategory.sub_category_id)))
                str_jsonsubcategorydata = ','.join(jsonSubCategorysData)

                jsonCategorysData.append({'case_category': ovcccat.case_category,
                                          'case_subcategorys': str_jsonsubcategorydata,
                                          'date_of_event': (ovcccat.date_of_event).strftime('%d-%b-%Y'),
                                          'place_of_event': ovcccat.place_of_event,
                                          'case_nature': ovcccat.case_nature,
                                          'case_grouping_id': str(ovcccat.case_grouping_id)
                                          })
                jsonSubCategorysData = []

        """ Create resultsets """
        resultsets.append(jsonCategorysData)

        # Get OVCReferral
        jsonData2 = []
        resultsets2 = []
        referral_grouping_ids = []
        """ Get referral_grouping_ids[] """
        for reffs in ovcrefa:
            referral_grouping_id = str(reffs.referral_grouping_id)
            if not referral_grouping_id in referral_grouping_ids:
                referral_grouping_ids.append(str(referral_grouping_id))
        """ Get Referral Actors """
        ovcrefa2 = None
        for referral_grouping_id in referral_grouping_ids:
            ovcrefa2 = OVCReferral.objects.filter(
                referral_grouping_id=referral_grouping_id)
            for ra in ovcrefa2:
                jsonData2.append({'refferal_actor_type': translate(ra.refferal_actor_type),
                                  'refferal_actor_specify': ra.refferal_actor_specify,
                                  'refferal_to': translate(ra.refferal_to),
                                  'referral_grouping_id': str(ra.referral_grouping_id)
                                  })
        resultsets2.append(jsonData2)

        return render(request,
                      'mobile/preview_csr.html',
                      {'init_data': init_data,
                       'vals': vals, 'result': f,
                       'ovcd': ovcd,
                       'ovccr': ovccr,
                       'ovcgeo': ovcgeo,
                       'ovcfrnds': ovcfrnds,
                       'ovchobs': ovchobs,
                       'ovcmed': ovcmed,
                       'ovcphymeds': ovcphymeds,
                       'ovcmentmeds': ovcmentmeds,
                       'ovcothermeds': ovcothermeds,
                       'ovcneeds': ovcneeds,
                       'perpetrators': perpetrators,
                       'ovcfam': ovcfam,
                       'resultsets': resultsets,
                       'resultsets2': resultsets2,
                       'ovclocs': ovclocs.first(),
                       'app_user': appuser
                       })
    except Exception as e:
        msg = 'An error occured trying to view OVCCaseRecord - %s' % (str(e))
        messages.add_message(request, messages.ERROR, msg)
    redirect_url = reverse(forms_registry)
    return HttpResponseRedirect(forms_registry)
    # return render(request, "mobile/home.html", {})



class MobileUser(APIView):

    serializer_class = MobileUserSerializer

    def get(self, request, *args, **kwargs):
        # postid = kwargs.get('postid')
        person_id = request.user.reg_person_id
        person_obj = request.user.reg_person
        first_name = person_obj.first_name
        surname = person_obj.surname
        onames = person_obj.surname
        other_names = onames if onames else ''
        person_names = '%s %s' % (first_name, surname)
        #
        user_orgs = get_attached_orgs(request)
        results = dcs_dashboard(request, user_orgs)
        results['org_unit'] = user_orgs['ou_name']
        results['org_unit_id'] = user_orgs['ou_id']
        parent_ou_id = results['org_unit_id']
        cous = RegOrgUnit.objects.filter(
            parent_org_unit_id=parent_ou_id, is_void=False)
        org_units = []
        # Children Units
        for cou in cous:
            org_units.append({'org_unit_id': cou.id,
                              'org_unit_name': cou.org_unit_name,
                              'primary_unit': False})

        results['person_id'] = person_id
        results['person_names'] = person_names
        results['person_first_name'] = first_name
        results['person_surname'] = surname
        results['person_other_names'] = other_names
        results['org_units'] = org_units
        results['org_units_count'] = cous.count()
        results['sync_timestamp'] = datetime.now()
        return Response(results)

class MobileMetadata(APIView):

    serializer_class = MobileUserSerializer

    def get(self, request, *args, **kwargs):
        results = {"message": "Successfull"}
        return Response(results)


class MobileNotifications(APIView):

    serializer_class = MobileUserSerializer

    def get(self, request, *args, **kwargs):
        results = [{"text": "Referral out", "category": "Referral",
                    "timestamp": datetime.now(), "count": 4} ]
        return Response(results)