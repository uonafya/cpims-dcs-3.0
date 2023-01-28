from datetime import datetime
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from cpovc_main.functions import get_dict
from cpovc_forms.models import OVCCaseCategory
from cpovc_forms.forms import OVCSearchForm
from cpovc_forms.functions import get_person_ids, get_case_info
from cpovc_registry.models import RegPersonsExternalIds
from .models import CTIPMain, CTIPEvents, CTIPForms
from .settings import FMS
from .forms import (
    CTIPFormA, CTIPFormB, CTIPFormC, CTIPFormD,
    CTIPFormE, CTIPFormF, CTIPFormG, CTIPForm)
from .functions import save_ctip_form, get_ctip, handle_ctip
from cpovc_forms.models import OVCCaseRecord
from cpovc_registry.models import RegPerson


@login_required
def ctip_home(request):
    '''
    Some default page for forms home page
    '''
    try:
        form = OVCSearchForm(data=request.GET)
        # form = SearchForm(data=request.POST)
        # person_type = 'TBVC'
        search_string = request.GET.get('search_name')
        pids = get_person_ids(request, search_string)

        ctip_ids, case_ids = {}, {}
        cases = RegPerson.objects.filter(is_void=False, id__in=pids)
        # Get case record sheet details
        crss = OVCCaseRecord.objects.filter(is_void=False, person_id__in=pids)
        for crs in crss:
            case_ids[crs.person_id] = {'clv': 1, 'cs': crs.case_serial,
                                       'cid': crs.case_id}
        # Check if there is a filled AFC Form
        ctips = CTIPMain.objects.filter(is_void=False, person_id__in=pids)
        for ctip in ctips:
            ctip_ids[ctip.person_id] = {'cid': ctip.case_id,
                                        'clv': 2, 'cdt': ctip.case_date}
        for case in cases:
            pid = case.id
            cid = ctip_ids[pid]['cid'] if pid in ctip_ids else 'N/A'
            cdt = ctip_ids[pid]['cdt'] if pid in ctip_ids else 'N/A'
            clvf = case_ids[pid]['clv'] if pid in case_ids else 0
            clv = ctip_ids[pid]['clv'] if pid in ctip_ids else clvf
            csn = case_ids[pid]['cs'] if pid in case_ids else 'N/A'
            ccid = case_ids[pid]['cid'] if pid in case_ids else 'N/A'
            setattr(case, 'case_t', str(cid))
            setattr(case, 'case_date', cdt)
            setattr(case, 'case_level', clv)
            setattr(case, 'case_id', cid)
            setattr(case, 'case_cid', str(ccid))
            setattr(case, 'case_serial', csn)
        return render(request, 'ctip/home.html',
                      {'status': 200, 'cases': cases, 'form': form})
    except Exception as e:
        raise e


@login_required
def view_ctip_case(request, case_id):
    '''
    View CTiP main page
    '''
    try:
        # form = OVCSearchForm(initial={'person_type': 'TBVC'})
        check_fields = ['sex_id', 'case_category_id']
        vals = get_dict(field_name=check_fields)
        case = CTIPMain.objects.get(is_void=False, case_id=case_id)
        # Case Categories
        categories = OVCCaseCategory.objects.filter(case_id_id=case_id)
        events = (CTIPEvents.objects
                  .filter(case_id=case_id)
                  .values('form_id')
                  .annotate(dcount=Count('form_id'))
                  .order_by()
                  )
        # Handle Form C - Multiple forms
        reffs = CTIPEvents.objects.filter(case_id=case_id, form_id='C')
        # print('events', events)
        ev_id = str(case.case.case_id).replace('-', '')
        forms = {}
        for event in events:
            forms[str(event['form_id'])] = event['dcount']
        print('forms', forms)
        return render(request, 'ctip/view_case.html',
                      {'status': 200, 'case': case, 'vals': vals,
                       'categories': categories, 'events': forms,
                       'ev_id': ev_id, 'reffs': reffs})
    except Exception as e:
        raise e


