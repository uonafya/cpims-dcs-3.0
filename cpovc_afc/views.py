from django.utils import timezone
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from cpovc_forms.forms import OVCSearchForm
from cpovc_forms.functions import get_person_ids
from .models import AFCMain, AFCEvents, AFCForms
from .forms import (
    AltCareForm, AFCForm1A, AFCForm1B, AFCForm2A, AFCForm4A, AFCForm5A,
    AFCForm6A, AFCForm7A, AFCForm8A, AFCForm9A, AFCForm10A,
    AFCForm12A, AFCForm14A, AFCForm15A, AFCForm16A)
from cpovc_registry.models import (
    RegPerson, RegPersonsSiblings, RegPersonsExternalIds, RegPersonsGeo)
from cpovc_forms.models import OVCCaseRecord, OVCCaseCategory
from cpovc_main.functions import get_dict
from .functions import (
    handle_alt_care, save_altcare_form, get_area, get_class_levels,
    get_education, get_form_info, get_crs, get_alt_care,
    get_last_form)
from .settings import FMS, CTS

# from cpovc_ovc.decorators import validate_ovc


@login_required
def alt_care_home(request):
    '''
    Some default page for forms home page
    '''
    try:
        form = OVCSearchForm(data=request.GET)
        # form = SearchForm(data=request.POST)
        # person_type = 'TBVC'
        afc_ids, case_ids = {}, {}
        search_string = request.GET.get('search_name')
        pids = get_person_ids(request, search_string)
        cases = RegPerson.objects.filter(is_void=False, id__in=pids)
        # Get case record sheet details
        crss = OVCCaseRecord.objects.filter(is_void=False, person_id__in=pids)
        for crs in crss:
            case_ids[crs.person_id] = {'clv': 1, 'cid': crs.case_id}
        # Check if there is a filled AFC Form
        afcs = AFCMain.objects.filter(is_void=False, person_id__in=pids)
        for afc in afcs:
            afc_ids[afc.person_id] = {'cid': afc.care_id,
                                      'clv': 2, 'cdt': afc.case_date}
        for case in cases:
            pid = case.id
            cid = afc_ids[pid]['cid'] if pid in afc_ids else 'N/A'
            cdt = afc_ids[pid]['cdt'] if pid in afc_ids else 'N/A'
            clvf = case_ids[pid]['clv'] if pid in case_ids else 0
            crs_id = case_ids[pid]['cid'] if pid in case_ids else None
            clv = afc_ids[pid]['clv'] if pid in afc_ids else clvf
            setattr(case, 'case_t', str(cid))
            setattr(case, 'care_id', cid)
            setattr(case, 'case_date', cdt)
            setattr(case, 'case_level', clv)
            setattr(case, 'case_id', crs_id)
        return render(request, 'afc/home.html',
                      {'status': 200, 'cases': cases, 'form': form})
    except Exception as e:
        raise e


@login_required
def new_alternative_care(request, case_id):
    '''
    New Alternative Care main page
    '''
    try:
        cid = 'XX'
        form = AltCareForm(initial={'person_type': 'TBVC'})
        check_fields = ['sex_id', 'case_category_id']
        vals = get_dict(field_name=check_fields)
        # Case Categories
        case = OVCCaseRecord.objects.get(case_id=case_id)
        categories = OVCCaseCategory.objects.filter(case_id_id=case_id)
        care = AFCMain.objects.filter(
            is_void=False, case_id=case_id, case_status__isnull=True)
        if care:
            my_care = care.first()
            care_id = my_care.care_id
            msg = 'Child already enrolled to Alternative care '
            msg += 'and case management is ongoing.'
            messages.add_message(request, messages.ERROR, msg)
            cid = str(my_care.care_type)[2:]
            url = reverse(view_alternative_care, kwargs={'care_id': care_id})
            return HttpResponseRedirect(url)

        if request.method == 'POST':
            afc_params = {}
            person_id = case.person_id
            afc_params['case_id'] = case_id
            afc_params['person_id'] = person_id
            afc_params['case_cid'] = cid
            care_id = handle_alt_care(request, 0, afc_params)
            url = reverse(view_alternative_care, kwargs={'care_id': care_id})
            msg = 'Alternative Care details saved successfully'
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(url)
        return render(request, 'afc/new_alternative_care.html',
                      {'status': 200, 'case_id': case_id, 'vals': vals,
                       'categories': categories, 'case': case,
                       'form': form, 'care': care, 'nid': case_id,
                       'cid': cid})
    except Exception as e:
        raise e


