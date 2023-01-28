from django.shortcuts import get_object_or_404
from cpovc_main.functions import convert_date
from .models import CTIPMain, CTIPEvents, CTIPForms
from cpovc_forms.functions import save_case_info
from cpovc_forms.models import OvcCaseInformation


def handle_ctip(request, action, params={}):
    """Method to handle CTiP"""
    try:
        if action == 0:
            tr_case = request.POST.get('is_trafficking')
            if tr_case == 'AYES':
                save_case(request, params)
            else:
                # This is to handle edits / deletion
                case_id = params['case_id']
                case = get_object_or_404(CTIPMain, case_id=case_id)
                if case:
                    # Void this record and delete case_info data
                    case.is_void = True
                    case.save(update_fields=["is_void"])
                    case_info = OvcCaseInformation.objects.filter(
                        case_id=case_id)
                    case_info.delete()
    except Exception as e:
        print('Error saving TIP Action %s' % (str(e)))
    else:
        return True


def get_ctip(request, case_id):
    """Method to get ctip case."""
    try:
        case = CTIPMain.objects.get(case_id=case_id, is_void=False)
    except Exception:
        return False
    else:
        return case


def save_case(request, params):
    """Method to save Main case data."""
    try:
        case_id = params['case_id']
        person_id = params['person_id']
        case_date = params['case_date']
        obj, created = CTIPMain.objects.update_or_create(
            case_id=case_id,
            defaults={'case_date': case_date,
                      'person_id': person_id, 'is_void': False},
        )
        # Save the activity, means and purpose
        activity_list = request.POST.getlist('ctip_activity')
        means_list = request.POST.getlist('ctip_means')
        purpose_list = request.POST.getlist('ctip_purpose')
        case = obj.case
        print('case', case)
        print('Activity', activity_list)
        for activity in activity_list:
            save_case_info(request, case, 'TACT', activity, '')
        for means in means_list:
            save_case_info(request, case, 'TMNS', means, '')
        for purpose in purpose_list:
            save_case_info(request, case, 'TPPS', purpose, '')
    except Exception as e:
        print('Error saving TIP %s' % (str(e)))
    else:
        return True


def save_ctip_form(request, form_id, ev_id=0):
    """Method to save forms."""
    try:
        response = True
        case_id = request.POST.get('case_id')
        person_id = request.POST.get('person_id')
        event_date = request.POST.get('event_date')
        lid = get_last_form(request, form_id)
        print('Last ID', lid)
        if form_id == 'A':
            consent_date = request.POST.get('consent_date')
            has_consent = request.POST.get('has_consent')
            case = get_object_or_404(
                CTIPMain, case_id=case_id, is_void=False)
            case.has_consent = True if has_consent == 'AYES' else False
            case.consent_date = convert_date(consent_date)
            case.save(update_fields=["consent_date", "has_consent"])
        elif form_id == 'C':
            nev_id = lid + 1 if ev_id == 0 else ev_id
            obj, created = CTIPEvents.objects.update_or_create(
                case_id=case_id, form_id=form_id, event_count=nev_id,
                defaults={'event_date': convert_date(event_date),
                          'person_id': person_id})
            event_id = obj.pk
            save_form_data(request, form_id, event_id)
        else:
            obj, created = CTIPEvents.objects.update_or_create(
                case_id=case_id, form_id=form_id,
                defaults={'event_date': convert_date(event_date),
                          'person_id': person_id})
            event_id = obj.pk
            save_form_data(request, form_id, event_id)
        pref = 'qf%s' % (form_id)
        extract_params(request, pref)
    except Exception as e:
        print('Error saving form - %s' % (str(e)))
        return False
    else:
        return response


def get_last_form(request, form_id):
    """Method to get the last form."""
    try:
        last_form = CTIPEvents.objects.filter(
            form_id=form_id).latest('event_count').event_count
    except Exception as e:
        print('Error querying last form ID - %s' % (str(e)))
        return 0
    else:
        return last_form


def save_form_data(request, form_id, event_id):
    """Method to save Main forms data."""
    try:
        print('event id', event_id)
        form_pref = 'qf%s' % (form_id)
        all_itms = extract_params(request, form_pref)
        for itms in all_itms:
            for itm in all_itms[itms]:
                print('itm', itms, itm)
                itdm = 'QTXT' if itms.endswith('_txt') else itm
                itdl = itm if itms.endswith('_txt') else None
                print('itm after', itms, itm, itdl)
                obj, created = CTIPForms.objects.update_or_create(
                    event_id=event_id, question_id=itms,
                    item_value=itdm,
                    defaults={'item_value': itdm, 'item_detail': itdl},
                )
    except Exception as e:
        print('Error saving TIP %s' % (str(e)))
    else:
        return True


def extract_params(request, pref):
    """Method to extract charges items."""
    try:
        params, itms = {}, []
        for itm in request.POST:
            if itm.startswith(pref):
                itms.append(itm.replace(pref, ''))
        # print('items', itms)

        for dt in itms:
            itm_id = '%s%s' % (pref, dt)
            itm_value = request.POST.getlist(itm_id)
            if itm_value[0]:
                params[itm_id] = itm_value
        print(params)
    except Exception as e:
        print('Error getting charges - %s' % (e))
        return []
    else:
        return params
