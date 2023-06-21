from django.urls import path, re_path
from . import views

# This should contain urls related to registry ONLY
urlpatterns = [
    path('', views.si_home, name='SI_home'),
    # path('new/<uuid:case_id>/', views.SI_admissions, name='new_si_admit'),
    path('new/<int:id>/', views.SI_admissions, name='new_si_admit'),
    path('needriskform/<int:id>/', views.SI_needriskform, name='new_si_riskneedform'),
    path('needriskscale/<int:id>/', views.SI_needriskscale, name='new_si_riskneedscale'),
]