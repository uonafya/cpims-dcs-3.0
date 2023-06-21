from django.urls import path, re_path
from . import views

# This should contain urls related to registry ONLY
urlpatterns = [
    path('', views.si_home, name='SI_home'),
    # path('new/<uuid:case_id>/', views.SI_admissions, name='new_si_admit'),
    path('new/<uuid:person_id>/', views.SI_admissions, name='new_si_admit'),
    path('case_refer', views.si_casereferral, name='SI_casereferral'),
    path('exit_certificate', views.si_certificateofexit, name='SI_certificateofexit'),
    path('remand_home_escape', views.si_remandhomeescape, name='SI_remandhomeescape'),
    path('record_of_visits', views.si_recordofvisits, name='SI_recordofvisits'),
    path('family_conference', views.si_familyconference, name='SI_familyconference'),
    path('release_form', views.si_releaseform, name='SI_releaseform'), 
    path('child_profile', views.si_childprofile, name='SI_childprofile'),
]