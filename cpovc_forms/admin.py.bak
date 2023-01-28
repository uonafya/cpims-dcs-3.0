import csv
import time
from django.contrib import admin
from django.http import HttpResponse
from .models import (
    OVCCaseGeo, OVCCaseCategory, OVCBasicCRS, OVCBasicPerson, OVCBasicCategory,
    OVCPlacement, OVCDischargeFollowUp, OVCCaseRecord, OVCCaseLoadView,
    OVCCaseEvents, OVCCaseLocation)


def dump_to_csv(modeladmin, request, qs):
    """
    These takes in a Django queryset and spits out a CSV file.

    Generic method for any queryset
    """
    model = qs.model
    file_id = 'CPIMS_%s_%d' % (model.__name__, int(time.time()))
    file_name = 'attachment; filename=%s.csv' % (file_id)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = file_name
    writer = csv.writer(response, csv.excel)

    headers = []
    for field in model._meta.fields:
        headers.append(field.name)
    writer.writerow(headers)

    for obj in qs:
        row = []
        for field in headers:
            val = getattr(obj, field)
            if callable(val):
                val = val()
            if type(val) == unicode:
                val = val.encode("utf-8")
            row.append(val)
        writer.writerow(row)
    return response


dump_to_csv.short_description = u"Dump to CSV"


