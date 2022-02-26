"""Admin backend for editing this aggregate data."""
from django.contrib import admin

from .models import (
    OVCAggregate, OVCFacility, OVCSchool, OVCCluster,
    OVCClusterCBO)


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


admin.site.register(OVCFacility, OVCFacilityAdmin)


class OVCSchoolAdmin(admin.ModelAdmin):
    """Aggregate data admin."""

    search_fields = ['school_name']
    list_display = ['id', 'school_level', 'school_name',
                    'sub_county']
    # readonly_fields = ['id']
    list_filter = ['is_void']


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


admin.site.register(OVCCluster, OVCClusterAdmin)


class OVCClusterCBOAdmin(admin.ModelAdmin):
    """Aggregate data admin."""

    search_fields = ['cluster', 'cbo']
    list_display = ['id', 'cluster', 'cbo', 'added_at']
    # readonly_fields = ['id']
    list_filter = ['is_void']


admin.site.register(OVCClusterCBO, OVCClusterCBOAdmin)
