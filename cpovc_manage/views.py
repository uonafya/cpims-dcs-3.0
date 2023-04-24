import collections
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from .models import NOTTTravel, NOTTChaperon, NOTTChild, OvcCasePersons
from .forms import NOTTForm, ChaperonForm, ChildrenForm
from django.forms.models import model_to_dict
from cpovc_forms.models import OVCBasicCRS, OVCBasicCategory, OVCBasicPerson
from cpovc_registry.models import (
    RegPerson, RegPersonsExternalIds, RegOrgUnit, RegPersonsOrgUnits,
    RegOrgUnitGeography)

from cpovc_main.functions import get_dict, convert_date

from django.db.models import Q
from cpovc_reports.forms import CaseLoad

from cpovc_reports.models import RPTCaseLoad
from .functions import (
    travel_pdf, handle_integration, get_geo, get_person_geo,
    get_person_orgs, generate_document, report_bug)
from cpovc_main.models import SetupGeography

from .params import PARAMS


@login_required(login_url='/')
def manage_home(request):
    """Main home method and view."""
    try:
        return render(request, 'management/home.html',
                      {'form': {}})
    except Exception as e:
        raise e
    else:
        pass


@login_required(login_url='/')
def home_travel(request):
    """Main home method and view."""
    try:
        form = CaseLoad(request.user)
        if request.method == 'POST':
            dts, vals = {}, {}
            dtls = ['is_void', 'sync_id', 'id']
            item_id = request.POST.get('item_id')
            data = NOTTTravel.objects.filter(
                is_void=False, pk=item_id).values()[0]
            for dt in data:
                if data[dt] is not None and data[dt] != '' and dt not in dtls:
                    dval = vals[data[dt]] if data[dt] in vals else data[dt]
                    if isinstance(dval, (bool)):
                        dval = 'Yes' if dval else 'No'
                    dts[dt.replace('_', ' ').capitalize()] = dval
            datas = collections.OrderedDict(sorted(dts.items()))
            results = {'message': 'Good', 'status': 0, 'dates': '0000',
                       'data': datas}
            return JsonResponse(results, content_type='application/json',
                                safe=False)
        cases = NOTTTravel.objects.filter(is_void=False)
        return render(request, 'management/home_travel.html',
                      {'form': form, 'cases': cases})
    except Exception as e:
        raise e
    else:
        pass


@login_required(login_url='/')
def new_travel(request):
    """Main home method and view."""
    try:
        if request.method == 'POST':
            item_id = request.POST.get('item_id')
            print(item_id)
        return render(request, 'management/edit_travel.html',
                      {'form': {}})
    except Exception as e:
        raise e
    else:
        pass


@login_required(login_url='/')
def view_travel(request, id):
    """Main home method and view."""
    try:
        if request.method == 'POST':
            item_id = request.POST.get('item_id')
            print(item_id)
        travel = NOTTTravel.objects.get(is_void=False, id=id)
        chaperons = NOTTChaperon.objects.filter(travel_id=id)
        children = NOTTChild.objects.filter(travel_id=id)
        return render(request, 'management/view_travel.html',
                      {'form': {}, 'travel': travel,
                       'chaperons': chaperons, 'children': children})
    except Exception as e:
        raise e
    else:
        pass


@login_required(login_url='/')
def travel_report(request, id):
    """Main home method and view."""
    try:
        file_name = 'National_Travel-Authorization_%s' % (id)
        fname = '%s.pdf' % (file_name)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="%s"' % (fname)
        travel_pdf(request, response, file_name)
        return response
    except Exception as e:
        raise e
    else:
        pass


