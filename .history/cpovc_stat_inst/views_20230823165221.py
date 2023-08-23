from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .forms import (
    SIAdmission, SICaseReferral, RemandHomeEscape, MedicalAssesmentForm,
    SICertificateofExit, SIRecordofVisits, IndividualCarePlanForm,
    SIFamilyConference, SIReleaseForm, SIChildProfile, SIAdmission,
    SINeedRiskAssessment, SINeedRiskScale, SIVacancyApp,
    SIVacancyConfirm, SISocialInquiry, LeaveOfAbsenceForm,
    SIForm)

from .functions import (
    CaseObj, get_form, save_form, get_event_data, delete_event_data,
    action_event_data)

from cpovc_main.functions import convert_date, get_dict

from cpovc_forms.functions import get_person_ids
from cpovc_registry.models import RegPerson, RegOrgUnit

from .models import SI_Admission, SI_VacancyApp, SIEvents

from cpovc_forms.models import OVCCaseRecord, OVCPlacement
from cpovc_forms.forms import OVCSearchForm

# Create your views here.
from cpovc_afc.forms import AFCForm2A


def si_home(request):

    try:
        form = OVCSearchForm(data=request.GET)

        search_string = request.GET.get('search_name')
        pids = get_person_ids(request, search_string)

        ctip_ids, case_ids = {}, {}
        cases = RegPerson.objects.filter(is_void=False, id__in=pids)

        # Get case record sheet details
        crss = OVCCaseRecord.objects.filter(is_void=False, person_id__in=pids)
        for crs in crss:
            case_ids[crs.person_id] = {
                'clv': 1, 'cs': crs.case_serial, 'cid': crs.case_id}

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
        context = {
            'status': 200,
            'cases': cases,
            'form': form
        }

        return render(request, 'stat_inst/home.html', context)

    except Exception as e:
        raise e


def SI_admissions(request, id):

    person_id = RegPerson.objects.filter(id=id, is_void=False)

    child = person_id.values()[0]

    form = SIAdmission()
    try:
        if(request.method == "POST"):
            data = request.POST

            print(data)
            SI_Admission(
                person_id=data.get('person_id'),
                institution_type=data.get('institution_type'),
                date_of_admission=convert_date(data.get('date_of_admission')),
                current_year_of_school=data.get('current_year_of_school'),
                type_of_entry=data.get('type_of_entry'),
                referral_source=data.get('referral_source'),
                child_category=data.get('child_category'),
                abused_child_desc=data.get('abused_child_desc'),
                referral_source_others=data.get('referral_source_others'),
                referrer_name=data.get('referrer_name'),
                referrer_address=data.get('referrer_address'),
                referrer_phone=data.get('referrer_phone'),
                not_contact_child=data.get('not_contact_child'),
                name_not_contact_child=data.get('name_not_contact_child'),
                relationship_to_child_not_contact_child=data.get(
                    'relationship_to_child_not_contact_child'),
                consent_form_signed=data.get('consent_form_signed'),
                commital_court_order=data.get('commital_court_order'),
                school_name=data.get('school_name'),
                health_status=data.get('health_status'),
                special_needs=data.get('special_needs'),
                workforce_id=data.get('workforce_id'),
                audit_date=convert_date(data.get('audit_date'))
            ).save()

            HttpResponseRedirect(reverse(si_home))
        context = {
            'form': form,
            'child': child
        }
        return render(request, 'stat_inst/admission.html', context)

    except Exception as e:
        raise e


def SI_childIdentification(request, person_id):

    form = SIChildIdentification()
    context = {
        'form': form
    }
    return render(request, 'stat_inst/childIdentification.html', context)


def si_casereferral(request, id):

    form = SICaseReferral()
    try:

        context = {
            'form': form
        }

        return render(request, 'stat_inst/case_referral.html', context)
    except Exception as e:
        raise e


def SI_needriskform(request, id):

    form = SINeedRiskAssessment()
    person_id = RegPerson.objects.filter(id=id, is_void=False)

    child = person_id.values()[0]

    try:

        context = {
            'form': form,
            'child': child
        }
        return render(request, 'stat_inst/needriskform.html', context)

    except Exception as e:
        raise e


