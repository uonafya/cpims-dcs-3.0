from django.urls import path
from django.contrib.auth import views as auth_views
from cpovc_access.forms import StrictPasswordChangeForm

from .forms import PasswordResetForm
from . import views
# This should contain urls related to auth app ONLY

urlpatterns = [
    path('', views.home, name='auth_home'),
    path('register/', views.register, name='register'),
    path('ping/', views.user_ping, name='user_ping'),
    path('roles/', views.roles_home, name='roles_home'),
    path('roles/edit/<int:user_id>/', views.roles_edit,
         name='roles_edit'),
    # Forget Password Functionality
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset.html',
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             form_class=PasswordResetForm
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path(
        'password/change/', auth_views.PasswordChangeView.as_view(),
        {'post_change_redirect': '/accounts/password/change/done/',
         'template_name': 'registration/password_change.html',
         'password_change_form': StrictPasswordChangeForm},
        name='password_change'),

]
