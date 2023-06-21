from datetime import datetime
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from .forms import (SIAdmission, SICaseReferral, 
SICertificateofExit,SIRemandHomeEscape, SIRecordofVisits, SIFamilyConference)

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
    

def SI_admissions(request, person_id):
    data = request.GET

    form = SIAdmission()
    try:

        context = {
            'form': form
        }
        return render(request,'stat_inst/admission.html',context)
    
    except Exception as e:
        raise e
    

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
    
def si_certificateofexit(request):
    data = request.GET

    form = SICertificateofExit()
    try:

        context = {
            'form': form
        }
        return render(request,'stat_inst/certificate_of_exit.html',context)
    
    except Exception as e:
        raise e

def si_remandhomeescape(request):
    data = request.GET

    form = SIRemandHomeEscape()
    try:

        context = {
            'form': form
        }
        return render(request,'stat_inst/remand_home_escape.html',context)
    
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
    try:

        context = {
            'form': form
        }
        return render(request,'stat_inst/family_conference.html',context)
    
    except Exception as e:
        raise e
    