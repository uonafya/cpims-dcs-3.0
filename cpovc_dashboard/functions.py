import datetime
from django.db import connection
import collections

from cpovc_main.models import SetupGeography
from cpovc_registry.models import RegOrgUnit

from .parameters import PARAMS, areas, CHART
from .queries import QUERIES
from .charts import (
    column_chart, bar_chart, combo_chart, column_pie_chart)


def get_geo(area_id, type_id='GDIS'):
    """Method to get geo list"""
    try:
        print('geos', area_id, type_id)
        geos = SetupGeography.objects.filter(
            area_type_id=type_id, parent_area_id=area_id)
    except Exception as e:
        print('Error getting geo - %s' % (str(e)))
        return []
    else:
        return geos


def get_geo_by_id(area_id):
    """Method to get geo list"""
    try:
        geo = SetupGeography.objects.get(area_id=area_id)
    except Exception as e:
        print('Error getting geo by ID - %s' % (str(e)))
        return None
    else:
        return geo


def get_ip():
    """Method to get IP Listing."""
    try:
        initial_list = {'0': 'ALL IPs'}
        my_list = collections.OrderedDict(initial_list)
        ous = ['TNRL', 'TNPR', 'TNCF', 'TNCB', 'TNRI']
        ips = RegOrgUnit.objects.filter(
            parent_org_unit_id=2,
            org_unit_type_id__in=ous, is_void=False)
        for ip in ips:
            my_list[ip.id] = ip.org_unit_name
    except Exception as e:
        print('error getting IP - %s' % (str(e)))
        return (('', 'ALL IPs'), )
    else:
        return my_list.items


def get_lips(ip_id):
    """Method to get LIP Listing."""
    try:
        # print('IP', ip_id)
        lips = RegOrgUnit.objects.filter(
            parent_org_unit_id=ip_id, is_void=False)
    except Exception as e:
        print('error getting LIP', str(e))
        return []
    else:
        return lips


def get_chart_data(request, rid, county_id, const_id,
                   ward_id, ip_id, lip_id, prd, yr):
    """Method to get chart data."""
    try:
        params = {}
        area_type = 0
        area_id = 0
        if int(county_id) > 0:
            area_type = 1
            area_id = county_id
        if int(const_id) > 0:
            area_type = 2
            area_id = const_id
        if int(ward_id) > 1:
            area_type = 3
            area_id = ward_id
        params['area_id'] = int(area_id)
        params['area_type'] = area_type
        params['ip_id'] = int(ip_id)
        params['lip_id'] = int(lip_id)
        params['dates'] = ''
        params['cont'] = str(rid)
        dates = get_dates(prd, yr)
        params['start_date'] = dates['start_date']
        params['end_date'] = dates['end_date']
        data = get_raw_data(rid, params)
        ctt = CHART[rid] if rid in CHART else CHART['2A']
        params['title'] = '%s : %s' % (rid, ctt['ctitle'])
        if ctt['ctype'] == 'bar':
            resp = bar_chart(request, params, data)
        elif ctt['ctype'] == 'combo':
            resp = combo_chart(request, params, data)
        elif ctt['ctype'] == 'column_pie':
            resp = column_pie_chart(request, params, data)
        else:
            resp = column_chart(request, params, data)
    except Exception as e:
        print('Chart error - %s' % (str(e)))
        raise e
    else:
        return resp


def get_dates(prd, yr):
    """Method to get dates based on Reporting period and FY."""
    try:
        dates = {}
        int_yr = int(yr)
        today = datetime.date.today()
        year = today.strftime('%Y')
        mwezi = today.strftime('%m')
        w_year = int(year) if int_yr == 0 else int_yr
        mwaka = (w_year + 1) if int(mwezi) > 9 else w_year
        emonth = '03' if int(prd) == 2 else '09'
        start_date = '%d-10-01' % (w_year)
        end_date = '%d-%s-30' % (mwaka, emonth)
        dates['start_date'] = start_date
        dates['end_date'] = end_date
    except Exception as e:
        print('Get dates error - %s' % (str(e)))
        raise e
    else:
        return dates


def get_region(area_id, area_type):
    """Method to get the region."""
    try:
        # area = str(area_id).zfill(3)
        atype = '%s' % (areas[area_type]) if area_type in areas else 'National'
        aname = ''
        if area_type == 1:
            aname = PARAMS[area_id] if area_id in PARAMS else 'Unknown'
        if area_type >= 2:
            geo = get_geo_by_id(area_id)
            aname = geo.area_name if geo else 'Unknown'

        region = '%s %s' % (aname, atype)
    except Exception as e:
        raise e
    else:
        return region


