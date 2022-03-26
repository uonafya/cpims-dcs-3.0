"""Registry section urls."""
from os import path

from django.urls import path

# This should contain urls related to registry ONLY
import cpovc_registry.views

urlpatterns = [
    'cpovc_registry.views',
    path('ou/', cpovc_registry.views.home, name='registry'),
    path('ou/new/', cpovc_registry.views.register_new, name='registry_new'),
    path('ou/view/<int:org_id>/', cpovc_registry.views.register_details, name='register_details'),
    path('ou/edit/<int:org_id>/', cpovc_registry.views.register_edit, name='registry_edit'),
    # url(r'^person/search/$', 'persons_search', name='search_persons'),
    path('person/search/', cpovc_registry.views.persons_search, name='search_persons'),
    # url(r'^person/user/(?P<id>\d+)/$', 'new_user', name='new_user'),
    path('person/user/<int:id>/', cpovc_registry.views.new_user, name='new_user'),
    #url(r'^person/$', 'person_actions', name='person_actions'),
    path('person/', cpovc_registry.views.person_actions, name='person_actions'),
    #url(r'^person/new/$', 'new_person', name='new_person'),
    path('person/new/', cpovc_registry.views.new_person, name='new_person'),
    #url(r'^person/edit/(?P<id>\d+)/$', 'edit_person', name='edit_person'),
    path('person/edit/<int:id>/', cpovc_registry.views.edit_person, name='edit_person'),
    #url(r'^person/view/(?P<id>\d+)/$', 'view_person', name='view_person'),
    path('person/view/<int:id>/', cpovc_registry.views.view_person, name='view_person'),
    #url(r'^person/delete/(?P<id>\d+)/$', 'delete_person', name='delete_person'),
    path('person/delete/<id>/', cpovc_registry.views.delete_person(), name='delete_person'),

    # url(r'^lookup/$', 'registry_look', name='reg_lookup'),
    path('lookup/', cpovc_registry.views.registry_look, name='reg_lookup'),
    # url(r'^person/api/$', 'person_api', name='person_api'),
    path('person/api/', cpovc_registry.views.person_api(), name='person_api'),
    # url(r'^person/profile/$', 'person_profile', name='person_profile'),
    path('person/profile/', cpovc_registry.views.person_profile, name='person_profile'),
    # url(r'^person/tl/(?P<id>\d+)/$', 'person_timeline', name='person_timeline'),
    path('person/tl/<int:id>/', cpovc_registry.views.person_timeline, name='person_timeline'),
]
    # {% url 'view_person' id=result.id %}
