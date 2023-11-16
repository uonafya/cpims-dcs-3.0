from django.contrib import admin
from .models import SIMain, SI_Document


class SIMainAdmin(admin.ModelAdmin):
    """SI Main admin."""

    search_fields = ['case', 'person__surname']
    list_display = ['case_number', 'person', 'org_unit',
                    'org_type', 'timestamp_created']
    # readonly_fields = ['id']
    list_filter = ['is_void', 'case_status', 'case_stage', 'org_type',
                   'timestamp_created']


admin.site.register(SIMain, SIMainAdmin)


class SIDocumentAdmin(admin.ModelAdmin):
    """SI Documents admin."""

    search_fields = ['document_type', 'person__surname']
    list_display = ['document_type', 'person', 'created_at']
    readonly_fields = ['person', 'created_by']
    list_filter = ['is_void', 'document_type', 'created_at']


admin.site.register(SI_Document, SIDocumentAdmin)
