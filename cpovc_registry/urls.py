"""Registry section urls."""
from django.urls import path
from . import views

# This should contain urls related to registry ONLY
urlpatterns = [
    path('ou/', views.home, name='registry'),
    path('ou/new/', views.register_new, name='registry_new'),
    path(
        'ou/view/<int:org_id>/', views.register_details,
        name='register_details'),
    path('ou/edit/<int:org_id>/', views.register_edit, name='registry_edit'),
    path('person/search/', views.persons_search, name='search_persons'),
    path('person/user/<int:id>/', views.new_user, name='new_user'),
    path('person/', views.person_actions, name='person_actions'),
    path('person/new/', views.new_person, name='new_person'),
    path('person/edit/<int:id>/', views.edit_person, name='edit_person'),
    path('person/view/<int:id>/', views.view_person, name='view_person'),
    path('person/delete/<int:id>/', views.delete_person, name='delete_person'),
    path('lookup/', views.registry_look, name='reg_lookup'),
    path('person/api/', views.person_api, name='person_api'),
    path('person/profile/', views.person_profile, name='person_profile'),
    path('person/tl/<int:id>/', views.person_timeline, name='person_timeline'),
]
# {% url 'view_person' id=result.id %}
