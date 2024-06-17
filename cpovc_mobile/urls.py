from django.urls import path
from . import views

# This should contain urls related to Mobile App endpoints ONLY

urlpatterns = [
    path('', views.ovc_mobile_home, name='ovc_mobile_home'),
    # path('caseload/', views.ovc_mobile_caseload, name='ovc_mobile_caseload'),
    path('caseload/', views.CaseloadViewSet.as_view()),
    # path('crs/', views.CaseloadViewSet.as_view()),
    # path('follow_up/', views.CaseloadViewSet.as_view()),
    path('crs/', views.ovc_mobile_crs, name='ovc_mobile_crs'),
    path('follow_up/', views.ovc_mobile_follow_up, name='ovc_mobile_follow_up'),
]