@login_required(login_url='/')
def edit_travel(request, id):
    """Main home method and view."""
    try:
        ChaperonFormset = formset_factory(ChaperonForm, extra=0)
        ChildrenFormset = formset_factory(ChildrenForm, extra=0)
        if request.method == 'POST':
            travel = NOTTTravel.objects.get(is_void=False, id=id)
            tdate = request.POST.get('travel_date')
            return_date = request.POST.get('return_date')
            no_applied = request.POST.get('no_applied')
            no_cleared = request.POST.get('no_cleared')
            no_returned = request.POST.get('no_returned')
            comments = request.POST.get('comments')
            contacts = request.POST.get('contacts')
            sponsor = request.POST.get('sponsor')
            reason = request.POST.get('reason')
            status_id = request.POST.get('status')
            status = 1 if status_id == 'on' else 0
            institution_name = request.POST.get('institution_name')
            country_name = request.POST.get('country_name')
            travel_date = convert_date(tdate)
            if return_date:
                return_date = convert_date(return_date)
            travel.travel_date = travel_date
            travel.return_date = return_date
            travel.contacts = contacts
            travel.comments = comments
            travel.sponsor = sponsor
            travel.reason = reason
            travel.status = status
            travel.institution_name = institution_name
            travel.country_name = country_name
            # travel.save()
            # Chaperon
            formset = ChaperonFormset(request.POST, prefix='chap')
            cformset = ChildrenFormset(request.POST, prefix='child')
            print(request.POST)
            clear_count, return_count = 0, 0
            if formset.is_valid():
                if formset.has_changed():
                    for echap in formset.cleaned_data:
                        ops = OvcCasePersons.objects.get(pk=echap['person_id'])
                        ops.person_sex = echap['sex']
                        ops.person_first_name = echap['first_name']
                        ops.person_other_names = echap['other_names']
                        ops.person_surname = echap['surname']
                        ops.person_identifier = echap['passport_no']
                        ops.save()
            else:
                print(formset.errors)
            if cformset.is_valid():
                if cformset.has_changed():
                    no_applied = len(cformset.cleaned_data)
                    for echild in cformset.cleaned_data:
                        cid = echild['person_id']
                        cidc = echild['cleared']
                        cidr = echild['returned']
                        cid_cleared = True if cidc == 'True' else False
                        cid_returned = True if cidr == 'True' else False
                        if cid_cleared:
                            clear_count += 1
                        if cid_returned:
                            return_count += 1
                        opc = RegPerson.objects.get(pk=cid)
                        opc.sex_id = echild['sex']
                        opc.first_name = echild['first_name']
                        opc.other_names = echild['other_names']
                        opc.surname = echild['surname']
                        opc.save()
                        # Update passport Number
                        cpp = RegPersonsExternalIds.objects.get(
                            person_id=cid, is_void=False,
                            identifier_type_id='IPPN')
                        cpp.identifier = echild['passport_no']
                        cpp.save()
                        # Update Returned / Cleared details
                        ch = NOTTChild.objects.get(travel_id=id, person_id=cid)
                        ch.returned = cid_returned
                        ch.cleared = cid_cleared
                        ch.save()
                        print(echild)
                    no_returned = return_count
                    no_cleared = clear_count
            else:
                print(cformset.errors)
            travel.no_applied = no_applied
            travel.no_cleared = no_cleared
            travel.no_returned = no_returned
            travel.save()
            url = reverse(view_travel, kwargs={'id': id})
            return HttpResponseRedirect(url)
        travel = NOTTTravel.objects.filter(is_void=False, id=id).values()[0]
        travel_date = travel['travel_date'].strftime('%d-%b-%Y')
        return_date = None
        if travel['return_date']:
            return_date = travel['return_date'].strftime('%d-%b-%Y')
        travel['travel_date'] = travel_date
        travel['return_date'] = return_date
        nott_form = NOTTForm(travel)
        # Chaperons
        chaps = []
        chaperons = NOTTChaperon.objects.filter(travel_id=id)
        for chap in chaperons:
            chap_details = {'first_name': chap.other_person.person_first_name}
            chap_details['surname'] = chap.other_person.person_surname
            chap_details['other_names'] = chap.other_person.person_other_names
            chap_details['sex'] = chap.other_person.person_sex
            chap_details['passport_no'] = chap.other_person.person_identifier
            chap_details['person_id'] = chap.other_person_id
            chap_details['chaperon_id'] = chap.id
            chaps.append(chap_details)
        chap_formset = ChaperonFormset(initial=chaps, prefix='chap')
        # Children
        tchildren = []
        children = NOTTChild.objects.filter(travel_id=id)
        for child in children:
            child_details = {'first_name': child.person.first_name}
            child_details['surname'] = child.person.surname
            child_details['other_names'] = child.person.other_names
            child_details['sex'] = child.person.sex_id
            child_details['passport_no'] = child.passport
            child_details['person_id'] = child.person_id
            child_details['child_id'] = child.id
            child_details['cleared'] = child.cleared
            child_details['returned'] = child.returned
            tchildren.append(child_details)
        child_formset = ChildrenFormset(initial=tchildren, prefix='child')
        return render(request, 'management/edit_travel.html',
                      {'form': nott_form, 'travel': travel,
                       'chap_formset': chap_formset,
                       'child_formset': child_formset})
    except Exception as e:
        raise e
    else:
        pass


