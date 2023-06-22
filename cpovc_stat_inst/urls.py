from django.urls import path, re_path
from . import views

# This should contain urls related to registry ONLY
urlpatterns = [
    path('', views.si_home, name='SI_home'),
    # path('new/<uuid:case_id>/', views.SI_admissions, name='new_si_admit'),
    path('view/<int:id>/', views.SI_child_view, name='new_si_child_view'),

    path('new/<int:id>/', views.SI_admissions, name='new_si_admit'),
    path('needriskform/<int:id>/', views.SI_needriskform, name='new_si_riskneedform'),    
    path('needriskscale/<int:id>/', views.SI_needriskscale, name='new_si_riskneedscale'),

    path('vacancy/<int:id>/', views.SI_vacancyapplication, name='vacancy_app'),
    path('confirmation/<int:id>/', views.SI_vacancyconfirmation, name='vacancy_confirm'),
    path('socialinquiry/<int:id>/', views.SI_social_inquiry, name='social_inquiry'),
]