@login_required
def view_alternative_care(request, care_id):
    '''
    View Alternative Care main page
    '''
    try:
        case = AFCMain.objects.get(is_void=False, care_id=care_id)
        if case.care_type:
            cid = str(case.care_type)[2:]
        else:
            cid = 'XX'
        cname = CTS[cid] if cid in CTS else 'Missing Assessments'
        check_fields = ['sex_id', 'case_category_id',
                        'alternative_family_care_type_id',
                        'care_admission_reason_id']
        vals = get_dict(field_name=check_fields)
        # Events
        events = (AFCEvents.objects
                  .filter(care_id=care_id)
                  .values('form_id')
                  .annotate(dcount=Count('form_id'))
                  .order_by()
                  )
        # Common data
        fdatas = get_form_info(request, case.pk, case.person_id, False)
        forms, fforms, iforms = {}, [], ['1A', '1B', '2A']
        for event in events:
            forms[str(event['form_id'])] = event['dcount']
            fforms.append(str(event['form_id']))
        print('forms', forms)
        step_one = all(elem in fforms for elem in iforms)
        return render(request, 'afc/view_alternative_care.html',
                      {'status': 200, 'case': case, 'vals': vals,
                       'cid': cid, 'care_name': cname, 'events': forms,
                       'fdatas': fdatas, 'step_one': step_one})
    except Exception as e:
        raise e


@login_required
def edit_alternative_care(request, care_id):
    '''
    Edit Alternative Care main page
    '''
    try:
        case = AFCMain.objects.get(is_void=False, care_id=care_id)
        if case.care_type:
            cid = str(case.care_type)[2:]
        else:
            cid = 'XX'
        case_id = case.case_id
        if request.method == 'POST':
            afc_params = {}
            person_id = case.person_id
            afc_params['care_id'] = care_id
            afc_params['case_id'] = case_id
            afc_params['person_id'] = person_id
            handle_alt_care(request, 0, afc_params)
            url = reverse(view_alternative_care, kwargs={'care_id': care_id})
            msg = 'Alternative Care details updated successfully'
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(url)
        initial_info = {}
        cdate = case.case_date
        case_date = cdate.strftime('%d-%b-%Y')
        initial_info['care_option'] = case.care_type
        initial_info['care_sub_option'] = case.care_sub_type
        initial_info['case_date'] = case_date
        # Get common elements
        fdatas = get_form_info(request, case.pk, case.person_id, False)
        # Events
        events = (AFCEvents.objects
                  .filter(care_id=care_id)
                  .values('form_id')
                  .annotate(dcount=Count('form_id'))
                  .order_by()
                  )
        forms, fforms, iforms = {}, [], ['1A', '1B', '2A']
        for event in events:
            forms[str(event['form_id'])] = event['dcount']
            fforms.append(str(event['form_id']))
        print('forms', forms)
        step_one = all(elem in fforms for elem in iforms)
        if fdatas:
            for fdt in fdatas:
                initial_info[fdt] = fdatas[fdt]
        form = AltCareForm(initial=initial_info)
        cname = CTS[cid] if cid in CTS else 'Missing Assessments'
        check_fields = ['sex_id', 'case_category_id',
                        'alternative_family_care_type_id']
        vals = get_dict(field_name=check_fields)
        categories = OVCCaseCategory.objects.filter(case_id_id=case_id)
        return render(request, 'afc/edit_alternative_care.html',
                      {'status': 200, 'case': case, 'vals': vals,
                       'cid': cid, 'care_name': cname,
                       'form': form, 'categories': categories,
                       'step_one': step_one})
    except Exception as e:
        raise e


