from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, generics, status

from cpovc_forms.models import OVCCaseRecord, OVCCaseGeo
from cpovc_mobile.serializers import CaseRecordSerializer


@api_view(['POST', 'GET'])
def ovc_mobile_home(request):
    """Method to handle Mobile endpoints."""
    try:
        return(Response({'message':'Method not allowed'}, status=status.HTTP_400_BAD_REQUEST))
    except Exception as e:
        raise e
    else:
        pass

@api_view(['GET'])
def ovc_mobile_caseload(request):
    """Method to handle Mobile endpoints."""
    try:
        results = []
        res = {"case_id": "",
               "ovc_cpims_id": 1,
			   "case_serial": "CCO/42/241/5/29/387/2024",
			   "parents": [{"cpims_id": 2, "first_name": "", "surname": "", "other_names": "", "relationship_type":""}],
			   "siblings": [{"cpims_id": 3,"first_name": "", "surname": "", "other_names": "", "relationship_type":""}],
			   "perpetrators" : [{"status": "", "first_name": "", "surname": "", "other_names": "", "relationship_type":""}],
			   "risk_level": "",
			   "date_case_opened": "2021-01-01",
			   "case_reporter": "",
			   "case_reporter_details" : [{"first_name": "", "surname": "", "other_names": "", "contacts": ""}],
			   "case_category" : [{'place_of_event': 'PESE', 'category': 'CSSO', 'nature_of_event': 'OCGE', 'date_of_event': '2021-01-01'},],
			   "case_status": "",
			   "referral": "", 
			   "case_remarks": "", 
			   "summon": "", "date_of_summon": ""}
        results.append(res)
        return(Response(results, status=status.HTTP_200_OK ))
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
