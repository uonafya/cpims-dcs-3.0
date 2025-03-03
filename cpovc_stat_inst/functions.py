import json
import uuid
from django.utils import timezone
from cpovc_main.models import ListQuestions
from cpovc_main.functions import convert_date, get_days_difference
from .parameters import SI_FORMS, SI_CODES

from .models import (
    SIMain, SI_VacancyApp, SIEvents, SIForms, SI_Document)

from cpovc_forms.models import OVCPlacement
from cpovc_registry.models import RegOrgUnit

from django.conf import settings
MEDIA_ROOT = settings.MEDIA_ROOT


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


def save_event(request, form_id, person_id, care_id, event_date, rev=None):
    """Method to save Event."""
    try:
        user_id = request.user.id
        defaults = {'event_date': event_date, 'created_by_id': user_id}
        # Handle Child Events
        if rev:
            defaults['related_to_id'] = rev
        obj, created = SIEvents.objects.update_or_create(
            care_id=care_id, form_id=form_id, related_to_id=rev,
            person_id=person_id, is_void=False,
            defaults=defaults)
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
        all_answers = request.POST.get('all_answers', '{}')
        si_datas = json.loads(all_answers)
        print('JSONS', si_datas)
        event_date = convert_date(ev_date) if ev_date else timezone.now()
        case_id = request.POST.get('case_id', None)
        print('Final Check', form_id, person_id, case_id)
        if form_id == 'FMSI005F':
            case_id = request.POST.get('case_record_id')
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
        care_id = si_obj.pk
        event_obj = save_event(
            request, form_id, person_id, care_id, event_date)
        event_id = event_obj.pk
        print('Save the form %s' % (form_id))
        # Save jsons
        if si_datas:
            save_jsons(request, form_id, person_id, care_id,
                       event_id, event_date, si_datas)
        # Defaults
        itdl = None
        qdels = {}
        for fm in fms:
            qid = fms[fm]['id']
            qtype = fms[fm]['type_id']
            q_values = []
            if qtype == 'FMCB':
                q_values = request.POST.getlist(qid, None)
                qdels[qid] = q_values
            elif qtype == 'FMTF' or qtype == 'FMTA':
                q_value = request.POST.get(qid, None)
                q_values = [q_value]
            elif qtype == 'FMFL':
                print('Handle File upload', request.FILES)
                if request.FILES:
                    u_file = request.FILES["Q12B_document_file"]
                    f_name = handle_uploads(
                        request, u_file, form_id, person_id)
                    q_value = f_name
                    q_values = [q_value]
            else:
                q_value = request.POST.get(qid, None)
                q_values = [q_value]
            for q_val in q_values:
                if q_val:
                    if qtype in ['FMTF', 'FMTA', 'FMFL']:
                        q_val, itdl = qtype, q_val
                    obj, created = SIForms.objects.update_or_create(
                        event_id=event_id, question_id=qid,
                        item_value=q_val,
                        defaults={'item_detail': itdl})
            # Handle delete for checkboxes
            for qid in qdels:
                qitms = qdels[qid]
                SIForms.objects.filter(
                    event_id=event_id, question_id=qid).exclude(
                    item_value__in=qitms).delete()
        # Special case of Vacancy application
        if form_id == 'FMSI001F':
            judge_name = get_data(request, 'Q5_magistrate_name')
            held_at = get_data(request, 'Q7_child_held_at')
            holding_place = get_data(request, 'Q8_child_held_at_name')
            next_mention_date = get_data(request, 'Q6_next_mention_date', 3)
            req_officer = get_data(request, 'Q9_request_officer')
            designation = get_data(request, 'Q10_designation')
            scco = get_data(request, 'Q11_scco')
            court = get_data(request, 'Q4B_court_station')
            obj, created = SI_VacancyApp.objects.update_or_create(
                person_id=person_id, case_id=case_id,
                defaults={'ref_no': get_data(request, 'Q1_ref_num'),
                          'date_of_application': event_date,
                          'crc_no': get_data(request, 'Q2_crc_num'),
                          'pnc_no': get_data(request, 'Q3_pnc_num'),
                          'court_number': get_data(request, 'Q4_court_num'),
                          'magistrate_court': court,
                          'judge_name': judge_name,
                          'child_held_at': held_at,
                          'holding_place': holding_place,
                          'date_of_next_mention': next_mention_date,
                          'requesting_officer': req_officer,
                          'designation': designation,
                          'sub_county_children_officer': scco,
                          'created_by_id': user_id,
                          'event_id': event_id},
            )
        # Special care for approval
        if form_id == 'FMSI033R':
            print('Handle approvals')
            print(request.POST)
            todate = timezone.now()
            d_fields = ["date_of_approved", "approved_by_id", "comment",
                        "application_status"]
            ev_id = request.POST.get('event_id')
            comment = request.POST.get('Q4_comment')
            status_id = request.POST.get('Q1_status')
            institution_id = request.POST.get('Q2_institution')
            months = request.POST.get('Q3_months')
            status = False if status_id == 'RVAR' else True
            ev = SI_VacancyApp.objects.get(pk=ev_id)
            ev.date_of_approved = todate
            ev.approved_by_id = user_id
            ev.comment = comment
            ev.application_status = status
            if status_id == 'RVAA':
                d_fields.append("institution_id")
                d_fields.append("months_approved")
                ev.institution_id = institution_id
                ev.months_approved = months
            ev.save(update_fields=d_fields)
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
            ob_station = get_data(request, 'Q7A_ob_station')
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
                          'ob_police_station': ob_station,
                          'case_record_id': crs_id,
                          'created_by': user_id})
            # update institute type on Main Table
            si_reg_id = si_obj.pk
            placement_id = obj.pk
            org_unit_id = int(inst_name)
            org_unit = RegOrgUnit.objects.get(id=org_unit_id)
            org_type = org_unit.org_unit_type_id
            SIMain.objects.filter(
                person_id=person_id, pk=si_reg_id).update(
                org_unit_id=org_unit_id, org_type=org_type,
                case_id=crs_id, placement_id=placement_id)
        # Handle Discharge in case of Release or Escape
        if form_id == 'FMSI021F' or form_id == 'FMSI019F':
            print('Process exit', request.POST)
            if si_obj.placement:
                placement_id = si_obj.placement.pk
                if placement_id:
                    pl = OVCPlacement.objects.get(pk=placement_id)
                    pl.is_active = False
                    pl.save(update_fields=['is_active'])
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
        vacancy_id = None
        if form_id in ['FMSI001F']:
            datas = SI_VacancyApp.objects.get(pk=event_id)
            event_id = datas.event_id
            vacancy_id = datas.pk
            print('ev id', event_id, vacancy_id)
        if form_id in ['FMSI033R']:
            datas = SI_VacancyApp.objects.get(pk=event_id)
            event_id = datas.event_id
            vacancy_id = datas.pk
            print('ev id', event_id, vacancy_id)
        event = SIEvents.objects.get(pk=event_id)
        ev_date = event.event_date
        event_date = ev_date.strftime('%d-%b-%Y')
        datas = SIForms.objects.filter(event_id=event_id, is_void=False)
        for data in datas:
            qid = data.question_id
            qval = data.item_value
            qvals = data.item_detail
            q_elem = qvals if qval in ['FMTF', 'FMTA', 'FMFL'] else qval
            if not qvals:
                if qid not in idata:
                    idata[qid] = [q_elem]
                else:
                    idata[qid].append(q_elem)
            else:
                idata[qid] = q_elem
        rel_datas = SIForms.objects.filter(
            event__related_to_id=event_id, is_void=False)
        # Handle child records
        itms_dict, itms = {}, []
        for data in rel_datas:
            ev_id = str(data.event_id)
            qid = data.question_id
            # qval = data.item_value
            qvals = data.item_detail
            if ev_id not in itms_dict:
                itms_dict[ev_id] = {qid: qvals}
            else:
                itms_dict[ev_id][qid] = qvals
        for itt in itms_dict:
            ftt = itms_dict[itt]
            ftt['event_id'] = itt
            ftt['event_date'] = event_date
            itms.append(ftt)
        if form_id in ['FMSI001F', 'FMSI033R'] and vacancy_id:
            datas = SI_VacancyApp.objects.filter(pk=vacancy_id)
            for data in datas:
                ev_date = data.date_of_application
                event_date = ev_date.strftime('%d-%b-%Y')
                next_date = data.date_of_next_mention
                n_date = None
                if next_date:
                    n_date = next_date.strftime('%d-%b-%Y')
                idata['Q1_ref_num'] = data.ref_no
                idata['event_date'] = event_date
                idata['Q2_crc_num'] = data.crc_no
                idata['Q3_pnc_num'] = data.pnc_no
                idata['Q4_court_num'] = data.court_number
                idata['Q5_magistrate_name'] = data.judge_name
                idata['Q7_child_held_at'] = data.child_held_at
                idata['Q8_child_held_at_name'] = data.holding_place
                idata['Q6_next_mention_date'] = n_date
                idata['Q9_request_officer'] = data.requesting_officer
                idata['Q10_designation'] = data.designation
                idata['Q11_scco'] = data.sub_county_children_officer
                # Confirmation
                app_status = data.application_status
                app_si = data.institution_id
                status = 'RVAR'
                if app_status:
                    status = 'RVAD'
                    if app_si:
                        status = 'RVAA'
                idata['Q1_status'] = status
                idata['Q3_months'] = data.months_approved
                idata['Q4_comment'] = data.comment
        idata['all_answers'] = itms
        idata['event_date'] = event_date
        idata['user_id'] = event.created_by_id
    except Exception as e:
        print('Error getting idata %s' % str(e))
        return {}
    else:
        return idata


