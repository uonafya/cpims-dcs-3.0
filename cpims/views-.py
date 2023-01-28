"""Main CPIMS common views."""
from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import JsonResponse
from cpovc_registry.functions import dashboard, ovc_dashboard
from cpovc_main.functions import get_dict
from cpovc_access.functions import access_request
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def home(request):
    """Some default page for the home page / Dashboard."""
    my_dates, my_cvals = [], []
    my_ovals, my_kvals = [], []
    my_dvals = []
    try:
        dash = dashboard(request)
        start_date = datetime.now() - timedelta(days=21)
        summary = {}
        summary['org_units'] = '{:,}'.format(dash['org_units'])
        summary['children'] = '{:,}'.format(dash['children'])
        summary['guardians'] = '{:,}'.format(dash['guardian'])
        summary['workforce'] = '{:,}'.format(dash['workforce_members'])
        summary['cases'] = '{:,}'.format(dash['case_records'])
        summary['pending'] = '{:08}'.format(dash['pending_cases'])
        summary['inst_girls'] = '{:,}'.format(dash['inst_pop']['G'])
        summary['inst_boys'] = '{:,}'.format(dash['inst_pop']['B'])
        pcases = float(dash['pending_cases'])
        tcases = float(dash['case_records'])
        intervens = (pcases / tcases) if tcases > 0 else 0
        interven = int(intervens * 100)
        print interven
        summary['interven'] = interven
        # OVC care
        odash = ovc_dashboard(request)
        ovc = {}
        ovc['org_units'] = '{:,}'.format(odash['org_units'])
        ovc['children'] = '{:,}'.format(odash['children'])
        ovc['children_all'] = '{:,}'.format(odash['children_all'])
        ovc['guardians'] = '{:,}'.format(odash['guardian'])
        ovc['workforce'] = '{:,}'.format(odash['workforce_members'])
        ovc['cases'] = '{:,}'.format(odash['case_records'])
        ovc['pending'] = '{:08}'.format(odash['pending_cases'])
        child_regs = dash['child_regs']
        ovc_regs = dash['ovc_regs']
        case_regs = dash['case_regs']
        case_cats = dash['case_cats']
        for date in range(0, 22, 2):
            end_date = start_date + timedelta(days=date)
            show_date = datetime.strftime(end_date, "%d-%b-%y")
            final_date = str(show_date).replace(' ', '&nbsp;')
            my_dates.append("[%s, '%s']" % (date, final_date))
        for vl in range(1, 22):
            t_date = start_date + timedelta(days=vl)
            s_date = datetime.strftime(t_date, "%d-%b-%y")
            k_count = child_regs[s_date] if s_date in child_regs else 0
            o_count = ovc_regs[s_date] if s_date in ovc_regs else 0
            c_count = case_regs[s_date] if s_date in case_regs else 0
            my_cvals.append("[%s, %s]" % (vl, c_count))
            my_kvals.append("[%s, %s]" % (vl, k_count))
            my_ovals.append("[%s, %s]" % (vl, o_count))
        dates = ', '.join(my_dates)
        kvals = ', '.join(my_kvals)
        cvals = ', '.join(my_cvals)
        ovals = ', '.join(my_ovals)
        my_dvals, cnt = [], 0
        colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00',
                  '#ffff33']
        # Case category names
        cat_names = get_dict(field_name=['case_category_id'])
        other_case = 0
        for case_cat in case_cats:
            cat_id = case_cat['case_category']
            cat_data = case_cat['unit_count']
            if cnt > 4:
                other_case += cat_data
            else:
                cname = cat_names[cat_id] if cat_id in cat_names else cat_id
                cat_name = cname[:16] + ' ...' if len(cname) > 16 else cname
                my_data = '{label: "%s", data: %s, color: "%s"}' % (
                    cat_name, cat_data, colors[cnt])
                my_dvals.append(my_data)
            cnt += 1
        if not case_cats:
            my_dvals.append('{label: "No data", data: 0, color: "#fd8d3c"}')
        if other_case > 0:
            my_dvals.append(
                '{label: "Others", data: %s, color: "#fb9a99"}' % (other_case))
        dvals = ', '.join(my_dvals)
        inst_list = ['TNAP', 'TNRH', 'TNRS', 'TNRR', 'TNRB', 'TNRC']
        sections = {}
        sections['SCCP'] = 'Child Protection'
        sections['SCPD'] = 'Planning and Development'
        sections['SCSI'] = 'Strategic Intervention'
        sections['SCCS'] = 'Community Child Support'
        sections['SAFC'] = 'Alternative Family Care'
        sections['SCIN'] = 'Institutions'
        sections['STIP'] = 'CTiP'
        section_id = request.session.get('section_id', 'XXXX')
        section = sections[section_id] if section_id in sections else ''
        return render(request, 'dashboard.html',
                      {'status': 200, 'dates': dates, 'kvals': kvals,
                       'dvals': dvals, 'cvals': cvals, 'data': summary,
                       'ovals': ovals, 'ovc': ovc, 'inst_list': inst_list,
                       'section': section})
    except Exception, e:
        print 'dashboard error - %s' % (str(e))
        raise e


def access(request):
    """Some default page for access login."""
    try:
        if request.method == 'POST':
            response = access_request(request)
            return JsonResponse(response, content_type='application/json',
                                safe=False)
        return render(request, 'home.html', {'status': 200, })
    except Exception, e:
        raise e


def handler_400(request):
    """Some default page for Bad request error page."""
    try:
        return render(request, '400.html', {'status': 400})
    except Exception, e:
        raise e


def handler_404(request):
    """Some default page for the Page not Found."""
    try:
        return render(request, '404.html', {'status': 404})
    except Exception, e:
        raise e


def handler_500(request):
    """Some default page for Server Errors."""
    try:
        return render(request, '500.html', {'status': 500})
    except Exception, e:
        raise e


def csrf_failure(request):
    """Some default page for CSRF error."""
    try:
        return render(request, 'csrf.html', {'status': 500})
    except Exception, e:
        raise e
