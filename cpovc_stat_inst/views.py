from datetime import datetime
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
import uuid

from django.utils import timezone

from cpovc_auth.models import AppUser

from .forms import (SIAdmission, SICaseReferral, RemandHomeEscape,MedicalAssesmentForm,
SICertificateofExit, SIRecordofVisits,IndividualCarePlanForm,
SIFamilyConference, SIReleaseForm,SIChildProfile, SIAdmission, 
SINeedRiskAssessment, SINeedRiskScale, SIVacancyApp, SIVacancyConfirm, SISocialInquiry, LeaveOfAbsenceForm, 
childPlacement)

from .forms import (
    SI_INSTITUTION,
    APP_STATUS,
    DOCUMENT_CHOICES_CASE_REFERRAL,
    REASON_CHOICES_CASE_REFERRAL,

)

from .models import (SI_Admission, 
                     SI_NeedRiskAssessment, 
                     SI_NeedRiskScale, 
                     SI_VacancyApp, 
                     SI_SocialInquiry,
                     SI_Referral,
                     SI_Release,
                     )

from .functions import convert_date, convertYesNo, get_si_reg_list


from cpovc_main.functions import get_dict
from cpovc_forms.models import OVCCaseCategory
from cpovc_forms.forms import OVCSearchForm
from cpovc_forms.functions import get_person_ids, get_case_info
from cpovc_registry.models import RegPersonsExternalIds, RegOrgUnit
# from .settings import FMS

# from .functions import save_ctip_form, get_ctip, handle_ctip
from cpovc_forms.models import OVCCaseRecord
from cpovc_registry.models import RegPerson

# Create your views here.

# Get organisation units linked to an SI type
@login_required
def si_look(request):
    data = request.POST
    si_type = data.get('si_type')

    si_lists = RegOrgUnit.objects.filter(is_void=False, org_unit_type_id=si_type)
    print(si_lists)
    context = {
        "centres": 
            [
                ['default_option,Please Select'],
            ]
        
    }
    for si_list in si_lists:
        context['centres'].append([f'{si_list.org_unit_id_vis},{si_list.org_unit_name}'])
    
    print(context)

    return JsonResponse(context, content_type='application/json',
                                safe=False)

# Get organisation units linked to an SI type
@login_required
def SI_vacancyDetail(request):
    data = request.POST
    uid = request.POST.get('vacancyId')

    vacancy = SI_VacancyApp.objects.filter(is_void=False, vacancy=uid)
    context=vacancy.values()[0]

    return JsonResponse(context, content_type='application/json',
                                safe=False)
@login_required
def SI_deny_vacancy(request, uid):
    person_id = ""
    try:
        del_vanc = SI_VacancyApp.objects.get(is_void=False, vacancy=uid)
        print(dir(del_vanc))
        del_vanc.application_status='D'
        del_vanc.date_of_approved=timezone.now()
        del_vanc.save()
        person_id = del_vanc.person_id

        msg = f'Application  {del_vanc.ref_no } denial successful'
        messages.add_message(request, messages.SUCCESS, msg)

    except Exception as e:
        err= f'Could not deny: {e}'

        msg = 'Follow-up error - (%s). %s.' % (str(e), err)
        print(msg)
        messages.add_message(request, messages.ERROR, msg)

    return HttpResponseRedirect(reverse('new_si_child_view', args=(person_id,))) # person_id)

@login_required
def SI_delete_vacancy(request, uid):
    person_id = ""
    try:
        del_vanc = SI_VacancyApp.objects.get(is_void=False, vacancy=uid)
        print(dir(del_vanc))
        del_vanc.is_void=True
        del_vanc.updated_at=timezone.now()
        del_vanc.save()
        person_id = del_vanc.person_id

        msg = f'Application  {del_vanc.ref_no } deleted successfully'
        messages.add_message(request, messages.SUCCESS, msg)

    except Exception as e:
        err= f'Could not Delete: {e}'

        msg = 'Follow-up error - (%s). %s.' % (str(e), err)
        print(msg)
        messages.add_message(request, messages.ERROR, msg)

    return HttpResponseRedirect(reverse('new_si_child_view', args=(person_id,))) # person_id)