def delete_event_data(request, form_id, event_id):
    """Method to GET event data."""
    try:
        cnt = 2
        if form_id in ['FMSI001F', 'FMSI033R']:
            si = SI_VacancyApp.objects.filter(
                pk=event_id, application_status=False)
            if si:
                cnt = 1
                si.delete()
        else:
            datas = SIEvents.objects.get(pk=event_id)
            delta = get_days_difference(datas.event_date)
            if delta > 90:
                cnt = 1
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
        return cnt


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


def save_jsons(
        request, form_id, person_id, care_id, event_id, event_date, si_datas):
    """Method to save jsons."""
    try:
        for si_id in si_datas:
            si_data = si_datas[si_id]
            for sidt in si_data:
                itdl = si_data[sidt][0]
                event_obj = save_event(
                    request, form_id, person_id, care_id, event_date, event_id)
                child_event_id = event_obj.pk
                # Save form elements
                obj, created = SIForms.objects.update_or_create(
                    event_id=child_event_id, question_id=sidt,
                    item_value='FMTA',
                    defaults={'item_detail': itdl})
    except Exception as e:
        raise e
    else:
        pass


def get_placement(request, person_id, single=1):
    """Method to get all placements."""
    try:
        idata = {}
        placements = OVCPlacement.objects.filter(
            person_id=person_id, is_void=False)
        placement = placements.filter(is_active=True).first()
        if placement:
            comm_period = placement.committing_period_units
            ev_date = placement.admission_date
            event_date = ev_date.strftime('%d-%b-%Y')
            idata['event_date'] = event_date
            idata['Q1_admission_num'] = placement.admission_number
            idata['Q3_admission_type'] = placement.admission_type
            idata['Q4_admission_reason'] = placement.admission_reason
            idata['Q5_has_committal'] = placement.has_court_committal_order
            idata['Q6_holding_days'] = placement.holding_period
            idata['Q7_ob_number'] = placement.ob_number
            idata['Q8_court_order_num'] = placement.court_order_number
            idata['Q9_court_order_date'] = placement.court_order_issue_date
            idata['Q10_court_name'] = placement.committing_court
            idata['Q11_committal_period_units'] = comm_period
            idata['Q12_committal_period'] = placement.committing_period
        print(idata)
    except Exception as e:
        raise e
    else:
        if single:
            if single == 2:
                return idata
            return placement
        else:
            return placements


