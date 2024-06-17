import segno

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.db.models import Count

from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from cpovc_stat_inst.forms import (SIForm)

from cpovc_stat_inst.functions import (
    CaseObj, get_form, delete_event_data,
    action_event_data, get_placement, get_user_level,
    dash_summary)

from cpovc_main.functions import get_dict

from cpovc_forms.functions import get_person_ids
from cpovc_registry.models import (
    RegPerson, RegOrgUnit, RegPersonsGuardians, RegPersonsGeo)

from .models import CCIEvents, CCIMain, CCIForms

from cpovc_forms.models import (
    OVCCaseRecord, OVCPlacement, OVCCaseCategory, OVCCaseGeo)
from cpovc_forms.forms import OVCSearchForm

from cpovc_stat_inst.parameters import FDEP, SI_FORMS, FPERM, INSTM
from cpovc_api.functions import save_form, get_event_data, get_events

from .parameters import DASHES

from django.conf import settings
DOC_ROOT = settings.DOC_ROOT


@login_required
def cci_home(request):

    try:
        form = OVCSearchForm(data=request.GET)
        search_string = request.GET.get('search_name')
        pids = get_person_ids(request, search_string)

        ctip_ids, case_ids = {}, {}
        cases = RegPerson.objects.filter(is_void=False, id__in=pids)

        # Get case record sheet details
        dash = dash_summary(request)
        crss = OVCCaseGeo.objects.filter(is_void=False, person_id__in=pids)
        for crs in crss:
            case_ids[crs.person_id] = {
                'clv': 1, 'cs': crs.case_id.case_serial,
                'cid': crs.case_id.case_id,
                'org_unit': crs.report_orgunit.org_unit_name}

        for case in cases:
            pid = case.id
            cid = ctip_ids[pid]['cid'] if pid in ctip_ids else 'N/A'
            cdt = ctip_ids[pid]['cdt'] if pid in ctip_ids else 'N/A'
            clvf = case_ids[pid]['clv'] if pid in case_ids else 0
            clv = ctip_ids[pid]['clv'] if pid in ctip_ids else clvf
            csn = case_ids[pid]['cs'] if pid in case_ids else 'N/A'
            ccid = case_ids[pid]['cid'] if pid in case_ids else 'N/A'
            ou = case_ids[pid]['org_unit'] if pid in case_ids else 'N/A'

            setattr(case, 'case_t', str(cid))
            setattr(case, 'case_date', cdt)
            setattr(case, 'case_level', clv)
            setattr(case, 'case_id', cid)
            setattr(case, 'case_cid', str(ccid))
            setattr(case, 'case_serial', csn)
            setattr(case, 'org_unit', ou)
        context = {
            'status': 200,
            'cases': cases,
            'form': form,
            'dash': dash
        }

        return render(request, 'cci/home.html', context)

    except Exception as e:
        raise e



@login_required
def cci_child_view(request, id):
    """ Child View"""
    try:
        forms, cases = {}, {}
        # TNRC is CCI
        ou_pri = request.session.get('ou_primary')
        user_level = get_user_level(request)
        person_id = RegPerson.objects.filter(id=id, is_void=False)
        placements = OVCPlacement.objects.filter(
            person_id=id, is_void=False)
        placement = placements.filter(is_active=True).first()
        si_data = CCIMain.objects.filter(
            person_id=id, case_status=None, is_void=False)
        case_id = None
        case_sc_id = 0
        if si_data:
            cidt = si_data.first()
            if cidt:
                case_id = cidt.case_id
                cases = OVCCaseCategory.objects.filter(
                    person_id=id, case_id_id=case_id)
                # CRS Geo
                cgeos = OVCCaseGeo.objects.filter(
                    person_id=id, case_id_id=case_id).first()
                if cgeos:
                    case_sc_id = cgeos.report_orgunit_id
        unit_type = None
        unit_name = 'Not placed'
        org_unit_id = 0
        if placement:
            org_unit_id = placement.residential_institution_id
            org_unit = RegOrgUnit.objects.get(id=org_unit_id)
            unit_type = org_unit.org_unit_type_id
            unit_name = org_unit.org_unit_name
        # unit_type = 'XXXX'
        child = person_id.first()
        is_allowed = False
        allow_edit = 1
        if user_level == 2 and ou_pri == org_unit_id:
            is_allowed = True
        if org_unit_id == 0:
            is_allowed = True
        if ou_pri == 2:
            user_level = 3
            is_allowed = True
            allow_edit = 0
        if request.user.is_superuser:
            user_level = 3
            is_allowed = True
        if user_level == 1 and ou_pri == case_sc_id:
            is_allowed = True
        # Events count
        forms = get_events(request, id, CCIEvents, 1)
        check_fields = ['sex_id', 'si_unit_type_id', 'case_category_id',
                        'cci_unit_type_id']
        vals = get_dict(field_name=check_fields)
        context = {'child': child, 'placement': placement, 'events': forms,
                   'unit_type': unit_type, 'unit_name': unit_name,
                   'placements': placements, 'vals': vals,
                   'si_data': si_data, 'cases': cases,
                   'allow_edit': allow_edit, 'case_id': case_id,
                   'user_level': user_level, 'is_allowed': is_allowed}
        return render(request, 'cci/view_child.html', context)

    except Exception as e:
        raise e