# Create your views here.
@login_required(login_url='/')
def integration_home(request):
    """Method to do pivot reports."""
    try:
        persons = {}
        categories = {}
        case_data = {}
        case_ids = []
        svals = {}
        user_id = request.user.id
        # form = CaseLoad(request.user)
        user_counties, user_geos = get_person_geo(request)
        print('Geos', user_counties, user_geos)
        rm_fields = ['is_void', 'account', 'case_serial']
        check_fields = ['sex_id', 'case_category_id', 'case_reporter_id',
                        'family_status_id', 'household_economics',
                        'risk_level_id', 'mental_condition_id',
                        'perpetrator_status_id', 'other_condition_id',
                        'physical_condition_id', 'yesno_id']
        vals = get_dict(field_name=check_fields)
        if request.method == 'POST':
            item_id = request.POST.get('item_id')
            case = OVCBasicCRS.objects.get(
                case_id=item_id, is_void=False)
            cdata = model_to_dict(case)
            for cd in cdata:
                cdt = cdata[cd]
                if len(str(cdt)) < 6 and cdt in vals:
                    cdt = vals[cdt]
                if cdt and cd not in rm_fields:
                    case_data[cd] = cdt
                if cdt and (cd == 'county' or cd == 'constituency'):
                    cid = 'GPRV' if cd == 'county' else 'GDIS'
                    cd_name = '%s name' % (cd)
                    geo = get_geo(int(cdt), cid)
                    if geo:
                        geo_name = geo.area_name
                        case_data[cd_name] = geo_name
            results = {'status': 0, 'message': 'Successful', 'dates': '',
                       'data': case_data}
            return JsonResponse(results, content_type='application/json',
                                safe=False)
        cases = OVCBasicCRS.objects.filter(is_void=False)
        if not request.user.is_superuser:
            if request.user.username == 'vurugumapper':
                cases = cases.filter(account_id=user_id)
            else:
                cases = cases.filter(county__in=user_counties)
        # Get filters from the URL
        cases = cases.order_by('-timestamp_created')
        case_source = request.GET.get('case_source', None)
        case_totals = int(request.GET.get('case_totals', 100))
        case_status = request.GET.get('case_status', 0)
        from_date = request.GET.get('report_from_date', None)
        to_date = request.GET.get('report_to_date', None)
        svals['case_totals'] = case_totals
        svals['case_source'] = case_source
        svals['case_status'] = case_status
        if from_date and to_date:
            sdate = convert_date(from_date)
            edate = convert_date(to_date)
            svals['report_from_date'] = from_date
            svals['report_to_date'] = to_date
            cases = cases.filter(case_date__range=(sdate, edate))
        if case_source:
            cases = cases.filter(account_id=case_source)
        if case_status:
            cases = cases.filter(status=case_status)
        cases = cases[:case_totals]
        for cs in cases:
            case_ids.append(cs.case_id)
        case_cats = OVCBasicCategory.objects.filter(
            is_void=False, case_id__in=case_ids)
        case_pers = OVCBasicPerson.objects.filter(
            is_void=False, case_id__in=case_ids)
        for ccat in case_cats:
            categories[ccat.case_id] = ccat
        for cpers in case_pers:
            pers_type = cpers.person_type
            if pers_type == 'PTCH':
                persons[cpers.case_id] = cpers
        for c in cases:
            cid = c.case_id
            category = categories[cid] if cid in categories else None
            child = persons[cid] if cid in persons else None
            setattr(c, 'category', category)
            setattr(c, 'child', child)
        iform = CaseLoad(request.user, svals)
        return render(request, 'management/integration.html',
                      {'form': iform, 'cases': cases, 'vals': vals})
    except Exception as e:
        print(e)
        raise e
    else:
        pass


