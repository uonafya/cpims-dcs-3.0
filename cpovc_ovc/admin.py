"""Admin backend for editing this aggregate data."""
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import (
    OVCAggregate, OVCFacility, OVCSchool, OVCCluster,
    OVCClusterCBO, OVCRegistration, OVCEligibility,
    OVCHHMembers, OVCHouseHold, OVCHealth)

from django.contrib.admin.helpers import ActionForm
from django import forms
from cpovc_main.utils import dump_to_csv


def bulk_transfer(modeladmin, request, queryset):
    transfer_to = request.POST['transfer_to']
    cbo_id = int(transfer_to)
    queryset.update(child_cbo_id=cbo_id)


bulk_transfer.short_description = 'Bulk Transfer to selected CBO'


class OVCEligibilityAdmin(admin.ModelAdmin):
    """Aggregate data admin."""

    search_fields = ['person', ]
    list_display = ['id', 'person', 'criteria', 'is_void']

    list_filter = ['criteria', 'is_void']


admin.site.register(OVCEligibility, OVCEligibilityAdmin)


class UpdateActionForm(ActionForm):
    transfer_to = forms.IntegerField()


class OVCRegistrationAdmin(admin.ModelAdmin):
    """Aggregate data admin."""

    search_fields = ['caretaker__id', 'person__id', 'child_chv__id']
    list_display = ['person_id', 'person', 'child_cbo', 'child_chv',
                    'caretaker', 'registration_date', 'hiv_status',
                    'is_active', 'is_void']
    readonly_fields = ['id', 'person', 'caretaker', 'child_chv']
    list_filter = ['is_active', 'is_void', 'hiv_status']

    action_form = UpdateActionForm

    actions = [bulk_transfer]


admin.site.register(OVCRegistration, OVCRegistrationAdmin)


class OVCAggregateAdmin(admin.ModelAdmin):
    """Aggregate data admin."""

    search_fields = ['indicator_name', 'gender']
    list_display = ['id', 'indicator_name', 'indicator_count', 'age',
                    'reporting_period', 'cbo', 'subcounty', 'county']
    # readonly_fields = ['id']
    list_filter = ['indicator_name', 'project_year', 'reporting_period',
                   'gender', 'subcounty', 'county', 'cbo']


admin.site.register(OVCAggregate, OVCAggregateAdmin)


class OVCFacilityAdmin(admin.ModelAdmin):
    """Aggregate data admin."""

    search_fields = ['facility_code', 'facility_name']
    list_display = ['id', 'facility_code', 'facility_name',
                    'sub_county']
    # readonly_fields = ['id']
    list_filter = ['is_void']
    actions = [dump_to_csv]


admin.site.register(OVCFacility, OVCFacilityAdmin)


class OVCSchoolAdmin(ImportExportModelAdmin):
    """Aggregate data admin."""

    search_fields = ['school_name']
    list_display = ['id', 'school_level', 'school_name',
                    'sub_county']
    # readonly_fields = ['id']
    list_filter = ['is_void']
    actions = [dump_to_csv]


admin.site.register(OVCSchool, OVCSchoolAdmin)


class CBOsInline(admin.StackedInline):
    model = OVCClusterCBO
    # exclude = ('password', )


class OVCClusterAdmin(admin.ModelAdmin):
    """Aggregate data admin."""

    search_fields = ['cluster_name']
    list_display = ['id', 'cluster_name', 'created_by']
    # readonly_fields = ['id']
    list_filter = ['is_void']
    inlines = (CBOsInline, )
    actions = [dump_to_csv]


admin.site.register(OVCCluster, OVCClusterAdmin)


class OVCClusterCBOAdmin(admin.ModelAdmin):
    """Aggregate data admin."""

    search_fields = ['cluster', 'cbo__org_unit_name']
    list_display = ['id', 'cluster', 'cbo', 'added_at']
    # readonly_fields = ['id']
    list_filter = ['is_void']


admin.site.register(OVCClusterCBO, OVCClusterCBOAdmin)
admin.site.disable_action('delete_selected')


class OVCHHMembersInline(admin.StackedInline):
    model = OVCHHMembers
    readonly_fields = ['person']


class OVCHouseHoldAdmin(admin.ModelAdmin):
    """Aggregate data admin."""

    search_fields = ['head_person__id', 'head_person__first_name',
                     'head_person__surname']
    list_display = ['head_person_id', 'head_person', 'head_identifier']

    readonly_fields = ['head_person']

    list_filter = ['is_void', 'created_at']
    inlines = (OVCHHMembersInline, )
    actions = [dump_to_csv]


admin.site.register(OVCHouseHold, OVCHouseHoldAdmin)
