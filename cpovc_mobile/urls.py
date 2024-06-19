from django.urls import path
from cpovc_mobile import views

# This should contain urls related to Mobile App endpoints ONLY

urlpatterns = [
    path('', views.ovc_mobile_home, name='ovc_mobile_home'),
    # Set up
    path('caseload/', views.CaseloadViewSet.as_view()),
    path('settings/', views.MobileUser.as_view()),
    path('metadata/', views.MobileMetadata.as_view()),
    # Forms
    path('crs/', views.ovc_mobile_crs, name='ovc_mobile_crs'),
    path('forms/', views.ovc_mobile_forms, name='ovc_mobile_forms'),
    # Follow ups
    path('follow_up/', views.ovc_mobile_follow_up, name='ovc_mobile_follow_up'),
    # Others
    path('notifications/', views.MobileNotifications.as_view()),
]