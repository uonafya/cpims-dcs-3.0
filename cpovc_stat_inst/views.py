from datetime import datetime
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from .forms import (SIAdmission, SICaseReferral, 
SICertificateofExit,SIRemandHomeEscape, SIRecordofVisits,
 SIFamilyConference, SIReleaseForm,SIChildProfile, SIAdmission, SINeedRiskAssessment, SINeedRiskScale, SIVacancyApp, SIVacancyConfirm, SISocialInquiry)

from .models import SI_Admission, SI_NeedRiskAssessment, SI_NeedRiskScale, SI_VacancyApp, SI_SocialInquiry

from .functions import convert_date

from cpovc_main.functions import get_dict
from cpovc_forms.models import OVCCaseCategory
from cpovc_forms.forms import OVCSearchForm
from cpovc_forms.functions import get_person_ids, get_case_info
from cpovc_registry.models import RegPersonsExternalIds
from cpovc_ctip.models import CTIPMain, CTIPEvents, CTIPForms
# from .settings import FMS

# from .functions import save_ctip_form, get_ctip, handle_ctip
from cpovc_forms.models import OVCCaseRecord
from cpovc_registry.models import RegPerson

from cpovc_forms.functions import get_person_ids, get_case_info

# Create your views here.
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
            case_ids[crs.person_id]={'clv': 1, 'cs': crs.case_serial, 'cid': crs.case_id}

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

        return render(request,'stat_inst/home.html',context)
    

    except Exception as e:
        raise e
    

def SI_admissions(request, id):

    person_id = RegPerson.objects.filter(id=id, is_void=False)

    print(dir(request))

    child = person_id.values()[0]

    form = SIAdmission()
    try:
        if(request.method == "POST"):
            data = request.POST

            print(data)
            SI_Admission(
                person_id = data.get('person_id'),
                institution_type = data.get('institution_type'),
                date_of_admission = convert_date(data.get('date_of_admission')),
                current_year_of_school = data.get('current_year_of_school'),
                type_of_entry = data.get('type_of_entry'),
                referral_source = data.get('referral_source'),
                child_category = data.get('child_category'),
                abused_child_desc = data.get('abused_child_desc'),
                referral_source_others = data.get('referral_source_others'),
                referrer_name = data.get('referrer_name'),
                referrer_address = data.get('referrer_address'),
                referrer_phone = data.get('referrer_phone'),
                not_contact_child = data.get('not_contact_child'),
                name_not_contact_child = data.get('name_not_contact_child'),
                relationship_to_child_not_contact_child = data.get('relationship_to_child_not_contact_child'),
                consent_form_signed = data.get('consent_form_signed'),
                commital_court_order = data.get('commital_court_order'),
                school_name = data.get('school_name'),
                health_status = data.get('health_status'),
                special_needs = data.get('special_needs'),
                workforce_id = data.get('workforce_id'),
                audit_date = convert_date(data.get('audit_date'))   
            ).save()

            HttpResponseRedirect(reverse(si_home))
        context = {
            'form': form,
            'child': child
        }
        return render(request,'stat_inst/admission.html',context)
    
    except Exception as e:
        raise e


def SI_childIdentification(request,person_id):
    data = request.POST

    form = SIChildIdentification()
    context = {
            'form': form
        }
    return render(request, 'stat_inst/childIdentification.html', context)

    


def si_casereferral(request):
    data = request.GET

    form = SICaseReferral()
    try:

        context = {
            'form': form
        }

        return render(request,'stat_inst/case_referral.html',context)    
    except Exception as e:
        raise e

def SI_needriskform(request, id):
    data = request.GET
    form = SINeedRiskAssessment()

    try:

        context = {
            'form': form
        }
        return render(request,'stat_inst/needriskform.html',context)
      
        

    except Exception as e:
        raise e

def SI_medicalassesment(request,person_id):
    data = request.POST

    form = MedicalAssesmentForm()
    context = {
            'form': form
        }
    
    return render(request, 'stat_inst/medicalassesmentform.html', context)

    

def si_certificateofexit(request):
    data = request.GET

    form = SICertificateofExit()

    try:

        context = {
            'form': form
        }

        
        return render(request,'stat_inst/certificate_of_exit.html',context)
#       return render(request,'stat_inst/certificate_of_exit.html',context)

    except Exception as e:
        raise e

def SI_individualCarePlan(request,person_id):
    data = request.POST

    form = IndividualCarePlanForm()
    try:

        context = {
            'person_id': person_id,
            'form': form
        }
        return render(request, 'stat_inst/individualtreatmentplan.html', context)

    except Exception as e:
        raise e
        
def SI_LeaveOfAbscence(request,person_id):
    data = request.POST

    form = LeaveOfAbsenceForm()
    try:

        context = {
            'person_id': person_id,
            'form': form
        }
        return render(request, 'stat_inst/leaveofabsenceassesmentform.html', context)

    except Exception as e:
        raise e
        
def SI_RemandHomeEscape(request,person_id):
    data = request.POST

    form = RemandHomeEscapeForm()
    try:

        context = {
            'person_id': person_id,
            'form': form
        }
        return render(request, 'stat_inst/escapeform.html', context)

    except Exception as e:
        raise e

def SI_needriskscale(request, id):
    data = request.GET

    form = SINeedRiskScale()
    return render(request,'stat_inst/needriskscale.html',context)
    

def si_remandhomeescape(request):
    data = request.GET

    form = SIRemandHomeEscape()
    context = {
            'form': form
        }

    return render(request,'stat_inst/remand_home_escape.html',context)  
    
def SI_vacancyapplication(request, id):
    data = request.GET

    form = SIVacancyApp()

    try:

        context = {
            'form': form
        }    

        return render(request,'stat_inst/vacancy_app.html',context)    
    except Exception as e:
        raise e


def si_recordofvisits(request):
    data = request.GET

    form = SIRecordofVisits()
    try:

        context = {
            'form': form
        }
        return render(request,'stat_inst/record_of_visits.html',context)
    
    except Exception as e:
        raise e
    
def si_familyconference(request): 
    data = request.GET

    form = SIFamilyConference()
    context = {
            'form': form
        }

     return render(request,'stat_inst/family_conference.html',context)

def SI_vacancyconfirmation(request, id):
    data = request.GET
    try:
        pass
    except Exception as e:
        raise e
    
def SI_social_inquiry(request, id):
    data = request.GET

    form = SISocialInquiry()

    try:

        context = {
            'form': form
        }

        return render(request,'stat_inst/social_inquiry.html',context)
    
    except Exception as e:
        raise e

def si_releaseform(request): 
    data = request.GET

    form = SIReleaseForm()
    try:

        context = {
            'form': form
        }
        return render(request,'stat_inst/release_form.html',context)
    
    except Exception as e:
        raise e

def si_childprofile(request): 
    data = request.GET

    form = SIChildProfile()
    try:

        context = {
            'form': form
        }
        return render(request,'stat_inst/change_in_profile.html',context)        
    
    except Exception as e:
        raise e
    

def SI_child_view(request, id):
    data = request.POST
    person_id = RegPerson.objects.filter(id=id, is_void=False)

    child = person_id.values()[0]

    creg = {}
    creg['is_active '] = True

    form = ""
    try:
        if request.method == 'POST':
            pass

        context = {
            'form': form,
            'child': child
        }
        return render(request,'stat_inst/view_child.html',context)
    
    except Exception as e:
        raise e
    
