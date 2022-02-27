"""URLs for authentication module."""
from django.urls import include, path

# This should contain urls related to auth app ONLY
urlpatterns = include('cpovc_auth.views',
                       path(r'^$', 'home'),
                       path(r'^register/$', 'register'),
                       path(r'^ping/$', 'user_ping', name='user_ping'),
                       path(r'^roles/$', 'roles_home', name='roles_home'),
                       path(r'^roles/edit/(?P<user_id>\d+)/$', 'roles_edit',
                           name='roles_edit'),
                       )
