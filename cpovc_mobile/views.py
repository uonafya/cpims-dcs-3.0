from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib import messages
from rest_framework import viewsets, generics, status

from cpovc_forms.models import OVCCaseRecord, OVCCaseGeo
from cpovc_mobile.serializers import CaseRecordSerializer
from django.shortcuts import render, redirect
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


@api_view(["POST"])
def ovc_mobile_crs(request):
    """Method to handle Mobile CRS endpoints."""
    try:
        results = {"message": "Saved Successfull"}

        return Response(results, status=201)
    except Exception as e:
        raise e
    else:
        pass


@api_view(["POST"])
def ovc_mobile_follow_up(request):
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