def get_events(request, person_id, cnts=0):
    """Method to get events details."""
    try:
        forms = {}
        dforms = {'FMSI002F': 0, 'FMSI003F': 0, 'FMSI005F': 0}
        events = SIEvents.objects.filter(person_id=person_id, is_void=False)
        is_filled = 1
        if cnts:
            for event in events:
                fid = event.form_id
                case_id = event.care.case_id
                # print('case', fid, event.care.case_id, event.event_id)
                if fid == 'FMSI033R':
                    is_filled = 0
                    vacancy = SI_VacancyApp.objects.filter(
                        case_id=case_id).first()
                    if vacancy and vacancy.application_status:
                        is_filled = 1
                if fid not in forms:
                    forms[fid] = is_filled
            for dform in dforms:
                if dform not in forms:
                    forms[dform] = dforms[dform]
            return forms
    except Exception as e:
        print('Error getting forms - %s' % (str(e)))
        return {}
    else:
        return events


def get_user_level(request):
    """Method to get user level."""
    try:
        sis = ['TNAP', 'TNRH', 'TNRS', 'TNRR', 'TNRB', 'TNRC']
        fis = ['TNGP', 'TNGD']
        ou_type = request.session.get('ou_type')
        ou_pri = request.session.get('ou_primary')
        ou_sid = request.session.get('section_id')
        ou_lvl = request.session.get('user_level')
        print('OUT', ou_type, ou_pri, ou_sid, ou_lvl)
        user_level = 1 if ou_type and ou_type in fis else 0
        if ou_type in sis:
            user_level = 2
        if ou_pri == 2 or request.user.is_superuser:
            user_level = 3
    except Exception as e:
        print('Get user level error - %s' % (str(e)))
        return 0
    else:
        return user_level


