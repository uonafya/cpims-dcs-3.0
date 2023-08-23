from django.utils import timezone
from cpovc_main.models import ListQuestions
from cpovc_main.functions import convert_date
from .parameters import SI_FORMS, SI_CODES

from .models import SIMain, SI_VacancyApp, SIEvents, SIForms

from cpovc_forms.models import OVCPlacement
from cpovc_registry.models import RegOrgUnit


class CaseObj(object):
    pass


def get_form(form_id):
    """Method to get form details."""
    try:
        form_data = {}
        form_name = SI_FORMS[form_id] if form_id in SI_FORMS else ''
        form_code = SI_CODES[form_id] if form_id in SI_CODES else ''
        form_data['form_name'] = form_name
        form_data['form_code'] = form_code
    except Exception:
        return {'form_name': 'SI Forms', 'form_code': ''}
    else:
        return form_data


def save_reg(request, case_id, event_date, org_type, person_id, oid=0):
    """Method to get Alt Care case."""
    try:
        # Org unit and user
        ou_id = request.session.get('ou_primary', None)
        org_unit_id = 1 if not ou_id else ou_id
        if oid:
            org_unit_id = oid
        user_id = request.user.id
        obj, created = SIMain.objects.update_or_create(
            person_id=person_id, is_void=False,
            defaults={'case_date': event_date, 'org_type': org_type,
                      'org_unit_id': org_unit_id, 'created_by_id': user_id,
                      'case_id': case_id
                      },
        )
    except Exception as e:
        print('Error saving care - %s' % str(e))
        return False
    else:
        return obj


def save_event(request, form_id, person_id, care_id, event_date):
    """Method to save Event."""
    try:
        user_id = request.user.id
        obj, created = SIEvents.objects.update_or_create(
            care_id=care_id, form_id=form_id, person_id=person_id,
            defaults={'event_date': event_date,
                      'created_by_id': user_id})
    except Exception as e:
        print('Error saving event %s' % (str(e)))
        return None
    else:
        return obj


def save_form(request, form_id, person_id, edit_id=1):
    """Method to save all forms"""
    try:
        fms = {}
        org_type = 'XXXX'
        user_id = request.user.id
        ev_date = request.POST.get('event_date')
        event_date = convert_date(ev_date) if ev_date else timezone.now()
        case_id = None
        print(form_id, person_id)
        si_obj = save_reg(request, case_id, event_date, org_type, person_id)
        questions = ListQuestions.objects.filter(
            form__form_guid=form_id, is_void=False)
        for fm in questions:
            fd = {'id': fm.question_code, 'label': fm.question_text,
                  'type_id': fm.answer_type_id,
                  'field_id': fm.answer_field_id,
                  'set_id': fm.answer_set_id,
                  'is_required': fm.question_required}
            fms[fm] = fd
        # Vacancy application has its own table the rest is vertical table
        #  and edit_id == 1
        if form_id == 'FMSI001F':
            judge_name = get_data(request, 'Q5_magistrate_name')
            held_at = get_data(request, 'Q7_child_held_at')
            holding_place = get_data(request, 'Q8_child_held_at_name')
            next_mention_date = get_data(request, 'Q6_next_mention_date', 3)
            req_officer = get_data(request, 'Q9_request_officer')
            designation = get_data(request, 'Q10_designation')
            scco = get_data(request, 'Q11_scco')
            obj, created = SI_VacancyApp.objects.update_or_create(
                person_id=person_id, application_status=False,
                defaults={'ref_no': get_data(request, 'Q1_ref_num'),
                          'date_of_application': event_date,
                          'crc_no': get_data(request, 'Q2_crc_num'),
                          'pnc_no': get_data(request, 'Q3_pnc_num'),
                          'court_number': get_data(request, 'Q4_court_num'),
                          'judge_name': judge_name,
                          'child_held_at': held_at,
                          'holding_place': holding_place,
                          'date_of_next_mention': next_mention_date,
                          'requesting_officer': req_officer,
                          'designation': designation,
                          'sub_county_children_officer': scco,
                          'created_by_id': user_id},
            )
        else:
            print('Save the form %s' % (form_id))
            care_id = si_obj.pk
            event_obj = save_event(
                request, form_id, person_id, care_id, event_date)
            event_id = event_obj.pk
            # Defaults
            itdl = None
            for fm in fms:
                qid = fms[fm]['id']
                qtype = fms[fm]['type_id']
                if qtype == 'FMRD':
                    q_values = request.POST.getlist(qid, None)
                elif qtype == 'FMTF' or qtype == 'FMTA':
                    q_value = request.POST.get(qid, None)
                    q_values = [q_value]
                else:
                    q_value = request.POST.get(qid, None)
                    q_values = [q_value]
                for q_val in q_values:
                    if q_val:
                        if qtype in ['FMTF', 'FMTA']:
                            q_val, itdl = qtype, q_val
                        obj, created = SIForms.objects.update_or_create(
                            event_id=event_id, question_id=qid,
                            item_value=q_val,
                            defaults={'item_detail': itdl})
            # Special case of Admission form
            if form_id == 'FMSI004F':
                print('OK')
                inst_name = get_data(request, 'Q2_admission_inst')
                adm_number = get_data(request, 'Q1_admission_num')
                adm_date = event_date
                adm_type = get_data(request, 'Q3_admission_type')
                adm_reason = get_data(request, 'Q4_admission_reason')
                holding_period = get_data(request, 'Q6_holding_days')
                has_committal = get_data(request, 'Q5_has_committal')
                ob_number = get_data(request, 'Q7_ob_number')
                court_order_num = get_data(request, 'Q8_court_order_num')
                co_date = get_data(request, 'Q9_court_order_date')
                court_order_date = convert_date(co_date) if co_date else None
                court_name = get_data(request, 'Q10_court_name')
                comm_period = get_data(request, 'Q12_committal_period')
                comm_period_units = get_data(
                    request, 'Q11_committal_period_units')
                crs_id = request.POST.get('case_record_id')
                obj, created = OVCPlacement.objects.update_or_create(
                    person_id=person_id, is_active=True,
                    defaults={'residential_institution_id': inst_name,
                              'residential_institution_name': inst_name,
                              'admission_number': adm_number,
                              'admission_date': adm_date,
                              'admission_type': adm_type,
                              'admission_reason': adm_reason,
                              'holding_period': holding_period,
                              'has_court_committal_order': has_committal,
                              'court_order_number': court_order_num,
                              'court_order_issue_date': court_order_date,
                              'committing_court': court_name,
                              'committing_period': comm_period,
                              'committing_period_units': comm_period_units,
                              'ob_number': ob_number,
                              'case_record_id': crs_id,
                              'created_by': user_id})
                # update institute type on Main Table
                si_reg_id = si_obj.pk
                org_unit_id = int(inst_name)
                org_unit = RegOrgUnit.objects.get(id=org_unit_id)
                org_type = org_unit.org_unit_type_id
                SIMain.objects.filter(
                    person_id=person_id, pk=si_reg_id).update(
                    org_unit_id=org_unit_id, org_type=org_type)

    except Exception as e:
        raise e
    else:
        pass