@login_required
def alt_care_form(request, cid, form_id, care_id, ev_id=0):
    '''
    Some default page for CTiP forms home page
    '''
    try:
        check_fields = ['sex_id', 'case_category_id', 'religion_type_id',
                        'alternative_family_care_type_id',
                        'family_type_id']
        vals = get_dict(field_name=check_fields)
        # Handle saved items - Multiple instance forms
        all_events = AFCEvents.objects.filter(
            care_id=care_id, form_id=form_id)
        if form_id in ['6A', '2A']:
            events = all_events.filter(event_count=ev_id)
        else:
            events = all_events
        # print('Event', form_id, case_id, events)
        for ev in events:
            print('ev', ev, ev.event_count)
        idata = {}
        if events:
            edate = events[0].event_date
            event_date = edate.strftime('%d-%b-%Y')
            idata['event_date'] = event_date
            event_id = events[0].pk
            ev_id = events[0].event_count
            fdatas = AFCForms.objects.filter(event_id=event_id)
            for fdata in fdatas:
                qid = fdata.question_id
                q_item = fdata.item_value
                q_detail = fdata.item_detail
                if qid.endswith('_msc'):
                    if qid not in idata:
                        idata[qid] = []
                    idata[qid].append(q_item)
                elif qid.endswith('_rdo') or qid.endswith('_sdd'):
                    idata[qid] = q_item
                else:
                    idata[qid] = q_detail
            print('idata', idata)
        form_name = FMS[form_id] if form_id in FMS else 'Default'
        my_care = get_alt_care(request, care_id, 1)
        if my_care:
            case = AFCMain.objects.get(is_void=False, care_id=care_id)
            person_id = case.person_id
            case_id = case.case_id
            case_num = case.case_number
        else:
            case_id = care_id
            case = get_crs(request, case_id)
            person_id = case.person_id
            case_id = care_id
            case_num = '0'
            setattr(case, 'care_id', care_id)
        afcs = AFCMain.objects.filter(person_id=person_id)
        # Get education
        sch_class = ''
        ed = get_education(person_id)
        if ed:
            sch_class = ed.school_class
            idata['school_level'] = ed.school_level
            idata['school'] = ed.school_id
            idata['school_name'] = ed.school.school_name
            idata['school_class'] = sch_class
            idata['admission_type'] = ed.admission_type
        # Get persons registry info
        geos = {}
        geo_locs = RegPersonsGeo.objects.filter(
            person_id=person_id, is_void=False)
        for geo in geo_locs:
            geos[geo.area.area_type_id] = geo.area.area_name
            if geo.area.area_type_id == 'GDIS':
                a_id = geo.area.parent_area_id
                a_name = get_area(a_id)
                geos['GPRV'] = a_name
        # Class levels
        levels = get_class_levels()
        siblings = RegPersonsSiblings.objects.select_related().filter(
            child_person=person_id, is_void=False, date_delinked=None)
        extids = RegPersonsExternalIds.objects.filter(
            person_id=person_id, is_void=False)
        ext_ids = {}
        for extid in extids:
            ext_ids[str(extid.identifier_type_id)] = extid.identifier
        # Save submitted records
        if request.method == 'POST':
            res = save_altcare_form(request, form_id, ev_id)
            if res:
                care_id = res
                msg = 'Form - %s saved successfully' % (form_id)
                messages.add_message(request, messages.INFO, msg)
                url = reverse(
                    view_alternative_care, kwargs={'care_id': care_id})
            else:
                msg = 'Error while saving Form - %s. Try again' % (form_id)
                messages.add_message(request, messages.ERROR, msg)
                url = reverse(
                    new_alternative_care, kwargs={'case_id': case_id})
            return HttpResponseRedirect(url)
        print('idata', idata, case)
        form = get_form(form_id, idata, cid)
        tmpl = 'afc/new_form_%s.html' % (form_id)
        case_uid = str(case_id).replace('-', '')
        case_num = '%s/%s' % (str(case_num).zfill(6), 2022)
        return render(request, tmpl,
                      {'status': 200, 'case': case, 'form_id': form_id,
                       'form_name': form_name, 'vals': vals, 'geos': geos,
                       'form': form, 'case_id': case_uid, 'cid': cid,
                       'siblings': siblings, 'ext_ids': ext_ids,
                       'levels': levels, 'sch_class': sch_class,
                       'case_num': case_num, 'afcs': afcs,
                       'events': all_events, 'care': my_care})
    except Exception as e:
        raise e


def get_form(form_id, initial_data, cid):
    """ Get the forms by ids."""
    try:
        form = AltCareForm(initial=initial_data)
        if form_id == '1A':
            form = AFCForm1A(initial=initial_data)
        elif form_id == '1B':
            form = AFCForm1B(initial=initial_data)
        elif form_id == '2A':
            form = AFCForm2A(initial=initial_data)
        elif form_id == '4A':
            form = AFCForm4A(initial=initial_data)
        elif form_id == '5A':
            form = AFCForm5A(cid, initial=initial_data)
        elif form_id == '6A':
            form = AFCForm6A(initial=initial_data)
        elif form_id == '7A':
            form = AFCForm7A(initial=initial_data)
        elif form_id == '8A':
            form = AFCForm8A(initial=initial_data)
        elif form_id == '9A':
            form = AFCForm9A(initial=initial_data)
        elif form_id == '10A':
            form = AFCForm10A(initial=initial_data)
        elif form_id == '12A':
            form = AFCForm12A(initial=initial_data)
        elif form_id == '14A':
            form = AFCForm14A(initial=initial_data)
        elif form_id == '15A':
            form = AFCForm15A(initial=initial_data)
        elif form_id == '16A':
            form = AFCForm16A(initial=initial_data)
    except Exception as e:
        print('error getting form - %s' % (str(e)))
        raise e
    else:
        return form


@login_required
def edit_alt_care_form(request, cid, form_id, care_id, ev_id=0):
    """Metthod for edit."""
    try:
        return alt_care_form(request, cid, form_id, care_id, ev_id)
    except Exception as e:
        raise e


@login_required
def delete_alt_care_form(request, form_id, event_id):
    """Metthod for edit."""
    try:
        event = AFCEvents.objects.get(event_id=event_id, form_id=form_id)
        start_date = event.timestamp_created
        today = timezone.now()
        diff_days = today - start_date
        if diff_days.days > 90:
            msg = "Can not delete record after 90 days."
        else:
            msg = "Entry deleted successfully"
            event.delete()
        messages.add_message(request, messages.INFO, msg)
        results = {"message": msg}
        return JsonResponse(results, content_type='application/json',
                            safe=False)
    except Exception as e:
        print('Error deleting form - %s' % (e))
        raise e