@login_required
def process_integration(request, case_id):
    """Method to process case."""
    try:
        case = OVCBasicCRS.objects.get(case_id=case_id, is_void=False)
        county_code = int(case.county)
        const_code = int(case.constituency)
        county_id, const_id = 0, 0
        crs_id = str(case_id).replace('-', '')
        user_counties, user_geos = get_person_geo(request)
        # Get person orgs
        ou_ids = get_person_orgs(request)
        if request.method == 'POST':
            response = handle_integration(request, case, case_id)
            print(response)
        check_fields = ['sex_id', 'case_category_id', 'case_reporter_id',
                        'family_status_id', 'household_economics',
                        'risk_level_id', 'mental_condition_id',
                        'perpetrator_status_id', 'other_condition_id',
                        'physical_condition_id', 'yesno_id']
        vals = get_dict(field_name=check_fields)
        category = OVCBasicCategory.objects.filter(
            case_id=case_id, is_void=False)
        person = OVCBasicPerson.objects.filter(case_id=case_id, is_void=False)
        # Attached Geos and Org Units for the user
        # ou_ids = []
        org_id = request.session.get('ou_primary', 0)
        ou_ids.append(org_id)
        ou_attached = request.session.get('ou_attached', 0)
        user_level = request.session.get('user_level', 0)
        user_type = request.session.get('user_type', 0)
        print(org_id, ou_attached, user_level, user_type)
        # person_id = request.user.reg_person_id
        county = SetupGeography.objects.filter(
            area_code=county_code, area_type_id='GPRV')
        for c in county:
            county_id = c.area_id
        # Get constituency
        constituency = SetupGeography.objects.filter(
            area_code=const_code, area_type_id='GDIS')
        for c in constituency:
            const_id = c.area_id
        ous = RegOrgUnit.objects.filter(is_void=False)
        counties = SetupGeography.objects.filter(area_type_id='GPRV')
        if user_counties:
            counties = counties.filter(area_id__in=user_counties)
        if request.user.is_superuser:
            all_ou_ids = ['TNGD']
            ous = ous.filter(org_unit_type_id__in=all_ou_ids)
            geos = SetupGeography.objects.filter(
                area_type_id='GDIS', parent_area_id=county_id)
        else:
            ous = ous.filter(id__in=ou_ids)
            geos = SetupGeography.objects.filter(
                area_type_id='GDIS', parent_area_id=county_id)
        return render(request, 'management/integration_process.html',
                      {'form': {}, 'case': case, 'vals': vals,
                       'category': category, 'person': person,
                       'geos': geos, 'ous': ous, 'counties': counties,
                       'county_id': county_id, 'const_id': const_id,
                       'crs_id': crs_id})
    except Exception as e:
        print('Error processing integration - %s' % (e))
    else:
        pass


@login_required
def get_document(request, doc_id, case_id):
    """Some default page for reports home page."""
    try:
        case = OVCBasicCRS.objects.get(case_id=case_id, is_void=False)
        person_id = str(1).zfill(6)
        ou = case.case_org_unit
        params = {}
        params['ref_to'] = ou.org_unit_name if ou else ''
        params['ref_from'] = 'HELPLINE 116'
        # Get the persons attached to this case
        child = {'name': '', 'sex': ''}
        mum, dad = '', ''
        persons = OVCBasicPerson.objects.filter(case_id=case_id, is_void=False)
        for person in persons:
            print('person', person.person_type, person.first_name, person.sex)
            if person.person_type == 'PTCH':
                name = '%s %s' % (person.first_name, person.surname)
                sex = 'Male' if person.sex == 'SMAL' else 'Female'
                child = {'name': name.upper(), 'sex': sex.upper()}
            if person.person_type == 'PTCG':
                name = '%s %s' % (person.first_name, person.surname)
                sex = 'Male' if person.sex == 'SMAL' else 'Female'
                if person.sex == 'SMAL':
                    dad = name.upper()
                else:
                    mum = name.upper()
        params['child'] = child
        params['mum'] = mum
        params['dad'] = dad
        response = HttpResponse(content_type='application/pdf')
        fname = 'U%s-%s' % (person_id, str(doc_id))
        f_name = 'attachment; filename=%s.pdf' % (fname)
        response['Content-Disposition'] = f_name
        generate_document(request, response, params, case)
        return response
    except Exception as e:
        print('Error writing report - %s' % (str(e)))
        raise e


