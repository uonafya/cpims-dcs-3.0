from django.urls import path, re_path
from . import views

# This should contain urls related to registry ONLY
urlpatterns = [
    path('', views.si_home, name='SI_home'),
    # path('new/<uuid:case_id>/', views.SI_admissions, name='new_si_admit'),
    path('new/<uuid:person_id>/', views.SI_admissions, name='new_si_admit'),
    path('medical-assessment/<uuid:person_id>/', views.SI_medicalassesment, name='medical_assessment_form'),
    path('individual-care-plan/<uuid:person_id>/', views.SI_individualCarePlan, name='individual_care_plan_form'),
    path('leave_of_abscence/<uuid:person_id>/', views.SI_LeaveOfAbscence, name='individual_care_plan_form'),
    path('remand_home_escape/<uuid:person_id>/', views.SI_RemandHomeEscape, name='individual_care_plan_form'),
]