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


@api_view(['POST'])
def ovc_mobile_crs(request):
    """Method to handle Mobile CRS endpoints."""
    try:
        results = {"message": "Saved Successfull"}

        return(Response(results, status=201 ))
    except Exception as e:
        raise e
    else:
        pass


@api_view(['POST'])
def ovc_mobile_follow_up(request):
    """Method to handle Mobile CRS endpoints."""
    try:
        results = {"message": "Saved Successfull"}

        return(Response(results, status=201 ))
    except Exception as e:
        raise e
    else:
        pass