def SI_medicalassesment(request, id):

    form = MedicalAssesmentForm()
    context = {
        'form': form
    }

    return render(request, 'stat_inst/medicalassesmentform.html', context)


def si_certificateofexit(request, id):

    form = SICertificateofExit()

    try:

        context = {
            'form': form
        }

        return render(request, 'stat_inst/certificate_of_exit.html', context)
#       return render(request,'stat_inst/certificate_of_exit.html',context)

    except Exception as e:
        raise e


def SI_individualCarePlan(request, id):

    form = IndividualCarePlanForm()

    person_id = RegPerson.objects.filter(id=id, is_void=False)

    child = person_id.values()[0]
    try:

        context = {
            'id': id,
            'form': form,
            "child": child
        }
        return render(
            request, 'stat_inst/individualtreatmentplan.html', context)

    except Exception as e:
        raise e


def SI_LeaveOfAbscence(request, id):

    form = LeaveOfAbsenceForm()
    try:

        context = {
            'id': id,
            'form': form
        }
        return render(
            request, 'stat_inst/leaveofabsenceassesmentform.html', context)

    except Exception as e:
        raise e


def SI_RemandHomeEscape(request, id):

    form = RemandHomeEscape()
    try:

        context = {
            'id': id,
            'form': form
        }
        return render(request, 'stat_inst/escapeform.html', context)

    except Exception as e:
        raise e


def SI_needriskscale(request, id):

    form = SINeedRiskScale()
    context = {
        "form": form
    }

    return render(request, 'stat_inst/needriskscale.html', context)


def si_remandhomeescape(request, id):

    form = RemandHomeEscape()
    context = {
        'form': form
    }

    return render(request, 'stat_inst/remand_home_escape.html', context)


def SI_vacancyapplication(request, id):

    form = SIVacancyApp()
    person_id = RegPerson.objects.filter(id=id, is_void=False)

    print(dir(request))

    child = person_id.values()[0]

    try:

        context = {
            'form': form,
            "child": child
        }

        return render(request, 'stat_inst/vacancy_app.html', context)
    except Exception as e:
        raise e


def si_recordofvisits(request, id):

    form = SIRecordofVisits()
    try:

        context = {
            'form': form
        }
        return render(request, 'stat_inst/record_of_visits.html', context)

    except Exception as e:
        raise e


def si_familyconference(request, id):

    form = SIFamilyConference()
    context = {
        'form': form
    }

    return render(request, 'stat_inst/family_conference.html', context)


def SI_vacancyconfirmation(request, id):

    try:
        pass
    except Exception as e:
        raise e


def SI_social_inquiry(request, id):

    form = SISocialInquiry()
    person_id = RegPerson.objects.filter(id=id, is_void=False)

    child = person_id.values()[0]

    try:

        context = {
            'form': form,
            'child': child
        }

        return render(request, 'stat_inst/social_inquiry.html', context)

    except Exception as e:
        raise e


def si_releaseform(request, id):

    form = SIReleaseForm()
    try:

        context = {
            'form': form
        }
        return render(request, 'stat_inst/release_form.html', context)

    except Exception as e:
        raise e


def si_childprofile(request, id):

    form = SIChildProfile()
    try:

        context = {
            'form': form
        }
        return render(request, 'stat_inst/change_in_profile.html', context)

    except Exception as e:
        raise e


def SI_child_view(request, id):
    """ Child View"""
    try:
        person_id = RegPerson.objects.filter(id=id, is_void=False)
        placement = OVCPlacement.objects.filter(
            person_id=id, is_void=False, is_active=True).first()
        unit_type = None
        unit_name = 'Not placed'
        if placement:
            org_unit_id = placement.residential_institution_id
            org_unit = RegOrgUnit.objects.get(id=org_unit_id)
            unit_type = org_unit.org_unit_type_id
            unit_name = org_unit.org_unit_name
        unit_type = 'XXXX'
        child = person_id.values()[0]
        context = {'child': child, 'placement': placement,
                   'unit_type': unit_type, 'unit_name': unit_name}
        return render(request, 'stat_inst/view_child.html', context)

    except Exception as e:
        raise e


