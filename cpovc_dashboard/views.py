from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse

from .forms import CaseLoad
from .functions import get_geo, get_lips, get_chart_data


@login_required
def ovc_dashboard(request):
    """Method to do pivot reports."""
    try:
        form = CaseLoad()
        return render(request, 'reports/ovc_dashboard.html', {'form': form})
    except Exception as e:
        raise e
    else:
        pass


@login_required
def ovc_dashboard_hivstat(request):
    """Method to do pivot reports."""
    try:
        form = CaseLoad()
        return render(
            request, 'reports/ovc_dashboard_hivstat.html', {'form': form})
    except Exception as e:
        raise e
    else:
        pass


@login_required
def ovc_dashboard_services(request):
    """Method to do pivot reports."""
    try:
        form = CaseLoad()
        return render(
            request, 'reports/ovc_dashboard_services.html', {'form': form})
    except Exception as e:
        raise e
    else:
        pass


@login_required
def ovc_dashboard_cm(request):
    """Method to do pivot reports."""
    try:
        form = CaseLoad()
        return render(
            request, 'reports/ovc_dashboard_cm.html', {'form': form})
    except Exception as e:
        raise e
    else:
        pass


@login_required
def get_constituency(request, area_id):
    """Method to do pivot reports."""
    try:
        values = []
        geos = get_geo(area_id)
        for geo in geos:
            vls = {'id': geo.area_id, 'name': geo.area_name}
            values.append(vls)
    except Exception:
        return JsonResponse([], safe=False)
    else:
        return JsonResponse(values, safe=False)


@login_required
def get_ward(request, area_id):
    """Method to do pivot reports."""
    try:
        values = []
        geos = get_geo(area_id, 'GWRD')
        for geo in geos:
            vls = {'id': geo.area_id, 'name': geo.area_name}
            values.append(vls)
    except Exception:
        return JsonResponse([], safe=False)
    else:
        return JsonResponse(values, safe=False)


@login_required
def get_lip(request, ip_id):
    """Method to do pivot reports."""
    try:
        values = []
        lips = get_lips(ip_id)
        for lip in lips:
            vls = {'id': lip.id, 'name': lip.org_unit_name}
            values.append(vls)
    except Exception:
        return JsonResponse([], safe=False)
    else:
        return JsonResponse(values, safe=False)


@login_required
def get_chart(request, rid, county_id, const_id, ward_id=0,
              ip_id=0, lip_id=0, prd=0, yr=0):
    """Method to do pivot reports."""
    try:
        html = get_chart_data(request, rid, county_id, const_id, ward_id,
                              ip_id, lip_id, prd, yr)
    except Exception as e:
        print('Chart view error - %s' % (str(e)))
        msg = 'Please change the Filters and try again.'
        return HttpResponse('<p>Error Generating Chart. %s</p>' % (msg))
    else:
        return HttpResponse(html)