@login_required
def SI_vacancyApprove(request):
    data = request.POST
    uid = request.POST.get('vacancyId')
    try:
        vacancy = SI_VacancyApp.objects.get(is_void=False, vacancy=uid)
        vacancy.cci_placed = request.POST.get('siname')
        vacancy.months_approved = request.POST.get('months')
        vacancy.magistrate_court = request.POST.get('magistrate_court')
        vacancy.application_status='A'
        vacancy.save()
        context={
            "message":"Data saved successfully"
        }

    except Exception as e:
        print(e)
        msgs = f'Data didnt save : {e}'
        context={
            "message":msgs
        }


        msg = f'Data didnt save {e}'
        messages.add_message(request, messages.ERROR, msg)

    return JsonResponse(context, content_type='application/json',
                                safe=False)

def si_home(request):

    try:
        form = OVCSearchForm(data=request.GET)
        print(f'forms {form}')
        search_string = request.GET.get('search_name')
        pids = get_person_ids(request, search_string)

        ctip_ids, inst_name = {}, {}
        cases = RegPerson.objects.filter(is_void=False, id__in=pids)


        # Get children already in institutions
        crss = SI_Admission.objects.filter(is_void=False, person_id__in=pids)
        for crs in crss:
            inst_name[crs.person_id]={'clv': 1, 'cs': crs.institution_type, 'cid': crs.institution_name}

        for case in cases:
            pid = case.id
            cdt = dict(SI_INSTITUTION)[inst_name[pid]['cs']] if pid in inst_name else 'Not Enrolled'
            csn = inst_name[pid]['cid'] if pid in inst_name else 'Not Enrolled'

            setattr(case, 'inst_type', cdt)
            setattr(case, 'inst_name', csn)
        
        apps = SI_VacancyApp.objects.filter(is_void=False, person_id__in=pids, application_status='W')
        for app in apps:
            ctip_ids[app.person_id]={'clv': 1, 'cs': app.application_status, 'cid': app.ref_no}

        for case in cases:
            pid = case.id
            cdt = ctip_ids[pid]['cs'] if pid in ctip_ids  else 'Not Enrolled'
            csn = 'Application Pending Approval' if pid in ctip_ids  else 'Application pending approval'

            setattr(case, 'inst_type', cdt)
            setattr(case, 'inst_name', csn)
        
        # print(cases)
        context = {
            'status': 200,
            'cases': cases,
            'form': form
        }
        face  = get_si_reg_list(['TNGP'])
        # print(f' output {face}')
        return render(request,'stat_inst/home.html',context)
    

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
                person_id = id,
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
                not_contact_child = convertYesNo(data.get('not_contact_child')),
                name_not_contact_child = data.get('name_not_contact_child'),
                relationship_to_child_not_contact_child = data.get('relationship_to_child_not_contact_child'),
                consent_form_signed = convertYesNo(data.get('consent_form_signed')),
                commital_court_order = convertYesNo(data.get('commital_court_order')),
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

    
# Case referral logic
def si_casereferral(request, id):
    data = request.GET
    person_id = RegPerson.objects.filter(id=id, is_void=False)

    person = RegPerson.objects.get(id=id, is_void=False)
    user_id = request.user.id
    current_user = AppUser.objects.get(reg_person=user_id, is_active=True)
    child = person_id.values()[0]

    applications = SI_Referral.objects.filter(is_void=False, person_id = id)
    referrals = applications.values()

    dict_reasons = dict(REASON_CHOICES_CASE_REFERRAL)
    dict_documents = dict(DOCUMENT_CHOICES_CASE_REFERRAL)
    # breakpoint()
    for one_ref in referrals:
        one_ref['reason_for_referral_s'] = dict_reasons[one_ref.get('reason_for_referral')]
        one_ref['documents_attached_s'] = dict_documents[one_ref.get('documents_attached')]
    
    print(request)
    admission = {
        'institution_name': "Wamumu Children home"
    }

    form = SICaseReferral()
    try:
        if request.method == 'POST':
            data = request.POST

            SI_Referral(
                person = person,
                user = current_user,    
                ref_no = data.get('ref_no'),
                refferal_to = data.get('refferal_to'),
                reason_for_referral =  data.get('reason_for_referral'),
                reason_for_referral_others =  data.get('reason_for_referral_others'),
                documents_attached = data.get('documents_attached') 
            ).save()

            msg = f'Case referral  {data.get("ref_no")} saved successful'
            messages.add_message(request, messages.SUCCESS, msg)

            return HttpResponseRedirect(reverse('new_si_child_view', args=(id,))) # person_id)



        context = {
            'form': form,
            'child': child,
            "admission": admission,
            "referrals": referrals
        }

        return render(request,'stat_inst/case_referral.html',context)    
    except Exception as e:
        raise e
    
