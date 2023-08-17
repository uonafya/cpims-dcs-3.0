"""Admin backend for editing some admin details."""
from django.contrib import admin

from .models import (
    RegPerson, RegOrgUnit, RegOrgUnitsAuditTrail,
    RegPersonsAuditTrail, RegPersonsTypes, RegPersonsOtherGeo,
    RegPersonsGeo, RegPersonsOrgUnits, Photo)


from cpovc_auth.models import AppUser


class PersonInline(admin.StackedInline):
    model = AppUser
    exclude = ('password', )


class PersonOrgsInline(admin.StackedInline):
    model = RegPersonsOrgUnits
    # exclude = ('password', )


class RegPersonAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['first_name', 'surname', 'other_names', 'id']
    list_display = ['id', 'first_name', 'surname', 'date_of_birth',
                    'age', 'sex_id', 'is_void']
    # readonly_fields = ['id']
    list_filter = ['is_void', 'sex_id', 'created_at']

    inlines = (PersonInline, PersonOrgsInline, )


admin.site.register(RegPerson, RegPersonAdmin)


class RegPersonTypesAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['person']
    list_display = ['id', 'person', 'person_type_id',
                    'date_created', 'is_void', ]

    def date_created(self, obj):
        return obj.person.created_at
    date_created.admin_order_field = 'date'
    date_created.short_description = 'Date Created'
    # readonly_fields = ['id']
    list_filter = ['is_void', 'person_type_id', 'person__created_at']


admin.site.register(RegPersonsTypes, RegPersonTypesAdmin)


class RegOrgUnitAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['org_unit_name', 'org_unit_id_vis']
    list_display = ['id', 'org_unit_id_vis', 'org_unit_name',
                    'parent_org_unit_id', 'parent_unit', 'is_void']
    # readonly_fields = ['id']
    list_filter = ['is_void', 'org_unit_type_id', 'created_at',
                   'parent_org_unit_id']


admin.site.register(RegOrgUnit, RegOrgUnitAdmin)


class RegPersonGeoAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['person__id', 'person__surname',
                     'person__first_name', 'area__area_name']
    list_display = ['id', 'person', 'area',
                    'area_type', 'date_linked', 'is_void']
    # readonly_fields = ['id']
    list_filter = ['is_void', 'area_type', 'date_linked']


admin.site.register(RegPersonsGeo, RegPersonGeoAdmin)


class OrgUnitAuditAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['org_unit_id']
    list_display = ['transaction_id', 'transaction_type_id', 'ip_address',
                    'app_user_id', 'timestamp_modified']
    # readonly_fields = ['id']
    list_filter = ['transaction_type_id', 'app_user_id']


admin.site.register(RegOrgUnitsAuditTrail, OrgUnitAuditAdmin)


class PersonsAuditAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['person_id']
    list_display = ['transaction_id', 'transaction_type_id', 'ip_address',
                    'app_user_id', 'timestamp_modified']
    # readonly_fields = ['id']
    list_filter = ['transaction_type_id', 'app_user_id']


admin.site.register(RegPersonsAuditTrail, PersonsAuditAdmin)


class RegPersonOtherGeoAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['person__surname', 'person__first_name',
                     'country_code', 'city']
    list_display = ['id', 'person', 'country_code',
                    'location', 'date_linked', 'is_void']
    # readonly_fields = ['id']
    list_filter = ['is_void', 'date_linked']


admin.site.register(RegPersonsOtherGeo, RegPersonOtherGeoAdmin)


class PhotoAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['person__surname', 'person__first_name',
                     'user__username']
    list_display = ['id', 'person', 'user', 'photo_passport', 'is_void']
    # readonly_fields = ['id']
    list_filter = ['is_void']


admin.site.register(Photo, PhotoAdmin)
