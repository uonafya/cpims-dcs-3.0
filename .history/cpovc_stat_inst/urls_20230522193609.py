from django.urls import path, re_path
from . import views

# This should contain urls related to registry ONLY
urlpatterns = [
    path('', views.home, name='SI_Home'),
]