"""OVC care section urls."""
from django.urls import path
from . import views

# This should contain urls related to registry ONLY
urlpatterns = [
    path("",views.ovc_home.as_view()),
    path("ovc/search/",views.ovc_search.as_view()),
    path('ovc/new/<int:id>',views.ovc_register.as_view()),
    path('ovc/edit/<int:id>',views.ovc_edit.as_view()),
    path('ovc/view/<int:id>',views.ovc_view.as_view()),
    path(r'^hh/view/(?P<hhid>[0-9A-Za-z_\-]+)/$',views.hh_manage.as_view())
    ]