@login_required
def si_forms(request, form_id, id):

    try:
        person_id = int(id)
        form = SIForm(form_id)
        form_data = get_form(form_id)
        form_name = form_data['form_name']
        f_code = form_data['form_code']
        form_code = f_code if f_code else form_id
        if request.method == 'POST':
            save_form(request, form_id, id)
            url = reverse(SI_child_view, kwargs={'id': id})
            msg = 'SI Form (%s) details saved successfully' % form_name
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(url)
        check_fields = ['sex_id']
        vals = get_dict(field_name=check_fields)
        case = CaseObj()
        person = RegPerson.objects.get(id=id, is_void=False)
        vacancies = SI_VacancyApp.objects.filter(person_id=id)
        events = SIEvents.objects.filter(
            person_id=person_id, is_void=False, form_id=form_id)
        cases = OVCCaseRecord.objects.filter(
            person_id=person_id, is_void=False)
        case.person = person
        case.vacancies = vacancies
        case.events = events
        case.cases = cases
        org_types = ['TNRR', 'TNAP']
        orgs = RegOrgUnit.objects.filter(
            org_unit_type_id__in=org_types,
            is_void=False).order_by('org_unit_type_id')
        # tmpls = ['FMSI001F', 'FMSI024F']
        # tmpl = form_id if form_id in tmpls else 'FMSI000F'
        tmpl = '%s.html' % form_id
        context = {'form': form, 'case': case, 'vals': vals,
                   'form_id': form_id, 'form_name': form_name,
                   'edit_form': 1, 'orgs': orgs, 'form_code': form_code}
        return render(request, 'si/%s' % tmpl, context)

    except Exception as e:
        raise e


def si_forms_edit(request, form_id, id, ev_id):
    try:
        person_id = int(id)
        idata = get_event_data(form_id, ev_id)
        form = SIForm(form_id, data=idata)
        form_data = get_form(form_id)
        form_name = form_data['form_name'] if 'form_name' in form_data else ''
        if request.method == 'POST':
            save_form(request, form_id, id, 2)
            url = reverse(SI_child_view, kwargs={'id': id})
            msg = 'SI Form (%s) details saved successfully' % form_name
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(url)
        check_fields = ['sex_id']
        vals = get_dict(field_name=check_fields)
        case = CaseObj()
        person = RegPerson.objects.get(id=id, is_void=False)
        vacancies = SI_VacancyApp.objects.filter(person_id=id, is_void=False)
        placement = OVCPlacement.objects.filter(
            person_id=id, is_void=False, is_active=True).first()
        events = SIEvents.objects.filter(
            person_id=person_id, is_void=False, form_id=form_id)
        cases = OVCCaseRecord.objects.filter(
            person_id=person_id, is_void=False)
        case.person = person
        case.vacancies = vacancies
        case.events = events
        case.placement = placement
        case.cases = cases
        case.event_id = ev_id
        tmpl = '%s.html' % form_id
        context = {'form': form, 'case': case, 'vals': vals,
                   'form_id': form_id, 'form_name': form_name,
                   'edit_form': 0, 'event_id': ev_id, 'status': 1}
        return render(request, 'si/%s' % tmpl, context)

    except Exception as e:
        raise e


def si_forms_delete(request):
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
    except Exception as e:
        response = {"deleted": 0,
                    "message": "Error deleting record %s" % (str(e))}
        return JsonResponse(
            response, content_type='application/json', safe=False)
    else:
        return JsonResponse(
            response, content_type='application/json', safe=False)


def si_forms_action(request):
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


def si_test(request):
    """Method to Test"""
    try:
        form = AFCForm2A()
        for f in form:
            print(f.choices)
        response = []
    except Exception as e:
        raise e
    else:
        return JsonResponse(
            response, content_type='application/json', safe=False)
