from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, generics, status

from rest_framework.views import APIView

from cpovc_forms.models import OVCCaseRecord, OVCCaseGeo
from cpovc_registry.models import RegPerson, RegPersonsOrgUnits, RegOrgUnit
from cpovc_mobile.serializers import CaseRecordSerializer, MobileUserSerializer

from cpovc_api.functions import get_attached_orgs, dcs_dashboard


@api_view(['POST', 'GET'])
def ovc_mobile_home(request):
    """Method to handle Mobile endpoints."""
    try:
        return(Response({'message':'Method not allowed'}, status=status.HTTP_400_BAD_REQUEST))
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
        cases = OVCCaseGeo.objects.filter(is_void=False).values('case_id_id')[:10]
        case_obj = OVCCaseRecord.objects.filter(
        	case_id__in=cases, case_status='ACTIVE')
        return case_obj


@api_view(['POST', 'PUT', 'PATCH', 'DELETE'])
def ovc_mobile_crs(request):
    """Method to handle Mobile CRS endpoints."""
    try:
        results = {"message": "Saved Successfull"}

        return(Response(results, status=201 ))
    except Exception as e:
        raise e
    else:
        pass


@api_view(['POST', 'PUT', 'PATCH', 'DELETE'])
def ovc_mobile_follow_up(request):
    """Method to handle Mobile CRS endpoints."""
    try:
        results = {"message": "Saved Successfull"}

        return(Response(results, status=201 ))
    except Exception as e:
        raise e
    else:
        pass


@api_view(['POST', 'PUT', 'PATCH', 'DELETE'])
def ovc_mobile_forms(request):
    """Method to handle Mobile CRS endpoints."""
    try:
        results = {"message": "Saved Successfull"}

        return(Response(results, status=201 ))
    except Exception as e:
        raise e
    else:
        pass


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