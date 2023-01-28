import operator
import json
from django.contrib import admin
from django.db.models import Count, Min, Max
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.conf.urls import url
from .models import SIPopulation, SystemUsage, CCIPopulation
from cpovc_registry.models import RegOrgUnit


def get_next_in_date_hierarchy(request, date_hierarchy):
    if date_hierarchy + '__day' in request.GET:
        return 'hour'
    if date_hierarchy + '__month' in request.GET:
        return 'day'
    if date_hierarchy + '__year' in request.GET:
        return 'week'
    return 'month'


@admin.register(SIPopulation)
class SIPopulationAdmin(admin.ModelAdmin):
    change_list_template = 'admin/si_summary_list.html'
    date_hierarchy = 'timestamp_created'

    show_full_result_count = False

    list_per_page = 25

    list_filter = ('is_active', 'is_void', 'timestamp_created',
                   'residential_institution__org_unit_type_id')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True

    def changelist_view(self, request, extra_context=None):
        response = super(SIPopulationAdmin, self).changelist_view(
            request, extra_context=extra_context,)
        si_types = ['TNRR', 'TNAP', 'TNRH', 'TNRS', 'TNRB']
        sis = {'TNRR': 'Rescue', 'TNAP': 'Reception', 'TNRH': 'Remand',
               'TNRS': 'Rehab', 'TNRB': 'Borstal'}
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {'total': Count('placement_id'), }
        org_units = RegOrgUnit.objects.filter(org_unit_type_id__in=si_types)

        vls = qs.values(
            'residential_institution_name',
            'person__sex_id').annotate(
            **metrics).order_by('-total')
        # response.context_data['summary'] = list(vls)
        dts, ous, ouds = [], {}, {}
        tboys, tgirls = 0, 0
        for vl in vls:
            org_unit = int(vl['residential_institution_name'])
            if org_unit not in ouds:
                ouds[org_unit] = {'boys': 0, 'girls': 0}
            pop = vl['person__sex_id']
            if pop == 'SMAL':
                ouds[org_unit]['boys'] = vl['total']
            else:
                ouds[org_unit]['girls'] = vl['total']
        for ou in org_units:
            org_id = ou.id
            org_type = ou.org_unit_type_id
            if ou not in ous:
                ous[ou.org_unit_name] = {'boys': 0, 'girls': 0,
                                         'org_type': org_type}
            boys = ouds[org_id]['boys'] if org_id in ouds else 0
            girls = ouds[org_id]['girls'] if org_id in ouds else 0
            ous[ou.org_unit_name]['girls'] = girls
            ous[ou.org_unit_name]['boys'] = boys

        sous = dict(sorted(ous.items(), key=operator.itemgetter(1)))
        for ou in sous:
            girls = ous[ou]['girls']
            boys = ous[ou]['boys']
            org_type_id = ous[ou]['org_type']
            org_type = sis[org_type_id] if org_type_id in sis else 'N/A'
            tboys += boys
            tgirls += girls
            orgs = {'org_unit': ou, 'girls': girls, 'boys': boys,
                    'total': girls + boys, 'org_type': org_type}
            dts.append(orgs)
        response.context_data['summary'] = dts

        # List view summary
        tdict = {'boys': tboys, 'girls': tgirls, 'totals': tboys + tgirls}
        response.context_data['summary_total'] = tdict

        # Chart
        period = get_next_in_date_hierarchy(request, self.date_hierarchy)
        response.context_data['period'] = period
        summary_over_time = qs.extra(
            select={'day': 'date( timestamp_created )'}).annotate(
            period=Count('timestamp_created'),).values(
            'period').annotate(total=Count(
                'placement_id')).order_by('period')

        summary_range = summary_over_time.aggregate(
            low=Min('total'),
            high=Max('total'),
        )
        high = summary_range.get('high', 0)
        low = summary_range.get('low', 0)

        response.context_data['summary_over_time'] = [{
            'period': x['period'],
            'total': x['total'] or 0,
            'pct':
            ((x['total'] or 0) - low) / (high - low) * 100
            if high > low else 0,
        } for x in summary_over_time]

        return response