def handle_uploads(request, f, form_id, person_id):
    try:
        ctype = f.content_type
        pid = str(person_id).zfill(10)
        fid = str(uuid.uuid4())
        allowed_exts = ["application/pdf"]
        print('Uploads', request.POST)
        f_name = None
        doc_type = request.POST.get('Q12A_document_type')
        if ctype in allowed_exts:
            f_ext = ctype.split('/')[1].replace('jpeg', 'jpg')
            f_name = '%s_%s.%s' % (fid, pid, f_ext)
            with open(MEDIA_ROOT + '/si_docs/' + f_name, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
            save_document(request, form_id, person_id, doc_type, f_name)
    except Exception as e:
        print('Error uploading file - %s' % (str(e)))
        return None
    else:
        return f_name


def save_document(request, form_id, person_id, doc_type, document):
    try:
        user_id = request.user.id
        doc, created = SI_Document.objects.update_or_create(
            form_id=form_id, person_id=person_id, document_type=doc_type,
            defaults={'document': document,
                      'created_by_id': user_id,
                      'is_void': False
                      })
    except Exception as e:
        print('Error uploading files - %s' % (str(e)))
        return False
    else:
        return doc


def dash_summary(request):
    """Method to get summaries."""
    try:
        dash = {}
        user_id = request.user.id
        user_level = get_user_level(request)
        ou_pri = request.session.get('ou_primary')
        ou_id = int(ou_pri) if ou_pri else 0
        placements = OVCPlacement.objects.filter(
            is_void=False, is_active=True)
        vacancies = SI_VacancyApp.objects.filter(
            application_status=False, is_void=False)
        if user_level < 3:
            placements = placements.filter(residential_institution_id=ou_id)
            vacancies = vacancies.filter(created_by_id=user_id)
        pls = placements.count()
        dash['placements'] = '{:,}'.format(pls)
        dash['vacancies'] = vacancies.count()
        # Others
        dash['discharges'] = 0
        dash['pending'] = 0
    except Exception as e:
        print('Error getting summaries - %s' % (str(e)))
        return {}
    else:
        return dash