@login_required
def cci_forms(request, form_id, id):

    try:
        idata = {}
        person_id = int(id)
        if form_id == 'FMSI004F':
            idata = get_placement(request, id, 2)
        # Main
        si_main = CCIMain.objects.filter(person_id=id, is_void=False).first()
        case_serial = si_main.case_serial if si_main else 'XXX/YYYY'
        vacancy = None
        print('Vac', vacancy)
        user_level = get_user_level(request)
        care_id = None
        case_id = None
        if si_main:
            care_id = si_main.pk
            case_id = si_main.case_id
            if si_main.case:
                idata['Q1_ref_num'] = si_main.case.case_serial
        placement = get_placement(request, id)
        form = SIForm(form_id, data=idata)
        form_data = get_form(form_id)
        form_name = form_data['form_name']
        f_code = form_data['form_code']
        form_code = f_code if f_code else form_id
        if request.method == 'POST':
            FormObj = CaseObj()
            FormObj.forms = CCIForms
            FormObj.main = CCIMain
            FormObj.event = CCIEvents
            save_form(request, FormObj, form_id, id, form_id)
            url = reverse(cci_child_view, kwargs={'id': id})
            msg = 'SI Form (%s) details saved successfully' % form_name
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(url)
        check_fields = ['sex_id', 'yesno_id',
                        'relationship_type_id', 'area_type_id']
        vals = get_dict(field_name=check_fields)
        case = CaseObj()
        person = RegPerson.objects.get(id=id, is_void=False)
        # vacancies = SI_VacancyApp.objects.filter(person_id=id)
        vacancies = {}
        events = CCIEvents.objects.filter(
            person_id=person_id, is_void=False,
            form_id=form_id, related_to_id=None)
        cases = OVCCaseRecord.objects.filter(
            person_id=person_id, is_void=False)
        case.person = person
        case.vacancies = vacancies
        case.events = events
        case.cases = cases
        case.care_id = care_id
        case.si_case = si_main
        case.vacancy = vacancy
        # Cases
        if case_id:
            case.case_id = case_id
        case.placement = placement
        org_types = ['TNRR', 'TNAP']
        allow_edit = 0 if user_level == 3 else 1
        # Past events
        forms = get_events(request, id, 1)
        # Form dependancies logic
        ffill, dep_forms = [], []
        fdeps = FDEP[form_id] if form_id in FDEP else []
        for f in forms:
            if forms[f] > 0:
                ffill.append(f)
        all_filled = set(fdeps).issubset(ffill)
        inst_type = request.session.get('ou_type', 'XXXX')
        print(inst_type)
        A_IN = INSTM[form_id] if form_id in INSTM else []
        if inst_type not in A_IN:
            all_filled = True
        for fdep in fdeps:
            dep_forms.append(SI_FORMS[fdep])
        # Forms permissions
        perms = False
        form_perms = FPERM[form_id] if form_id in FPERM else {}
        pss = form_perms[user_level] if user_level in form_perms else ['']
        ps = pss[0]
        print('PS', ps, 'AE', allow_edit)
        if 'C' in ps:
            perms = True
        # Override for super admin - Debugging and Testing was headache
        if request.user.is_superuser:
            ps = 'CRUD'
            allow_edit = True
            perms = True
        orgs = RegOrgUnit.objects.filter(
            org_unit_type_id__in=org_types,
            is_void=False).order_by('org_unit_type_id')
        caregivers = RegPersonsGuardians.objects.select_related().filter(
            child_person_id=person_id, is_void=False, date_delinked=None)
        person_geos = RegPersonsGeo.objects.select_related().filter(
            person_id=person_id, is_void=False, date_delinked=None)
        tmpl = '%s.html' % form_id
        # Dynamic Back URLS
        back_url = reverse(cci_child_view, kwargs={'id': person_id})
        context = {'form': form, 'case': case, 'vals': vals,
                   'form_id': form_id, 'form_name': form_name,
                   'edit_form': 1, 'orgs': orgs, 'form_code': form_code,
                   'events': forms, 'user_level': user_level,
                   'vacancy_status': 0, 'allow_edit': allow_edit,
                   'all_perms': ps, 'caregivers': caregivers,
                   'person_geos': person_geos, 'BACK_URL': back_url,
                   'EDIT_URL': 'cci_form_edit', 'DELETE_URL': 'cci_form_delete',
                   'case_num': case_serial}
        if not all_filled or not perms:
            context['dep_forms'] = dep_forms
            context['dep_perms'] = perms
            return render(request, 'gforms/FMSI000R.html', context)
        return render(request, 'gforms/%s' % tmpl, context)

    except Exception as e:
        raise e


