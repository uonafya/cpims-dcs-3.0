import json
import uuid
from django.utils import timezone
from django.db.models import Count

from cpovc_main.models import ListQuestions
from cpovc_main.functions import convert_date, get_days_difference
from cpovc_afc.models import AFCMain, AFCEvents

from cpovc_forms.models import OVCPlacement, OVCCaseCategory, OVCCaseRecord
from cpovc_registry.models import (
    RegOrgUnit, RegPerson, RegPersonsOrgUnits, RegPersonsTypes,
    RegPersonsExternalIds)

from cpovc_auth.models import AppUser
from cpovc_ovc.models import OVCRegistration


from django.conf import settings
MEDIA_ROOT = settings.MEDIA_ROOT

def form_handler(request, FormObj, form_id, form_guid):
    """Method to handle Generic forms."""
    try:
        person_id = request.POST.get('person_id')
        save_form(request, FormObj, form_id, person_id, form_guid)
    except Exception as e:
        print("Error handling generic Forms - %s" % (str(e)))
        return False
    else:
        return True



def save_reg(request, case_id, event_date, org_type, person_id, FormObjs, oid=0):
    """Method to get Alt Care case."""
    try:
        FormObj = FormObjs.main
        # Org unit and user
        print('REG', case_id, event_date, org_type, person_id, oid)
        ou_id = request.session.get('ou_primary', None)
        org_unit_id = 1 if not ou_id else ou_id
        if oid:
            org_unit_id = oid
        user_id = request.user.id
        obj, created = FormObj.objects.update_or_create(
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


def save_event(request, form_id, person_id, care_id, event_date, FormObjs, rev=None):
    """Method to save Event."""
    try:
        FormObj = FormObjs.event
        user_id = request.user.id
        defaults = {'event_date': event_date, 'created_by_id': user_id}
        # Handle Child Events
        if rev:
            defaults['related_to_id'] = rev
        obj, created = FormObj.objects.update_or_create(
            care_id=care_id, form_id=form_id,
            person_id=person_id, is_void=False,
            defaults=defaults)
    except Exception as e:
        print('Error saving event %s' % (str(e)))
        return None
    else:
        return obj


def save_form(request, FormObjs, form_id, person_id, form_guid, edit_id=1):
    """Method to save all forms"""
    try:
        fms = {}
        FormObj = FormObjs.forms
        org_type = 'XXXX'
        user_id = request.user.id
        ev_date = request.POST.get('event_date')
        all_answers = request.POST.get('all_answers', '{}')
        si_datas = json.loads(all_answers)
        print('JSONS', si_datas)
        event_date = convert_date(ev_date) if ev_date else timezone.now()
        case_id = request.POST.get('case_id', None)
        print('Final Check', form_id, person_id, case_id)
        if form_guid == 'FMSI005F':
            case_id = request.POST.get('case_record_id')
        si_obj = save_reg(request, case_id, event_date, org_type, person_id, FormObjs)
        questions = ListQuestions.objects.filter(
            form__form_guid=form_guid, is_void=False)
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
            request, form_id, person_id, care_id, event_date, FormObjs)
        event_id = event_obj.pk
        print('Save the form %s' % (form_id))
        # Save jsons
        if si_datas:
            save_jsons(request, form_id, person_id, care_id,
                       event_id, event_date, si_datas, FormObjs)
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
                    obj, created = FormObj.objects.update_or_create(
                        event_id=event_id, question_id=qid,
                        item_value=q_val,
                        defaults={'item_detail': itdl})
            # Handle delete for checkboxes
            for qid in qdels:
                qitms = qdels[qid]
                FormObj.objects.filter(
                    event_id=event_id, question_id=qid).exclude(
                    item_value__in=qitms).delete()
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
            FormMain = FormObjs.main
            si_reg_id = si_obj.pk
            placement_id = obj.pk
            org_unit_id = int(inst_name)
            org_unit = RegOrgUnit.objects.get(id=org_unit_id)
            org_type = org_unit.org_unit_type_id
            FormMain.objects.filter(
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


def save_jsons(
        request, form_id, person_id, care_id, event_id, event_date, si_datas, FormObjs):
    """Method to save jsons."""
    try:
        for si_id in si_datas:
            si_data = si_datas[si_id]
            for sidt in si_data:
                itdl = si_data[sidt][0]
                event_obj = save_event(
                    request, form_id, person_id, care_id, event_date, event_id, FormObjs)
                child_event_id = event_obj.pk
                # Save form elements
                obj, created = AFCForms.objects.update_or_create(
                    event_id=child_event_id, question_id=sidt,
                    item_value='FMTA',
                    defaults={'item_detail': itdl})
    except Exception as e:
        raise e
    else:
        pass


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


def get_event_data(form_id, event_id, FormObjs):
    """Method to GET event data."""
    try:
        FormObj = FormObjs.forms
        EventObj = FormObjs.event
        idata = {}
        vacancy_id = None
        event = EventObj.objects.get(pk=event_id)
        ev_date = event.event_date
        event_date = ev_date.strftime('%d-%b-%Y')
        datas = FormObj.objects.filter(event_id=event_id, is_void=False)
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
        rel_datas = FormObj.objects.filter(
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
        idata['all_answers'] = itms
        idata['event_date'] = event_date
        idata['user_id'] = event.created_by_id
    except Exception as e:
        print('Error getting idata %s' % str(e))
        return {}
    else:
        return idata


def get_events(request, person_id, EventsObj, cnts=0):
    """Method to get events details."""
    try:
        forms = {}
        dforms = {'FMSI002F': 0, 'FMSI003F': 0, 'FMSI005F': 0}
        events = EventsObj.objects.filter(person_id=person_id, is_void=False)
        is_filled = 1
        if cnts:
            for event in events:
                fid = event.form_id
                case_id = event.care.case_id
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


def get_child_units(org_ids):
    """Method to do the organisation tree."""
    try:
        # print org_ids
        orgs = RegOrgUnit.objects.filter(
            parent_org_unit_id__in=org_ids).values_list('id', flat=True)
        print('Check Org Unit level - %s' % (str(orgs)))
    except Exception as e:
        print('No parent unit - %s' % (str(e)))
        return []
    else:
        return list(orgs)


def get_attached_orgs(request):
    """Method to get attached units."""
    try:
        orgs = []
        dcs = 'Directorate of Children Services (DCS)'
        person_id = request.user.reg_person_id
        person_orgs = RegPersonsOrgUnits.objects.filter(
            person_id=person_id, is_void=False)
        reg_pri, reg_ovc, reg_pri_name = 2, False, dcs
        all_roles, all_ous = [], []
        for p_org in person_orgs:
            p_roles = []
            org_id = p_org.org_unit_id
            org_name = p_org.org_unit.org_unit_name
            reg_assist = p_org.reg_assistant
            if reg_assist:
                p_roles.append('REGA')
                all_roles.append('REGA')
            reg_prim = p_org.primary_unit
            if reg_prim:
                reg_pri = org_id
                reg_pri_name = org_name
            reg_ovc = p_org.org_unit.handle_ovc
            if reg_ovc:
                p_roles.append('ROVC')
                all_roles.append('ROVC')
                reg_ovc = True
            pvals = {org_id: p_roles}
            orgs.append(pvals)
            all_ous.append(str(org_id))
        # allroles = ','.join(list(set(all_roles)))
        # allous = ','.join(all_ous)
        child_ous = get_child_units([reg_pri])
        vals = {'perms': orgs, 'ou_id': reg_pri,
                'attached_ou': all_ous, 'perms_ou': all_roles,
                'reg_ovc': reg_ovc, 'ou_name': reg_pri_name,
                'ou_attached': child_ous}
    except Exception as e:
        print('Error with dashboard - %s' % (str(e)))
        return {}
    else:
        return vals


def dcs_dashboard(request, params):
    """Method to get dashboard totals."""
    try:
        dash = {}
        vals = {'TBVC': 0, 'TBGR': 0, 'TWGE': 0, 'TWNE': 0}
        pr_ouid = int(request.session.get('ou_primary', 0))
        if request.user.is_superuser or pr_ouid == 2:
            person_types = RegPersonsTypes.objects.filter(
                is_void=False, date_ended=None).values(
                    'person_type_id').annotate(dc=Count('person_type_id'))
            for person_type in person_types:
                vals[person_type['person_type_id']] = person_type['dc']
            dash['children'] = vals['TBVC']
            dash['caregivers'] = vals['TBGR']
            dash['government'] = vals['TWGE']
            dash['ngo'] = vals['TWNE']
            # Get org units
            org_units = RegOrgUnit.objects.filter(is_void=False).count()
            dash['org_units'] = org_units
            # Case categories to find pending cases
            cases_category = OVCCaseCategory.objects.filter(is_void=False)
            # Case records counts
            case_records = OVCCaseRecord.objects.filter(is_void=False)
            case_counts = cases_category.count()
            dash['case_records'] = case_counts
            # Workforce members
            workforce_members = RegPersonsExternalIds.objects.filter(
                identifier_type_id='IWKF', is_void=False).count()
            workforce_members = AppUser.objects.distinct(
                'reg_person_id').count()
            dash['workforce_members'] = workforce_members
            # Get pending
            cases = case_records.filter(case_stage=0).values_list(
                'case_id', flat=True).distinct()
            pending_count = cases_category.filter(
                case_id_id__in=cases).count()
            dash['pending_cases'] = pending_count
            # Child registrations
            ptypes = RegPersonsTypes.objects.filter(
                person_type_id='TBVC', is_void=False,
                date_ended=None).values_list('person_id', flat=True)
            cregs = RegPerson.objects.filter(id__in=ptypes).values(
                'created_at').annotate(unit_count=Count('created_at'))
            # Institution Population
            dash['inst_pop'] = {'B': 0, 'G': 0}
        else:
            # Org units
            cbo_id = request.session.get('ou_primary', 0)
            cbo_ids = request.session.get('ou_attached', [])
            print(cbo_ids)
            org_id = int(cbo_id)
            org_ids = get_orgs_child(org_id)
            # Workforce members using Appuser
            person_orgs = RegPersonsOrgUnits.objects.select_related().filter(
                org_unit_id__in=org_ids, is_void=False,
                date_delinked=None).values_list('person_id', flat=True)
            users = AppUser.objects.filter(
                reg_person_id__in=person_orgs)
            user_ids = users.values_list('id', flat=True)
            print('user ids', user_ids)
            users_count = users.count()
            dash['workforce_members'] = users_count
            person_types = RegPersonsTypes.objects.filter(
                is_void=False, date_ended=None,
                person__created_by_id__in=user_ids).values(
                    'person_type_id').annotate(dc=Count('person_type_id'))
            for person_type in person_types:
                vals[person_type['person_type_id']] = person_type['dc']
            dash['children'] = vals['TBVC']
            dash['caregivers'] = vals['TBGR']
            dash['government'] = vals['TWGE']
            dash['ngo'] = vals['TWNE']
            # Get org units
            orgs_count = len(org_ids) - 1 if len(org_ids) > 1 else 1
            dash['org_units'] = orgs_count
            # Org unit cases
            case_ids = OVCCaseGeo.objects.select_related().filter(
                report_orgunit_id__in=org_ids,
                is_void=False).values_list('case_id_id', flat=True)
            # Case records counts
            case_records = OVCCaseRecord.objects.filter(
                case_id__in=case_ids, is_void=False)
            # Case categories to find pending cases
            cases_category = OVCCaseCategory.objects.filter(
                is_void=False, case_id_id__in=case_ids)
            case_counts = cases_category.count()
            dash['case_records'] = case_counts
            # Get pending
            cases = case_records.filter(
                case_stage=0, case_id__in=case_ids).values_list(
                'case_id', flat=True).distinct()
            pending_count = cases_category.filter(
                case_id_id__in=cases).count()
            dash['pending_cases'] = pending_count
            # Child registrations
            ptypes = RegPersonsTypes.objects.filter(
                person_type_id='TBVC', is_void=False,
                date_ended=None).values_list('person_id', flat=True)
            cregs = RegPerson.objects.filter(
                id__in=ptypes, created_by_id__in=user_ids).values(
                'created_at').annotate(unit_count=Count('created_at'))
            # Institution Population
            inst_pop = {'B': 0, 'G': 0}
            ou_type = request.session.get('ou_type', None)
            print('OU TYPE', ou_type)
            if ou_type:
                inst_id = request.session.get('ou_primary', 0)
                ou_attached = request.session.get('ou_attached', 0)
                print('OU ID', inst_id, ou_attached)
                inst_pops = OVCPlacement.objects.filter(
                    residential_institution_name=str(inst_id),
                    is_active=True, is_void=False).values(
                    'person__sex_id').annotate(
                    dcount=Count('person__sex_id'))
                for ipop in inst_pops:
                    if str(ipop['person__sex_id']) == 'SFEM':
                        inst_pop['G'] = ipop['dcount']
                    else:
                        inst_pop['B'] = ipop['dcount']
            dash['inst_pop'] = inst_pop
        # OVC
        oregs = OVCRegistration.objects.values(
            'registration_date').annotate(
            unit_count=Count('registration_date'))
        child_regs, case_regs, ovc_regs = {}, {}, {}
        for creg in cregs:
            the_date = creg['created_at']
            # cdate = '1900-01-01'
            cdate = the_date.strftime('%d-%b-%y')
            # child_regs[str(cdate)] = creg['unit_count']
        for oreg in oregs:
            the_date = oreg['registration_date']
            # cdate = the_date.strftime('%d-%b-%y')
            # ovc_regs[str(cdate)] = oreg['unit_count']
        # Case Records
        ovc_regs = case_records.values(
            'date_case_opened').annotate(unit_count=Count('date_case_opened'))
        for ovc_reg in ovc_regs:
            the_date = ovc_reg['date_case_opened']
            # cdate = '1900-01-01'
            # cdate = the_date.strftime('%d-%b-%y')
            # case_regs[str(cdate)] = ovc_reg['unit_count']
        # Case categories Top 5
        case_categories = cases_category.values(
            'case_category').annotate(unit_count=Count(
                'case_category')).order_by('-unit_count')
        dash['child_regs'] = child_regs
        dash['ovc_regs'] = []
        dash['case_regs'] = case_regs
        dash['case_cats'] = []
    except Exception as e:
        print('error with dash - %s' % (str(e)))
        dash = {}
        dash['children'] = 0
        dash['caregivers'] = 0
        dash['government'] = 0
        dash['ngo'] = 0
        dash['org_units'] = 0
        dash['case_records'] = 0
        dash['workforce_members'] = 0
        dash['pending_cases'] = 0
        dash['child_regs'] = []
        dash['ovc_regs'] = []
        dash['case_regs'] = []
        dash['case_cats'] = 0
        # Institution Population
        dash['inst_pop'] = {'B': 0, 'G': 0}
        return dash
    else:
        return dash
