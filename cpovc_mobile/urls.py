from django.urls import path
from . import views

# This should contain urls related to Mobile App endpoints ONLY

urlpatterns = [
    path('', views.ovc_mobile_home, name='ovc_mobile_home'),
    # path('caseload/', views.ovc_mobile_caseload, name='ovc_mobile_caseload'),
    path('caseload/', views.CaseloadViewSet.as_view()),
]