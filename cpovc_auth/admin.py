"""Users admin."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import AppUser, CPOVCProfile
from cpovc_registry.models import RegPerson
from cpovc_main.admin import dump_to_csv


class PersonInline(admin.StackedInline):
    model = RegPerson
    max_num = 1
    can_delete = False
    fk_name = 'id'
    # exclude = ('password', )


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    using <a href=\"password/\">this form</a>
    """
    password = ReadOnlyPasswordHashField(
        label=("Password"),
        help_text=("Raw passwords are not stored, so there is no way to see "
                   "this user's password. Change of passwords "
                   "by Administrators has been disabled. Make sure account "
                   "is active and that email address is set for them "
                   "to self reset."))

    class Meta:
        model = AppUser
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class MyUserAdmin(UserAdmin):
    """
    Admin back end class.

    This is for handling Django admin create user.
    """

    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        actions = super(MyUserAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    model = AppUser
    form = UserChangeForm

    actions = [dump_to_csv]

    list_display = ['username', 'sex', 'surname', 'first_name', 'last_name',
                    'email', 'timestamp_created', 'last_login', 'is_active']

    search_fields = ['username']
    readonly_fields = ['reg_person']
    list_filter = ['is_active', 'is_staff', 'is_superuser',
                   'timestamp_created', 'last_login',
                   'groups', 'reg_person__sex_id']

    fieldsets = (
        (_('Personal info'), {'fields': ('username', 'password',
                                         'reg_person')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff',
                                       'is_superuser', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',
                                           'password_changed_timestamp')}),
        (_('Groups'), {'fields': ('groups',)}),
    )

    add_fieldsets = (
        (_('Create Account'), {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'reg_person')}
         ),
    )

    # inlines = (PersonInline, )


admin.site.register(AppUser, MyUserAdmin)


class MyProfileAdmin(admin.ModelAdmin):
    """Admin for profile."""
    list_display = ['user', 'details']


admin.site.register(CPOVCProfile, MyProfileAdmin)