@login_required
def new_ctip_case(request, case_id):
    '''
    View CTiP main page
    '''
    try:
        # form = OVCSearchForm(initial={'person_type': 'TBVC'})
        check_fields = ['sex_id', 'case_category_id']
        vals = get_dict(field_name=check_fields)
        ctip = get_ctip(request, case_id)
        # Case Categories
        case = OVCCaseRecord.objects.get(case_id=case_id)
        categories = OVCCaseCategory.objects.filter(case_id_id=case_id)
        events = (CTIPEvents.objects
                  .filter(case_id=case_id)
                  .values('form_id')
                  .annotate(dcount=Count('form_id'))
                  .order_by()
                  )
        print('events', events)
        if request.method == 'POST':
            ctip_params = {}
            person_id = case.person_id
            case_date = case.date_case_opened
            ctip_params['case_id'] = case_id
            ctip_params['person_id'] = person_id
            ctip_params['case_date'] = case_date
            handle_ctip(request, 0, ctip_params)
            url = reverse(view_ctip_case, kwargs={'case_id': case_id})
            msg = 'CTiP Case details saved successfully'
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(url)
        ev_id = ''
        if ctip:
            ev_id = str(case.case_id).replace('-', '')
        forms = {}
        tr_initial_info = {}
        case_infos = get_case_info(request, case_id)
        activities, means, purposes = [], [], []
        for cinfo in case_infos:
            info_type = cinfo.info_type
            if info_type == 'TACT':
                activities.append(str(cinfo.info_item))
            elif info_type == 'TMNS':
                means.append(str(cinfo.info_item))
            elif info_type == 'TPPS':
                purposes.append(str(cinfo.info_item))
        # Check if in CTiP DB
        ctip_case = get_ctip(request, case_id)
        is_traffick = 'AYES' if ctip_case else 'ANNO'
        tr_initial_info['ctip_activity'] = activities
        tr_initial_info['ctip_means'] = means
        tr_initial_info['ctip_purpose'] = purposes
        tr_initial_info['is_trafficking'] = is_traffick
        tr_form = CTIPForm(initial=tr_initial_info)
        for event in events:
            forms[str(event['form_id'])] = event['dcount']
        print('forms', forms)
        return render(request, 'ctip/new_case.html',
                      {'status': 200, 'case_id': case_id, 'vals': vals,
                       'categories': categories, 'events': forms,
                       'ev_id': ev_id, 'case': case, 'tr_form': tr_form})
    except Exception as e:
        raise e


@login_required
def edit_ctip_case(request, case_id):
    '''
    View CTiP main page
    '''
    try:
        # form = OVCSearchForm(initial={'person_type': 'TBVC'})
        check_fields = ['sex_id', 'case_category_id']
        vals = get_dict(field_name=check_fields)
        ctip = get_ctip(request, case_id)
        # Case Categories
        case = OVCCaseRecord.objects.get(case_id=case_id)
        categories = OVCCaseCategory.objects.filter(case_id_id=case_id)
        events = (CTIPEvents.objects
                  .filter(case_id=case_id)
                  .values('form_id')
                  .annotate(dcount=Count('form_id'))
                  .order_by()
                  )
        print('events', events)
        if request.method == 'POST':
            ctip_params = {}
            person_id = case.person_id
            case_date = case.date_case_opened
            ctip_params['case_id'] = case_id
            ctip_params['person_id'] = person_id
            ctip_params['case_date'] = case_date
            handle_ctip(request, 0, ctip_params)
            url = reverse(view_ctip_case, kwargs={'case_id': case_id})
            msg = 'CTiP Case details updated successfully'
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(url)
        ev_id = ''
        if ctip:
            ev_id = str(case.case_id).replace('-', '')
        forms = {}
        tr_initial_info = {}
        case_infos = get_case_info(request, case_id)
        activities, means, purposes = [], [], []
        for cinfo in case_infos:
            info_type = cinfo.info_type
            if info_type == 'TACT':
                activities.append(str(cinfo.info_item))
            elif info_type == 'TMNS':
                means.append(str(cinfo.info_item))
            elif info_type == 'TPPS':
                purposes.append(str(cinfo.info_item))
        # Check if in CTiP DB
        ctip_case = get_ctip(request, case_id)
        is_traffick = 'AYES' if ctip_case else 'ANNO'
        tr_initial_info['ctip_activity'] = activities
        tr_initial_info['ctip_means'] = means
        tr_initial_info['ctip_purpose'] = purposes
        tr_initial_info['is_trafficking'] = is_traffick
        tr_form = CTIPForm(initial=tr_initial_info)
        for event in events:
            forms[str(event['form_id'])] = event['dcount']
        print('forms', forms)
        return render(request, 'ctip/edit_case.html',
                      {'status': 200, 'case_id': case_id, 'vals': vals,
                       'categories': categories, 'events': forms,
                       'ev_id': ev_id, 'case': case, 'tr_form': tr_form})
    except Exception as e:
        raise e