@login_required(login_url='/')
def dq_home(request):
    """Main home method and view."""
    try:
        form = CaseLoad(request.user)
        return render(request, 'management/dq_home.html',
                      {'form': form})
    except Exception as e:
        print('error - %s' % (e))
        raise e
    else:
        pass


def dq_data(request):
    """Main home method and view."""
    try:
        cases = []
        sdate, edate = None, None
        sts = {0: 'Pending', 1: 'Open', 2: 'Closed'}
        # Conditions
        qa = request.GET.get('q_aspect')
        va = request.GET.get('variance')
        age = request.GET.get('age')
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        ou = request.GET.get('org_unit')
        org_unit = int(ou) if ou else 0
        if from_date and to_date:
            sdate = convert_date(from_date)
            edate = convert_date(to_date)
        cage = int(age) if age else 0
        vid = int(va) if va else 0
        qid = int(qa) if qa else 0
        q2 = Q(case_category_id__in=('CTRF', 'CCCT'), age__lt=6)
        q3 = Q(case_category_id__in=('CSAB', 'CSHV', 'CCCM', 'CORP'),
               age__lt=11)
        if qa:
            acases = RPTCaseLoad.objects.filter(is_void=False)
            if qid == 1:
                acases = acases.filter(
                    Q(age__gte=25) | Q(dob__isnull=True) | Q(age__lt=0))
            elif qid == 2:
                acases = acases.filter(
                    Q(case_category_id='CDIS',
                      age__gt=15) | Q(case_category_id='CSIC',
                                      age__gt=18) | q2 | q3)
            elif qid == 3:
                acases = acases.filter(
                    case_category_id__in=('CSHV', 'CSCS'), sex_id='SMAL')
            elif qid == 4:
                acases = acases.filter(
                    case_status=1, intervention__isnull=True)
        else:
            acases = RPTCaseLoad.objects.filter(
                Q(age__gte=25) | Q(dob__isnull=True))
        if vid == 1:
            acases = acases.filter(age=cage)
        elif vid == 2:
            acases = acases.filter(age__gt=cage)
        elif vid == 3:
            acases = acases.filter(age__lt=cage)
        if edate and sdate:
            acases = acases.filter(case_date__range=(sdate, edate))
        if org_unit:
            acases = acases.filter(org_unit_id=org_unit)
        else:
            if not request.user.is_superuser:
                acases = acases.filter(org_unit_id=org_unit)
        fcases = acases.order_by('-case_date')[:1000]
        cnt = 0
        for case in fcases:
            cnt += 1
            cs = case.case_status
            fname = case.case.person.first_name
            sname = case.case.person.surname[0]
            o_name = case.case.person.other_names
            oname = o_name[0] if o_name else ''
            dt = {"id": cnt, "cpims_id": case.case.person_id}
            dt['age'] = case.age
            dt['case_category'] = case.case_category
            dt['case_date'] = case.case_date
            dt['sex'] = case.sex
            dt['case_status'] = sts[cs] if cs in sts else 'Open'
            dt['dob'] = case.dob
            dt['org_unit'] = case.org_unit_name
            dt['intervention'] = case.intervention
            dt['org_unit'] = case.org_unit_name
            dt['names'] = '%s %s%s' % (fname, sname, oname)
            cases.append(dt)
        result = {"data": cases}
        return JsonResponse(result, content_type='application/json',
                            safe=False)
    except Exception as e:
        print('error - %s' % (e))
        raise e
    else:
        pass