@login_required
def cci_forms_edit(request, form_id, id, ev_id):
    try:
        FormObj = CaseObj()
        FormObj.forms = CCIForms
        FormObj.main = CCIMain
        FormObj.event = CCIEvents
        person_id = int(id)
        user_id = request.user.id
        idata = get_event_data(form_id, ev_id, FormObj)
        print('idata', idata)
        all_answers = idata['all_answers'] if 'all_answers' in idata else []
        user_level = get_user_level(request)
        # Uploads
        form = SIForm(form_id, idata)
        form_data = get_form(form_id)
        form_name = form_data['form_name']
        f_code = form_data['form_code']
        form_code = f_code if f_code else form_id
        if request.method == 'POST':
            save_form(request, FormObj, form_id, id, form_id, 2)
            url = reverse(cci_child_view, kwargs={'id': id})
            msg = 'Form (%s) details saved successfully' % form_name
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(url)
        check_fields = ['sex_id', 'relationship_type_id', 'area_type_id']
        vals = get_dict(field_name=check_fields)
        case = CaseObj()
        # Case main table
        # si_case = CCIMain.objects.get(person_id=person_id)
        si_case = CCIMain.objects.filter(
            person_id=person_id, is_void=False).first()
        case_serial = si_case.case_serial
        care_id = si_case.pk
        case_id = si_case.case_id
        person = RegPerson.objects.get(id=id, is_void=False)
        vacancy = None
        placement = OVCPlacement.objects.filter(
            person_id=id, is_void=False, is_active=True).first()
        events = CCIEvents.objects.filter(
            person_id=person_id, is_void=False,
            form_id=form_id, related_to_id=None)
        cases = OVCCaseRecord.objects.filter(
            person_id=person_id, is_void=False)
        case.person = person
        case.vacancy = vacancy
        case.events = events
        case.placement = placement
        case.cases = cases
        case.all_answers = all_answers
        case.event_id = ev_id
        case.care_id = care_id
        case.si_case = si_case
        si, scco = {}, {}
        print('check case_id', si_case)
        vac_status = 0
        allow_edit = 0 if user_level == 3 else 1
        if case_id:
            case.case_id = case_id
            if vacancy and vacancy.institution:
                si_type = vacancy.institution.org_unit_type_id
                si['type'] = si_type
                vac_status = 1
            casegeo = OVCCaseGeo.objects.filter(case_id_id=case_id).first()
            if casegeo:
                scco['name'] = casegeo.report_orgunit.org_unit_name
        case.si = si
        case.scco = scco
        # Get Organization details
        org_types = ['TNRR', 'TNAP']
        orgs = RegOrgUnit.objects.filter(
            org_unit_type_id__in=org_types,
            is_void=False).order_by('org_unit_type_id')
        # Permission matrix
        form_perms = FPERM[form_id] if form_id in FPERM else {}
        pss = form_perms[user_level] if user_level in form_perms else ['']
        perms = pss[0]
        # User overwrite
        record_user_id = idata['user_id'] if 'user_id' in idata else 0
        if record_user_id == user_id:
            perms = 'CRUD'
        if record_user_id == user_id and user_level < 3:
            perms = 'CR'
        # print('P', perms, 'AE', allow_edit)
        caregivers = RegPersonsGuardians.objects.select_related().filter(
            child_person_id=person_id, is_void=False, date_delinked=None)
        person_geos = RegPersonsGeo.objects.select_related().filter(
            person_id=person_id, is_void=False, date_delinked=None)
        tmpl = '%s.html' % form_id
        # URLS
        back_url = reverse(cci_child_view, kwargs={'id': person_id})
        context = {'form': form, 'case': case, 'vals': vals,
                   'form_id': form_id, 'form_name': form_name,
                   'edit_form': 0, 'event_id': ev_id, 'status': 1,
                   'form_code': form_code, 'all_answers': all_answers,
                   'user_level': user_level, 'orgs': orgs,
                   'vacancy_status': vac_status, 'idata': idata,
                   'allow_edit': allow_edit, 'all_perms': perms,
                   'caregivers': caregivers, 'person_geos': person_geos,
                   'EDIT_URL': 'cci_form_edit', 'DELETE_URL': 'cci_form_delete',
                   'BACK_URL': back_url, 'case_num': case_serial}
        return render(request, 'gforms/%s' % tmpl, context)

    except Exception as e:
        raise e