@login_required
def view_ctip_form(request, form_id, case_id):
    '''
    Some default page for CTiP forms home page
    '''
    try:
        check_fields = ['sex_id', 'case_category_id']
        vals = get_dict(field_name=check_fields)
        form_name = FMS[form_id] if form_id in FMS else 'Default'
        case = CTIPMain.objects.get(is_void=False, case_id=case_id)
        person_id = case.person.id
        contacts = RegPersonsExternalIds.objects.filter(person_id=person_id)
        # Check events
        idata = {}
        events = CTIPEvents.objects.filter(
            case_id=case_id, form_id=form_id)
        print('Event', form_id, case_id, events)
        if events:
            edate = events[0].event_date
            event_date = edate.strftime('%d-%b-%Y')
            idata['event_date'] = event_date
            event_id = events[0].pk
            fdatas = CTIPForms.objects.filter(event_id=event_id)
            for fdata in fdatas:
                qid = fdata.question_id
                q_item = fdata.item_value
                q_detail = fdata.item_detail
                if qid.endswith('_txt'):
                    idata[qid] = q_detail
                elif qid.endswith('_rdo'):
                    idata[qid] = q_item
                else:
                    if qid not in idata:
                        idata[qid] = []
                    idata[qid].append(q_item)
            print('idata', idata)
        form = get_form(form_id, idata)
        if request.method == 'POST':
            form.data = request.POST
            res = save_ctip_form(request, form_id)
            if res:
                url = reverse(view_ctip_case, kwargs={'case_id': case_id})
            else:
                url = reverse(view_ctip_form, kwargs={'form_id': form_id,
                                                      'case_id': case_id})
            msg = 'Form - %s saved successfully' % (form_id)
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(url)
        tmpl = 'ctip/view_form_%s.html' % (form_id)
        cid = str(case_id).replace('-', '')
        mydate = datetime.now()
        dtm = mydate.strftime("%d-%b-%Y (%I:%M:%S %p)")
        return render(request, tmpl,
                      {'status': 200, 'case': case, 'form_id': form_id,
                       'form_name': form_name, 'vals': vals,
                       'form': form, 'case_id': cid, 'events': events,
                       'contacts': contacts, 'datetime': dtm})
    except Exception as e:
        raise e


@login_required
def ctip_form(request, form_id, case_id, ev_id=0):
    '''
    Some default page for CTiP forms home page
    '''
    try:
        check_fields = ['sex_id', 'case_category_id']
        vals = get_dict(field_name=check_fields)
        form_name = FMS[form_id] if form_id in FMS else 'Default'
        case = CTIPMain.objects.get(is_void=False, case_id=case_id)
        person_id = case.person.id
        contacts = RegPersonsExternalIds.objects.filter(person_id=person_id)
        # Forms and initial data
        has_consent = 'AYES' if case.has_consent else 'ANNO'
        cdate = case.consent_date
        if cdate:
            consent_date = cdate.strftime('%d-%b-%Y')
        else:
            consent_date = None
        if form_id == 'A':
            form = CTIPFormA(
                initial={'consent_date': consent_date,
                         'has_consent': has_consent})
        else:
            # Check events
            idata = {}
            events = CTIPEvents.objects.filter(
                case_id=case_id, form_id=form_id)
            print('Event', form_id, case_id, events)
            if form_id == 'C':
                events = events.filter(event_count=ev_id)
            if events:
                edate = events[0].event_date
                event_date = edate.strftime('%d-%b-%Y')
                idata['event_date'] = event_date
                event_id = events[0].pk
                fdatas = CTIPForms.objects.filter(event_id=event_id)
                for fdata in fdatas:
                    qid = fdata.question_id
                    q_item = fdata.item_value
                    q_detail = fdata.item_detail
                    if qid.endswith('_txt'):
                        idata[qid] = q_detail
                    elif qid.endswith('_rdo'):
                        idata[qid] = q_item
                    else:
                        if qid not in idata:
                            idata[qid] = []
                        idata[qid].append(q_item)
                print('idata', idata)
            form = get_form(form_id, idata)
        if request.method == 'POST':
            form.data = request.POST
            res = save_ctip_form(request, form_id, ev_id)
            if res:
                url = reverse(view_ctip_case, kwargs={'case_id': case_id})
            else:
                url = reverse(view_ctip_form, kwargs={'form_id': form_id,
                                                      'case_id': case_id})
            msg = 'Form - %s saved successfully' % (form_id)
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(url)
        tmpl = 'ctip/new_form_%s.html' % (form_id)
        cid = str(case_id).replace('-', '')
        return render(request, tmpl,
                      {'status': 200, 'case': case, 'form_id': form_id,
                       'form_name': form_name, 'vals': vals,
                       'form': form, 'case_id': cid, 'contacts': contacts})
    except Exception as e:
        raise e


@login_required
def ctip_forms(request, form_id, case_id, id):
    return ctip_form(request, form_id, case_id, id)


def get_form(form_id, idata):
    """Method to get form."""
    try:
        if form_id == 'B':
            form = CTIPFormB(initial=idata)
        elif form_id == 'C':
            form = CTIPFormC(initial=idata)
        elif form_id == 'D':
            form = CTIPFormD(initial=idata)
        elif form_id == 'E':
            form = CTIPFormE(initial=idata)
        elif form_id == 'F':
            form = CTIPFormF(initial=idata)
        else:
            form = CTIPFormG(initial=idata)
    except Exception as e:
        raise e
    else:
        return form