@login_required(login_url='/')
def se_home(request):
    """Main home method and view."""
    try:
        form = CaseLoad(request.user)
        return render(request, 'management/se_home.html',
                      {'form': form})
    except Exception as e:
        raise e
    else:
        pass


def se_data(request):
    """Main home method and view."""
    try:
        cases = []
        ou_ids = []
        org_unit = request.GET.get('org_unit')
        county = request.GET.get('county')

        persons = RegPersonsOrgUnits.objects.filter(
            is_void=False, date_delinked__isnull=True).exclude(
            person__designation__isnull=True, person__designation='',
            person__designation__in=['CCGV', 'COVC'])
        check_fields = ['wdn_cadre_type_id', 'vol_cadre_type',
                        'sw_cadre_type_id', 'scc_cadre_type_id',
                        'po_cadre_type_id', 'pm_cadre_type_id',
                        'pa_cadre_type_id', 'cle_cadre_type_id',
                        'ogo_cadre_type_id', 'nct_cadre_type_id',
                        'mng_cadre_type_id', 'me_cadre_type_id',
                        'ict_cadre_type_id', 'hsm_cadre_type_id',
                        'hou_cadre_type_id', 'hos_cadre_type_id',
                        'dir_cadre_type_id', 'ddr_cadre_type_id',
                        'cc_cadre_type_id', 'cadre_type_id',
                        'adm_cadre_type_id']
        vals = get_dict(field_name=check_fields)
        county_id = int(county) if county else 0
        if org_unit:
            print('OU', org_unit)
            persons = persons.filter(org_unit_id=org_unit)
        # Get Geo Locations
        for pers in persons:
            if pers.org_unit_id not in ou_ids:
                ou_ids.append(pers.org_unit_id)
        ous = {}
        geos = RegOrgUnitGeography.objects.filter(
            is_void=False, org_unit_id__in=ou_ids, area_id__lt=338)
        for geo in geos:
            if county_id > 0:
                if county_id == int(geo.area.parent_area_id):
                    ous[geo.org_unit_id] = geo.area.parent_area_id
            else:
                ous[geo.org_unit_id] = geo.area.parent_area_id
        if county_id > 0:
            persons = persons.filter(org_unit_id__in=ous)
        for person in persons:
            fname = person.person.first_name
            sname = person.person.surname
            o_name = person.person.other_names
            oname = ' %s' % o_name if o_name else ''
            sex = 'Male' if person.person.sex_id == 'SMAL' else 'Female'
            did = person.person.designation
            ou_id = person.org_unit_id
            cid = ous[ou_id] if ou_id in ous else None
            ccd = str(cid).zfill(3) if cid else None
            cname = PARAMS[ccd] if cid else None
            des = vals[did] if did in vals else 'N/A'
            age = person.person.years
            dob = str(person.person.date_of_birth)
            dt = {"cpims_id": person.person_id}
            dt['age'] = 'N/A' if dob == '1900-01-01' else age
            dt['designation'] = des
            dt['sex'] = sex
            dt['dob'] = dob
            dt['county'] = cname if cname else 'N/A'
            dt['org_unit'] = person.org_unit.org_unit_name
            dt['names'] = '%s %s%s' % (fname, sname, oname)
            cases.append(dt)
        result = {"data": cases}
        return JsonResponse(result, content_type='application/json',
                            safe=False)
    except Exception as e:
        print('error - %s' % (e))
        raise e
    else:
        pass


@login_required(login_url='/')
def manage_bugs(request):
    """Main home method and view."""
    try:
        person_id = request.user.reg_person_id
        resp = report_bug(request)
        msg = resp['message']
        result = {"response_code": 0, "message": "Issue Successfully sent to %s" % (msg)}
        return JsonResponse(result, content_type='application/json',
                            safe=False)
    except Exception:
        result = {"response_code": 9, "message": "Error while reporting bug"}
        return JsonResponse(result, content_type='application/json',
                            safe=False)