@login_required
def cci_forms_delete(request):
    """Method to delete forms."""
    try:
        response = {"message": "Form entry deleted successfully", 'deleted': 1}
        if request.method == 'POST':
            form_id = request.POST.get('form_id')
            event_id = request.POST.get('event_id')
            idata = delete_event_data(request, form_id, event_id)
            if idata == 0:
                response["deleted"] = 0
                response["message"] = "Error deleting record"
            elif idata == 2:
                response["deleted"] = 0
                response["message"] = "90+ old days events can not be deleted"
    except Exception as e:
        response = {"deleted": 0,
                    "message": "Error deleting record %s" % (str(e))}
        return JsonResponse(
            response, content_type='application/json', safe=False)
    else:
        return JsonResponse(
            response, content_type='application/json', safe=False)


@login_required
def cci_forms_action(request):
    """Method to delete forms."""
    try:
        response = {"message": "Form entry actioned successfully", 'status': 1}
        if request.method == 'POST':
            print(request.POST)
            form_id = request.POST.get('form_id')
            event_id = request.POST.get('event_id')
            idata = action_event_data(request, form_id, event_id)
            if idata == 0:
                response["status"] = 0
                response["message"] = "Error changing record"
    except Exception as e:
        response = {"status": 0,
                    "message": "Error changing record %s" % (str(e))}
        return JsonResponse(
            response, content_type='application/json', safe=False)
    else:
        return JsonResponse(
            response, content_type='application/json', safe=False)


def cci_document(request, form_id):
    """Method to Generate PDF."""
    try:
        # html_string = '<p>Sample</p>'
        if request.method == 'POST':
            person_id = request.POST.get('person_id')
            fdata = request.POST.get('form_data')
            # doc_id = '%s_%s' % (form_id, person_id)
            print('session', person_id, form_id)
            request.session[form_id] = fdata
        form_data = get_form(form_id)
        form_name = form_data['form_name']
        fname = '%s.pdf' % (form_id)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="%s"' % fname

        # Render the template with the data from the Django model
        context = {'form_id': form_id, 'form_name': form_name}
        # Bar code
        # rv = BytesIO()
        # EAN13("100000902922", writer=barcode.writer.SVGWriter()).write(rv)
        '''
        svg = "img/tmp_somefile.svg"
        code = form_id
        with open('static/%s' % svg, "wb") as f:
            Code128(
                code,
                writer=barcode.writer.SVGWriter()).write(f)
        context['svg'] = svg
        '''
        # doc_id = '%s_9427' % (form_id)
        form_data = request.session.get(form_id, '<p>TO DO</p>')
        context['form_data'] = form_data
        html_string = render_to_string('si/document.html', context)
        # Create the PDF from the HTML string
        HTML(
            string=html_string,
            base_url=request.build_absolute_uri()).write_pdf(response)
    except Exception as e:
        raise e
    else:
        return response


