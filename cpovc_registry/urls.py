"""Registry section urls."""
from django.urls import re_path, path
from . import views
# This should contain urls related to registry ONLY
urlpatterns = [
    # 'cpovc_registry.views',
    path('ou/', views.home, name='registry'),
    path('ou/new/', views.register_new, name='registry_new'),
    re_path('ou/view/(?P<org_id>\d+)/', views.register_details, name='register_details'),
    re_path('ou/edit/(?P<org_id>\d+)/', views.register_edit, name='registry_edit'),
    path('person/search/', views.persons_search, name='search_persons'),
    re_path(r'^person/user/(?P<id>\d+)/$', views.new_user, name='new_user'),
    path('person/', views.person_actions, name='person_actions'),
    path('person/new/', views.new_person, name='new_person'),
    re_path(r'^person/edit/(?P<id>\d+)/$', views.edit_person, name='edit_person'),
    re_path(r'^person/view/(?P<id>\d+)/$', views.view_person, name='view_person'),
    path('person/delete/<int:id>/', views.delete_person, name='delete_person'),
    # path('person/delete/<int:id>/', views.delete_person, name='delete_person'),
    path('lookup/', views.registry_look, name='reg_lookup'),
    re_path(r'^person/api/$', views.person_api, name='person_api'),
    re_path(r'^person/profile/$', views.person_profile, name='person_profile'),
    re_path(r'^person/tl/(?P<id>\d+)/$', views.person_timeline, name='person_timeline'),
]
# {% url 'view_person' id=result.id %}
