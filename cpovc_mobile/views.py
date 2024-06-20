from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, generics, status

from cpovc_forms.models import OVCCaseRecord, OVCCaseGeo
from cpovc_mobile.serializers import CaseRecordSerializer
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required


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
    csr_id = id
    print(f"CSR-ID: {csr_id}")
    context = {
        "cases": [
            {
                "id": "749fc18f2cbf11efb24922a3499bfe31",
                "care_id": "2323",
                "case": "CCO/47/287/5/29/4423/2024",
                "first_name": "Boniface",
                "case_date": "2024-01-01",
                "case_level": "8",
            },
            {
                "id": "749fc18f2cbf11efb24922a3499bfe32",
                "care_id": "2323",
                "case": "CCO/47/287/5/29/4425/2024",
                "first_name": "John",
                "case_date": "2024-01-01",
                "case_level": "8",
            },
            {
                "id": "749fc18f2cbf11efb24922a3499bfe33",
                "care_id": "2323",
                "case": "CCO/47/287/5/29/4426/2024",
                "first_name": "Jane",
                "case_date": "2024-01-01",
                "case_level": "8",
            },
            {
                "id": "749fc18f2cbf11efb24922a3499bfe33",
                "care_id": "2323",
                "case": "CCO/47/287/5/29/4427/2024",
                "first_name": "Jude",
                "case_date": "2024-01-01",
                "case_level": "8",
            },
        ]
    }
    return render(request, "mobile/preview_csr.html", context=context)
