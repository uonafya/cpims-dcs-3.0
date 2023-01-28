"""Main module for managing set up lists."""

from django.contrib import admin

from .models import (
    SetupGeography, SetupList, ListAnswers, SetupLocation, ListQuestions)

from .utils import dump_to_csv, export_xls, export_xlsx


class GeoModelAdmin(admin.ModelAdmin):
    """Admin back end for Geo data management."""

    search_fields = ['area_id', 'area_name']
    list_display = ['area_id', 'area_name', 'area_type_id', 'area_code',
                    'parent_area_id']
    readonly_fields = ['area_id']
    list_filter = ['area_type_id', 'parent_area_id']
    actions = [dump_to_csv, export_xls, export_xlsx]


admin.site.register(SetupGeography, GeoModelAdmin)


class GeneralModelAdmin(admin.ModelAdmin):
    """Admin back end for Lookup lists management."""

    search_fields = ['item_id', 'item_description', 'field_name']
    list_display = ['item_id', 'item_description', 'field_name',
                    'item_category', 'item_sub_category', 'the_order',
                    'is_void']
    readonly_fields = ['is_void']
    list_filter = ['field_name']
    actions = [dump_to_csv]


admin.site.register(SetupList, GeneralModelAdmin)


class ListAnswersAdmin(admin.ModelAdmin):
    """Admin back end for Lookup lists management."""

    search_fields = ['answer_set_id', 'answer']
    list_display = ['id', 'answer_set_id', 'answer_code', 'answer',
                    'the_order', 'is_void']
    list_filter = ['answer_set_id']
    actions = [dump_to_csv]


admin.site.register(ListAnswers, ListAnswersAdmin)


class GeoLocationAdmin(admin.ModelAdmin):
    """Admin back end for Geo data management."""

    search_fields = ['area_id', 'area_name']
    list_display = ['area_id', 'area_name', 'area_type_id', 'area_code',
                    'parent_area_id']
    readonly_fields = ['area_id']
    list_filter = ['area_type_id']
    actions = [dump_to_csv, export_xls, export_xlsx]


admin.site.register(SetupLocation, GeoLocationAdmin)


class ListQuestionsAdmin(admin.ModelAdmin):
    """ Questions model."""

    search_fields = ['question_code', 'question_text']
    list_display = ['form_type_id', 'question_code', 'question_text',
                    'is_void']
    list_filter = ['form_type_id']


admin.site.register(ListQuestions, ListQuestionsAdmin)