@login_required
def si_casereferral_completed(request, id):
    person_id = ""
    try:
        update_vac = SI_Referral.objects.get(is_void=False, id=id)
        update_vac.ref_completed=True
        update_vac.updated_at=timezone.now()
        update_vac.save()
        person_id = update_vac.person_id
        print(update_vac)

        msg = f'Referral  {update_vac.ref_no } marked as completed'
        messages.add_message(request, messages.SUCCESS, msg)

    except Exception as e:
        err= f'Could not Mark as successful: {e}'

        msg = 'Follow-up error - (%s). %s.' % (str(e), err)
        print(msg)
        messages.add_message(request, messages.ERROR, msg)  

    return HttpResponseRedirect(reverse('SI_casereferral', args=(person_id,))) # person_id)


def SI_needriskform(request, id):
    data = request.GET
    form = SINeedRiskAssessment()
    person_id = RegPerson.objects.filter(id=id, is_void=False)

    child = person_id.values()[0]

    try:

        context = {
            'form': form,
            'child': child
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

    

def si_certificateofexit(request, id):
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

def SI_individualCarePlan(request,id):
    data = request.POST

    form = IndividualCarePlanForm()

    person_id = RegPerson.objects.filter(id=id, is_void=False)

    child = person_id.values()[0]
    try:

        context = {
            'id': id,
            'form': form,
            "child": child
        }
        return render(request, 'stat_inst/individualtreatmentplan.html', context)

    except Exception as e:
        raise e
        
def SI_LeaveOfAbscence(request,id):
    data = request.POST

    form = LeaveOfAbsenceForm()
    try:

        context = {
            'id': id,
            'form': form
        }
        return render(request, 'stat_inst/leaveofabsenceassesmentform.html', context)

    except Exception as e:
        raise e
        
def SI_RemandHomeEscape(request,id):
    data = request.POST

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
    data = request.GET
    form = SINeedRiskScale()
    context = {
        "form": form
    }

    return render(request,'stat_inst/needriskscale.html',context)
    

def si_remandhomeescape(request, id):
    data = request.GET

    form = RemandHomeEscape()
    context = {
            'form': form
        }

    return render(request,'stat_inst/remand_home_escape.html',context)  
    
def SI_vacancyapplication(request, id):
    try:
        person_In = RegPerson.objects.get(id=id, is_void=False)  # Get Instance
            

        if(request.method == 'POST'):
            data = request.POST
            print(data)
            SI_VacancyApp(
                vacancy = uuid.uuid1(),
                person = person_In,
                ref_no = data.get('ref_no'),
                date_of_application = convert_date(data.get('date_of_application')),
                crc_no = data.get('crc_no'),
                pnc_no = data.get('pnc_no'),
                court_number = data.get('court_number'),
                judge_name = data.get('judge_name'),
                child_held_at = data.get('child_held_at'),
                date_of_next_mention = convert_date(data.get('date_of_next_mention')),
                requesting_officer = data.get('requesting_officer'),
                designation = data.get('designation'),
                sub_county_children_officer = data.get('sub_county_children_officer')
            ).save()
            
            msg = f'Application  {data.get("ref_no")} saved successful'
            messages.add_message(request, messages.SUCCESS, msg)

            return HttpResponseRedirect(reverse('new_si_child_view', args=(id,))) # person_id)
        form = SIVacancyApp()
        applications = SI_VacancyApp.objects.filter(is_void=False, person_id = id)
        vacancy = applications.values()
        child = {
            "first_name": person_In.first_name,
            "other_names": person_In.other_names,
            "surname": person_In.surname,
            "id": id,
            "age": person_In.age,
            "sex_id": person_In.sex_id
        }
    
        print(type(vacancy))
        context = {
            "form": form,
            "child": child,
            "vacancies": vacancy            
        }    

        return render(request,'stat_inst/vacancy_app.html',context)    
    except Exception as e:
            raise e


def si_recordofvisits(request, id):
    data = request.GET

    form = SIRecordofVisits()
    try:

        context = {
            'form': form
        }
        return render(request,'stat_inst/record_of_visits.html',context)
    
    except Exception as e:
        raise e
    
def si_familyconference(request, id): 
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
    person_id = RegPerson.objects.filter(id=id, is_void=False)

    child = person_id.values()[0]

    try:

        context = {
            'form': form, 
            'child': child
        }

        return render(request,'stat_inst/social_inquiry.html',context)
    
    except Exception as e:
        raise e

def si_releaseform(request, id): 
    data = request.GET
    person_id = RegPerson.objects.filter(id=id, is_void=False)
    child = person_id.values()[0]


    form = SIReleaseForm()
    try:
        person_In = RegPerson.objects.get(id=id, is_void=False)  # Get Instance
        if request.method == 'POST':
            active_User = AppUser.objects.get(id=request.user.id)
            data = request.POST
            
            SI_Release(
                person = person_In,
                ref_no = data.get('ref_no'),
                date_released = convert_date(data.get('date_released')),
                name = data.get('name'),
                id_no = data.get('id_no'),
                phone_number = data.get('telephone'),
                occupation = data.get('occupation'),
                residence = data.get('residence'),
                relation_to_child = data.get('relation_to_child'),
                user = active_User
            ).save()

            msg = f'Release  {data.get("ref_no")} saved successful'
            messages.add_message(request, messages.SUCCESS, msg)

            return HttpResponseRedirect(reverse('SI_releaseform', args=(id,))) # person_id)

        child_inst_details = SI_Admission.objects.filter(person_id=id, is_void=False)
        releases = SI_Release.objects.filter(person_id = id, is_void = False)
        if len(releases)>0:
            for release in releases:
                release['institution_name'] = child_inst_details.institution_name
                print(release)
                # breakpoint()
        context = {
            'form': form,
            'child': child,
            'releases': releases
        }
        return render(request,'stat_inst/release_form.html',context)
    
    except Exception as e:
        raise e

def si_childprofile(request, id): 
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


def child_placement(request, id):
    person_id = RegPerson.objects.filter(id=id, is_void=False)

    child = person_id.values()[0]

    creg = {}
    creg['is_active '] = True

    form = childPlacement()
    try:
        if request.method == 'POST':
            child_inst = RegPerson.objects.get(is_void = False, id=id)
            data = request.POST
            active_User = AppUser.objects.get(id=request.user.id)
            SI_Admission(
                person = child_inst,
                institution_type = data.get('institution_type'),
                institution_name = data.get('institution_name'),
                is_placed = True,
                placed_by = active_User,
                place_created_at = timezone.now(),
            ).save()

            msg = f'Placement  successful'
            messages.add_message(request, messages.SUCCESS, msg)

            return HttpResponseRedirect(reverse('new_si_admit', args=(id,))) # person_id)

        context = {
            'form': form,
            'child': child
        }
        return render(request,'stat_inst/placement.html',context)
    
    except Exception as e:
        raise e