def dictfetchall(cursor):
    """Return all rows from a cursor as a dict"""
    column = [col[0] for col in cursor.description]
    columns = [col for col in column]
    return [
        collections.OrderedDict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def get_raw_sql(rid, params):
    """Method to get the query."""
    try:
        # rows = []
        q = QUERIES[rid] if rid in QUERIES else QUERIES['1A'].format(**params)
        sql = q.format(**params)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            # rows = cursor.fetchall()
            # desc = cursor.description
            rows = dictfetchall(cursor)
            # rows = [row for row in cursor.fetchall()]
        # print('query', rows)
    except Exception as e:
        raise e
    else:
        return rows


def get_raw_data(rid, params):
    """Method to get the raw data."""
    try:
        # print('params', params)
        cbos_list, cbos = [], []
        data = {}
        ip_id = params['ip_id']
        lip_id = params['lip_id']
        area_id = params['area_id']
        area_type = params['area_type']
        if ip_id > 0 and lip_id == 0:
            lips = get_lips(ip_id)
            for lip in lips:
                cbos_list.append(lip.id)
                cbos.append(str(lip.id))
            # Handle IPs that are also LIPs
            cbos_list.append(ip_id)
            cbos.append(str(ip_id))
        if lip_id > 0:
            cbos_list = [lip_id]
            cbos = [str(lip_id)]
        # CBO Query Filters
        cboq, cbov, ocboq = '', '', ''
        if len(cbos) > 0:
            cboq = "AND cbo_id in (%s)" % ','.join(cbos)
            cbov = "AND v.cbo_id in (%s)" % ','.join(cbos)
            ocboq = "WHERE cbo_id in (%s)" % ','.join(cbos)
        # Area Query filters
        qarea, oqarea = '', ''
        if area_id > 0:
            if area_type == 3:
                areaq = " ward_id = %d" % (area_id)
            elif area_type == 2:
                areaq = " consituency_id = %d" % (area_id)
            elif area_type == 1:
                areaq = " countyid = %d" % (area_id)
            qarea = "AND %s" % (areaq)
            if ocboq == '':
                oqarea = "WHERE %s" % (areaq)
            else:
                oqarea = "AND %s" % (areaq)
        qparams = {'cbos': cboq, 'ocbos': ocboq, 'vcbos': cbov,
                   'areas': qarea, 'oareas': oqarea}
        # Date filters
        cur_chart = CHART[rid]
        fdt = cur_chart['dfilter'] if 'dfilter' in cur_chart else ''
        if fdt:
            sdate = params['start_date']
            edate = params['end_date']
            dquery = "AND %s BETWEEN '%s' AND '%s'" % (fdt, sdate, edate)
            fdates = "AND %s <= '%s'" % (fdt, edate)
            odate = "AND %s <= '%s'" % (fdt, edate)
            odates = " %s BETWEEN '%s' AND '%s'" % (fdt, sdate, edate)
            # Change filter clause if its only one
            if ocboq == '' and oqarea == '':
                odate = "WHERE %s <= '%s'" % (fdt, edate)
        else:
            dquery = ""
            fdates = ""
            odate = ""
            odates = ""
        qparams['dates'] = dquery
        qparams['fdate'] = fdates
        qparams['odate'] = odate
        qparams['odates'] = odates
        datas = get_raw_sql(rid, qparams)
        # print('Query ID', rid, datas)
        print('Query filter', qparams)
        items = CHART[rid]['categories']
        itd = CHART[rid]['qparam']
        if len(items) == 0:
            items, rdata = format_other_data(datas, items, itd)
        else:
            rdata = format_data(rid, datas, items, itd)
        # print('Final data', rid, rdata)
        data['items'] = items
        for rdt in rdata:
            data[rdt] = rdata[rdt]
    except Exception as e:
        print('error getting data - %s' % (str(e)))
        return {}
    else:
        return data


def format_data(rid, datas, items, itd='agerange'):
    """Method to format data."""
    try:
        rdata = {}
        mdata = ['0'] * len(items)
        fdata = ['0'] * len(items)
        males = ['SMAL', 'Male']
        females = ['SFEM', 'Female']
        for i, itm in enumerate(items):
            for data in datas:
                if itd in data and data[itd] == itm:
                    if data['sex_id'] in males:
                        mdata[i] = str(int(data['dcount']))
                    elif data['sex_id'] in females:
                        fdata[i] = str(int(data['dcount']))
        rdata['mdata'] = ','.join(mdata)
        if rid in ['2D']:
            fdata = format_percentage(rid, mdata, fdata)
        rdata['fdata'] = ','.join(fdata)
        # print(data)
    except Exception as e:
        print('error with default data - %s' % (str(e)))
        return {}
    else:
        return rdata


def format_percentage(rid, adata, bdata):
    """Method to calculate percentage of bdata out of adata."""
    try:
        fdata = ['0'] * len(bdata)
        for i, itm in enumerate(bdata):
            d_data = float(int(adata[i]))
            n_data = float(int(bdata[i]))
            p_data = (n_data / d_data) * 100 if d_data > 0 else 0
            print('Newton', d_data, n_data, p_data)
            fdata[i] = str(round(p_data, 1))
    except Exception:
        return bdata
    else:
        return fdata


def format_other_data(datas, items=[], itd='services'):
    """Method to format data."""
    try:
        all_data = {}
        rdata = {}
        mdata = []
        fdata = []
        males = ['SMAL', 'Male']
        females = ['SFEM', 'Female']
        for data in datas:
            if itd in data:
                sname = data[itd]
                if sname not in all_data:
                    all_data[sname] = {'mdata': '0', 'fdata': '0'}
                # print('--', data, all_data)
                if data['sex_id'] in males:
                    all_data[sname]['mdata'] = str(int(data['dcount']))
                elif data['sex_id'] in females:
                    all_data[sname]['fdata'] = str(int(data['dcount']))
        # Now format the dict to array for charting
        print('all data', all_data)
        for adata in all_data:
            items.append(str(adata))
            mdata.append(all_data[adata]['mdata'])
            fdata.append(all_data[adata]['fdata'])
        rdata['mdata'] = ','.join(mdata)
        rdata['fdata'] = ','.join(fdata)
        # print(data)
    except Exception as e:
        print('error with other data - %s' % (str(e)))
        return [], {}
    else:
        return items, rdata