def export_xls(modeladmin, request, queryset):
    """Method to export as excel."""
    import xlwt
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=list_geo.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("List Geo")
    row_num = 0
    columns = [
        (u"ID", 2000),
        (u"Name", 6000),
        (u"Parent", 8000),
    ]

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in xrange(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1
    for obj in queryset:
        row_num += 1
        row = [
            obj.pk,
            obj.area_name,
            obj.parent_area_id,
        ]
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response


export_xls.short_description = u"Export XLS"


def export_xlsx(modeladmin, request, queryset):
    """Export as xlsx."""
    import openpyxl
    from openpyxl.cell import get_column_letter
    fmt = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response = HttpResponse(content_type=fmt)
    response['Content-Disposition'] = 'attachment; filename=mymodel.xlsx'
    wb = openpyxl.Workbook()
    ws = wb.get_active_sheet()
    ws.title = "List Geo"

    row_num = 0

    columns = [
        (u"ID", 15),
        (u"Name", 70),
        (u"Parent", 70),
    ]

    for col_num in xrange(len(columns)):
        c = ws.cell(row=row_num + 1, column=col_num + 1)
        c.value = columns[col_num][0]
        c.style.font.bold = True
        # set column width
        col_width = columns[col_num][1]
        ws.column_dimensions[get_column_letter(col_num + 1)].width = col_width

    for obj in queryset:
        row_num += 1
        row = [
            obj.pk,
            obj.area_name,
            obj.parent_area_id,
        ]
        for col_num in xrange(len(row)):
            c = ws.cell(row=row_num + 1, column=col_num + 1)
            c.value = row[col_num]
            c.style.alignment.wrap_text = True

    wb.save(response)
    return response


export_xlsx.short_description = u"Export XLSX"


class OVCCaseGeoAdmin(admin.ModelAdmin):
    """Admin back end for Geo data management."""

    search_fields = ['report_orgunit__org_unit_name']
    list_display = ['case_id_id', 'person', 'report_orgunit',
                    'occurence_county',
                    'occurence_subcounty', 'get_creator']
    # readonly_fields = ['area_id']
    list_filter = ['is_void', 'case_id__created_by']

    def get_creator(self, obj):
        return obj.case_id.created_by
    get_creator.short_description = 'Creator'
    get_creator.admin_order_field = 'case_id__created_by'
    actions = [dump_to_csv, export_xls, export_xlsx]


admin.site.register(OVCCaseGeo, OVCCaseGeoAdmin)


class OVCCaseCategoryAdmin(admin.ModelAdmin):
    """Admin back end for Geo data management."""

    search_fields = ['person__first_name', 'person__surname',
                     'person__other_names']
    list_display = ['case_id_id', 'person', 'case_category', 'date_of_event',
                    'place_of_event', 'get_creator']
    # readonly_fields = ['area_id']
    list_filter = ['is_void', 'timestamp_created',
                   'case_nature', 'date_of_event']

    def get_creator(self, obj):
        return obj.case_id.created_by
    get_creator.short_description = 'Creator'
    get_creator.admin_order_field = 'case_id__created_by'
    actions = [dump_to_csv]


admin.site.register(OVCCaseCategory, OVCCaseCategoryAdmin)


class PersonInline(admin.StackedInline):
    model = OVCBasicPerson

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True
    # exclude = ('password', )


class CategoryInline(admin.StackedInline):
    model = OVCBasicCategory

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True


class OVCBasicCRSAdmin(admin.ModelAdmin):
    search_fields = ['case_serial']
    list_display = ['case_id', 'case_serial',
                    'timestamp_created']
    ordering = ('-timestamp_created',)

    list_filter = ['is_void', 'timestamp_created']

    inlines = (PersonInline, CategoryInline, )
    actions = [dump_to_csv]


admin.site.register(OVCBasicCRS, OVCBasicCRSAdmin)


class OVCDischargeInline(admin.StackedInline):
    model = OVCDischargeFollowUp

    readonly_fields = ['person']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True


class OVCPlacementSAdmin(admin.ModelAdmin):
    search_fields = ['admission_number', 'person__first_name', 'person__id',
                     'person__surname']
    list_display = ['admission_number', 'admission_date', 'person_id_display',
                    'person', 'admission_type', 'org_unit',
                    'residential_institution', 'timestamp_created',
                    'is_active', 'is_void']
    ordering = ('-timestamp_created',)

    list_filter = ['is_void', 'is_active', 'timestamp_created',
                   'admission_date', 'residential_institution_name']

    readonly_fields = ['org_unit', 'person', 'residential_institution',
                       'case_record']

    inlines = (OVCDischargeInline, )

    actions = [dump_to_csv]

    def person_id_display(self, obj):
        return obj.person_id
    person_id_display.short_description = 'Person ID'

    def get_actions(self, request):
        actions = super(OVCPlacementSAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(OVCPlacement, OVCPlacementSAdmin)


class OVCCaseCategoryInline(admin.StackedInline):
    model = OVCCaseCategory
    readonly_fields = ['person']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True


class OVCCaseGeoInline(admin.StackedInline):
    model = OVCCaseGeo
    readonly_fields = ['person']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True


class OVCCaseEventsInline(admin.StackedInline):
    model = OVCCaseEvents
    readonly_fields = ['placement_id', 'app_user']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True


class OVCCaseRecordAdmin(admin.ModelAdmin):
    search_fields = ['case_serial', 'person__first_name', 'person__id',
                     'person__surname', 'person__other_names']
    list_display = ['case_serial', 'person_id_display',
                    'person', 'timestamp_created', 'is_void']
    ordering = ('-timestamp_created',)

    list_filter = ['is_void', 'timestamp_created', 'case_stage',
                   'date_case_opened']

    readonly_fields = ['person']

    inlines = (OVCCaseCategoryInline, OVCCaseGeoInline, OVCCaseEventsInline, )

    actions = [dump_to_csv]

    def person_id_display(self, obj):
        return obj.person_id
    person_id_display.short_description = 'Person ID'

    def get_actions(self, request):
        actions = super(OVCCaseRecordAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(OVCCaseRecord, OVCCaseRecordAdmin)


class OVCCaseLoadAdmin(admin.ModelAdmin):
    search_fields = ['case_serial', 'cpims_id']
    list_display = ['cpims_id', 'case_serial', 'case_category',
                    'case_sub_category', 'org_unit', 'case_date',
                    'intervention']
    ordering = ('-date_case_opened',)

    list_filter = ['date_case_opened']

    # readonly_fields = ['person']

    actions = [dump_to_csv]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(OVCCaseLoadView, OVCCaseLoadAdmin)


class OVCCaseLocationAdmin(admin.ModelAdmin):
    """Admin back end for Geo data management."""

    search_fields = ['case_id', 'person__first_name', 'person__surname']
    list_display = ['case_id', 'person', 'report_country_code', 'report_city',
                    'get_creator']
    # readonly_fields = ['area_id']
    list_filter = ['is_void', 'report_country_code']

    def get_creator(self, obj):
        return obj.case.created_by
    get_creator.short_description = 'Creator'
    get_creator.admin_order_field = 'case__created_by'
    actions = [dump_to_csv, export_xls, export_xlsx]


admin.site.register(OVCCaseLocation, OVCCaseLocationAdmin)