def si_file(request, event_id):
    """Method to Generate PDF."""
    try:
        form_id = 'FMSI033R'
        vacancy = SI_VacancyApp.objects.filter(
            pk=event_id, is_void=False).first()
        case_id = vacancy.case_id
        print('GET Case file ', case_id)
        form_data = get_form(form_id)
        form_name = form_data['form_name']
        fname = '%s.pdf' % (form_id)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="%s"' % fname
        # Render the template with the data
        context = {'form_id': form_id, 'form_name': form_name}
        case = CaseObj()
        case.vacancy = vacancy
        print('case', vacancy.case_id)
        # Geo
        scco = {}
        casegeo = OVCCaseGeo.objects.filter(case_id_id=case_id).first()
        if casegeo:
            scco['name'] = casegeo.report_orgunit.org_unit_name
        case.scco = scco
        context['case'] = case
        # Generate QR code
        pid = vacancy.person.id
        fname = vacancy.person.first_name
        sname = vacancy.person.surname
        pnc = vacancy.pnc_no
        names = '%s %s' % (fname, sname)
        uid = None
        if vacancy.approved_by:
            uid = vacancy.approved_by.reg_person_id
        qrcode = segno.make_qr(
            "F.No:%s\nCPIMS.ID:%s\n%s\nAID:%s" % (
                pnc, pid, names, uid))
        qrcode.save(
            "%s/img/qr_code_%s.png" % (DOC_ROOT, pid),
            scale=3,
        )
        context['qr_code'] = 'img/qr_code_%s.png' % (pid)
        html_string = render_to_string('si/document.html', context)
        # Create the PDF from the HTML string
        HTML(
            string=html_string,
            base_url=request.build_absolute_uri()).write_pdf(response)
    except Exception as e:
        raise e
    else:
        return response


@login_required
def cci_dash_view(request, id):
    """ Child View"""
    try:
        did = int(id)
        summaries = []
        user_id = request.user.id
        dash = DASHES[did] if did in DASHES else DASHES[1]
        check_fields = ['sex_id', 'si_unit_type_id', 'case_category_id',
                        'cci_unit_type_id', 'si_unit_type_id']
        vals = get_dict(field_name=check_fields)
        user_level = get_user_level(request)
        ou_pri = request.session.get('ou_primary')
        ou_id = int(ou_pri) if ou_pri else 0
        sis = ['TNRC']
        if did == 1:
            summaries = OVCPlacement.objects.filter(
                is_void=False, is_active=True, residential_institution__org_unit_type_id__in=sis)
            if user_level < 3:
                summaries = summaries.filter(residential_institution_id=ou_id)
            else:
                summaries = summaries.filter(
                    is_void=False, is_active=True).extra(
                    select={'name':'residential_institution__org_unit_type_id'}).values(
                    'residential_institution__org_unit_type_id').annotate(
                    dcount=Count('residential_institution__org_unit_type_id'))
        if did == 5:
            si = request.GET.get('si')
            if si:
                sis = [si]
            summaries = OVCPlacement.objects.filter(
                is_void=False, is_active=True)
            if user_level < 3:
                summaries = summaries.filter(residential_institution_id=ou_id)
            else:
                summaries = OVCPlacement.objects.filter(
                    is_void=False, is_active=True,
                    residential_institution__org_unit_type_id__in=sis).values(
                    'residential_institution__org_unit_name').annotate(
                    dcount=Count('residential_institution__org_unit_name'))
        elif did == 3:
            # Vacancies
            summaries = {}
        context = {'vals': vals, 'dashboard': dash, 'summaries': summaries,
                   'user_level': user_level, 'did': did}
        return render(request, 'cci/dashboard.html', context)

    except Exception as e:
        raise e
