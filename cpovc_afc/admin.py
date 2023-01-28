from django.contrib import admin
from .models import AFCMain, AFCForms, AFCEvents, AFCInfo, AFCQuestions


class AFCMainAdmin(admin.ModelAdmin):
    """Admin back end for Geo data management."""

    search_fields = ['case_number', 'person__surname', 'person__first_name']
    list_display = ['care_id', 'case_id', 'care_type', 'case_number',
                    'person', 'org_unit',
                    'case_date', 'get_creator', 'case_status', 'case_stage']
    # readonly_fields = ['area_id']
    list_filter = ['is_void', 'care_type', 'case_status', 'case__created_by']

    def get_creator(self, obj):
        return obj.case.created_by
    get_creator.short_description = 'Creator'
    get_creator.admin_order_field = 'case__created_by'
    # actions = [dump_to_csv]


admin.site.register(AFCMain, AFCMainAdmin)


class FormsInline(admin.StackedInline):
    model = AFCForms


class AFCEventsAdmin(admin.ModelAdmin):
    """Admin back end for Geo data management."""

    search_fields = ['person__first_name', 'person__surname']
    list_display = ['case_id', 'form_id', 'person', 'event_date',
                    'event_count', 'created_by']
    # readonly_fields = ['area_id']
    list_filter = ['is_void', 'form_id', 'event_date']

    inlines = (FormsInline, )


admin.site.register(AFCEvents, AFCEventsAdmin)


class AFCInfoAdmin(admin.ModelAdmin):
    """Admin back end for Geo data management."""

    search_fields = ['person_id']
    list_display = ['care_id', 'person', 'item_id', 'item_value']
    # readonly_fields = ['area_id']
    list_filter = ['is_void']


admin.site.register(AFCInfo, AFCInfoAdmin)


class AFCFormsAdmin(admin.ModelAdmin):
    """Admin back end for Geo data management."""

    search_fields = ['person_id']
    list_display = ['event', 'question_id', 'item_value']
    # readonly_fields = ['area_id']
    list_filter = ['is_void']


admin.site.register(AFCForms, AFCFormsAdmin)


class AFCQuestionsAdmin(admin.ModelAdmin):
    """ Questions model."""

    search_fields = ['question_code', 'question_text']
    list_display = ['form_id', 'the_order', 'question_code', 'question_text',
                    'is_void']
    list_filter = ['form_id']


admin.site.register(AFCQuestions, AFCQuestionsAdmin)