@admin.register(CCIPopulation)
class CCIPopulationAdmin(admin.ModelAdmin):
    change_list_template = 'admin/si_summary_list.html'
    date_hierarchy = 'timestamp_created'

    show_full_result_count = False

    list_per_page = 10

    list_filter = ('is_active', 'timestamp_created',
                   'residential_institution__org_unit_type_id')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True

    def changelist_view(self, request, extra_context=None):
        response = super(CCIPopulationAdmin, self).changelist_view(
            request, extra_context=extra_context,)
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {'total': Count('placement_id'), }
        cci_types = ['TNRC']

        vls = qs.filter(
            residential_institution__org_unit_type_id__in=cci_types).values(
            'residential_institution__org_unit_name',
            'person__sex_id').annotate(
            **metrics).order_by('-total')
        # response.context_data['summary'] = list(vls)
        dts, ous = [], {}
        tboys, tgirls = 0, 0
        for vl in vls:
            org_unit = vl['residential_institution__org_unit_name']
            if org_unit not in ous:
                ous[org_unit] = {'boys': 0, 'girls': 0}
            pop = vl['person__sex_id']
            if pop == 'SMAL':
                ous[org_unit]['boys'] = vl['total']
            else:
                ous[org_unit]['girls'] = vl['total']
        sous = dict(sorted(ous.items(), key=operator.itemgetter(1)))
        for ou in sous:
            girls = ous[ou]['girls']
            boys = ous[ou]['boys']
            tboys += boys
            tgirls += girls
            orgs = {'org_unit': ou, 'girls': girls, 'boys': boys,
                    'total': girls + boys}
            dts.append(orgs)
        response.context_data['summary'] = dts

        # List view summary
        tdict = {'boys': tboys, 'girls': tgirls, 'totals': tboys + tgirls}
        response.context_data['summary_total'] = tdict

        # Chart
        period = get_next_in_date_hierarchy(request, self.date_hierarchy)
        response.context_data['period'] = period
        summary_over_time = qs.extra(
            select={'day': 'date( timestamp_created )'}).annotate(
            period=Count('timestamp_created'),).values(
            'period').annotate(total=Count(
                'placement_id')).order_by('period')

        summary_range = summary_over_time.aggregate(
            low=Min('total'),
            high=Max('total'),
        )
        high = summary_range.get('high', 0)
        low = summary_range.get('low', 0)

        response.context_data['summary_over_time'] = [{
            'period': x['period'],
            'total': x['total'] or 0,
            'pct':
            ((x['total'] or 0) - low) / (high - low) * 100
            if high > low else 0,
        } for x in summary_over_time]

        return response


@admin.register(SystemUsage)
class SystemUsageAdmin(admin.ModelAdmin):
    # change_list_template = 'admin/system_usage.html'
    date_hierarchy = 'date_began'
    list_display = ("person_type_id", "person", "date_began")
    list_per_page = 10

    # actions = None

    # show_full_result_count = False

    list_filter = (
        'person_type_id', 'person__created_at', 'date_began'
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True

    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day
        print request.GET
        syqs = SystemUsage.objects.filter(is_void=False)
        if 'person_type_id' in request.GET:
            syqs.filter(person_type_id=request.GET['person_type_id'])
        for vl in request.GET:
            if vl.startswith('date_began__'):
                print 'VL', vl
                syqs.filter(date_began=request.GET[vl])
        chart_data = (
            syqs.extra(
                select={'date': 'date( date_began )'})
            .values("date")
            .annotate(y=Count("person_type_id"))
            .order_by("-date")
        )
        # print chart_data
        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super(SystemUsageAdmin, self).changelist_view(
            request, extra_context=extra_context)

    def get_urls(self):
        urls = super(SystemUsageAdmin, self).get_urls()
        extra_urls = [
            url(r'^chart_data/$',
                self.admin_site.admin_view(self.chart_data_endpoint))
        ]
        return extra_urls + urls

    def chart_data_endpoint(self, request):
        chart_data = self.chart_data()
        return JsonResponse(list(chart_data), safe=False)

    def chart_data(self):
        return (
            SystemUsage.objects.filter(is_void=False).extra(
                select={'date': 'date( date_began )'})
            .values("date")
            .annotate(y=Count("person_type_id"))
            .order_by("-date")
        )
