from django.urls import path, re_path
from . import views

# This should contain urls related to Mobile App endpoints ONLY

urlpatterns = [
    path("", views.ovc_mobile_home, name="ovc_mobile_home"),
    # path('caseload/', views.ovc_mobile_caseload, name='ovc_mobile_caseload'),
    path("caseload/", views.CaseloadViewSet.as_view()),
    # path('crs/', views.CaseloadViewSet.as_view()),
    # path('follow_up/', views.CaseloadViewSet.as_view()),
    path("crs/", views.ovc_mobile_crs, name="ovc_mobile_crs"),
    path("follow_up/", views.ovc_mobile_follow_up, name="ovc_mobile_follow_up"),
    # Approval urls UI
    path("mobile-approval/", views.mobile_app_home, name="mobile_app_home"),
    re_path(
        r"^crs/view/(?P<id>[0-9a-f]{8}-[0-9a-f]{4}-1[0-9a-f]{3}-[0-9a-f]{4}-[0-9a-f]{12})/$",
        views.view_mobile_case_record_sheet,
        name="view_mobile_case_record_sheet",
    ),
#      re_path(
#         r"^crs/view/(?P<id>\w+)/$",
#         views.view_mobile_case_record_sheet,
#         name="view_mobile_case_record_sheet",
#     ),
]
