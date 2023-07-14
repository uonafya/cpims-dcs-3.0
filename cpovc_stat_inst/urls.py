from django.urls import path, re_path
from . import views

# This should contain urls related to registry ONLY
urlpatterns = [
    path('', views.si_home, name='SI_home'),

    path('new/<int:id>/', views.SI_admissions, name='new_si_admit'),

    path('medical-assessment/<int:id>/', views.SI_medicalassesment, name='medical_assessment_form'),
    path('individual-care-plan/<int:id>/', views.SI_individualCarePlan, name='individual_care_plan_form'),
    path('leave_of_abscence/<int:id>/', views.SI_LeaveOfAbscence, name='leave_of_absence'),
    path('remand_home_escape/<int:id>/', views.SI_RemandHomeEscape, name='remand_escape'),

    path('case_refer/<int:id>/', views.si_casereferral, name='SI_casereferral'),
    path('exit_certificate/<int:id>/', views.si_certificateofexit, name='SI_certificateofexit'),
    path('remand_home_escape/<int:id>/', views.si_remandhomeescape, name='SI_remandhomeescape'),
    path('record_of_visits/<int:id>/', views.si_recordofvisits, name='SI_recordofvisits'),
    path('family_conference/<int:id>/', views.si_familyconference, name='SI_familyconference'),
    path('release_form/<int:id>/', views.si_releaseform, name='SI_releaseform'), 
    path('child_profile/<int:id>/', views.si_childprofile, name='SI_childprofile'),

    path('view/<int:id>/', views.SI_child_view, name='new_si_child_view'),

    path('needriskform/<int:id>/', views.SI_needriskform, name='new_si_riskneedform'),    
    path('needriskscale/<int:id>/', views.SI_needriskscale, name='new_si_riskneedscale'),

    path('socialinquiry/<int:id>/', views.SI_social_inquiry, name='social_inquiry'),


    # Vacancy mode
    path('vacancy/<int:id>/', views.SI_vacancyapplication, name='vacancy_app'),
    path('confirmation/<int:id>/', views.SI_vacancyconfirmation, name='vacancy_confirm'),
    path('deny_vacancy/<uuid:uid>/', views.SI_deny_vacancy, name='deny_vacancy'),
    path('delete_vacancy/<uuid:uid>/', views.SI_delete_vacancy, name='delete_vacancy'),
    path('vacancyDetail/', views.SI_vacancyDetail, name='vacancyDetail'),
    path('vacancyApprove/', views.SI_vacancyApprove, name='vacancyApprove'),

    # Placement
    path('placement/<int:id>/', views.child_placement, name='placement'),


    # lookup script/ Api endpoints
    path('si_lookup/', views.si_look, name='si_lookup'),


]