def get_data(request, f_id, f_type=1):
    """Method to get field data."""
    try:
        f_data = request.POST.get(f_id, None)
        if f_type == 3:
            f_data = convert_date(f_data) if f_data else None
        if not f_data:
            return None
    except Exception as e:
        print('Error - %s' % str(e))
        return None
    else:
        return f_data


def get_event_data(form_id, event_id):
    """Method to GET event data."""
    try:
        idata = {}
        if form_id == 'FMSI001F':
            datas = SI_VacancyApp.objects.filter(pk=event_id)
            for data in datas:
                ev_date = data.date_of_application
                event_date = ev_date.strftime('%d-%b-%Y')
                idata['Q1_ref_num'] = data.ref_no
                idata['event_date'] = event_date
                idata['Q2_crc_num'] = data.crc_no
                idata['Q3_pnc_num'] = data.pnc_no
                idata['Q4_court_num'] = data.court_number
                idata['Q5_magistrate_name'] = data.judge_name
                idata['Q7_child_held_at'] = data.child_held_at
                idata['Q8_child_held_at_name'] = data.holding_place
                idata['Q6_next_mention_date'] = data.date_of_next_mention
                idata['Q9_request_officer'] = data.requesting_officer
                idata['Q10_designation'] = data.designation
                idata['Q11_scco'] = data.sub_county_children_officer
        else:
            event = SIEvents.objects.get(pk=event_id)
            ev_date = event.event_date
            event_date = ev_date.strftime('%d-%b-%Y')
            datas = SIForms.objects.filter(event_id=event_id, is_void=False)
            for data in datas:
                qid = data.question_id
                qval = data.item_value
                qvals = data.item_detail
                q_elem = qvals if qval in ['FMTF', 'FMTA'] else qval
                idata[qid] = q_elem
            idata['event_date'] = event_date
    except Exception as e:
        print('Error getting idata %s' % str(e))
        return {}
    else:
        return idata


def delete_event_data(request, form_id, event_id):
    """Method to GET event data."""
    try:
        if form_id == 'FMSI001F':
            SI_VacancyApp.objects.filter(pk=event_id).delete()
        else:
            datas = SIEvents.objects.get(pk=event_id)
            datas.is_void = True
            datas.save(update_fields=["is_void"])
            # Hard delete the form elements
            SIForms.objects.filter(event_id=event_id).delete()
            # OVCPlacement.objects.filter(
            # person=person, pk=placement_id).update(is_active=False)
    except Exception as e:
        print('Error getting idata %s' % str(e))
        return 0
    else:
        return 1


def action_event_data(request, form_id, event_id):
    """Method to GET event data."""
    try:
        if form_id == 'FMSI001F':
            verdict = request.POST.get('verdict')
            status = True if verdict == 'AYES' else False
            a_date = timezone.now() if verdict else None
            si = SI_VacancyApp.objects.get(pk=event_id)
            si.application_status = status
            si.date_of_approved = a_date
            si.save(
                update_fields=["application_status", "date_of_approved"])
            print('Good')
        else:
            print('WIP')
    except Exception as e:
        print('Error getting idata %s' % str(e))
        return 0
    else:
        return 1
