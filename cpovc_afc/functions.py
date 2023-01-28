from django.shortcuts import get_object_or_404
from django.utils import timezone

from cpovc_main.functions import convert_date
from .models import AFCMain, AFCForms, AFCEvents, AFCInfo
from cpovc_main.models import SetupGeography
from cpovc_ovc.models import OVCEducation
from cpovc_main.functions import get_dict

from cpovc_forms.models import OVCCaseRecord


def handle_alt_care(request, action, params={}):
    """Method to handle Alt Care"""
    try:
        if action == 0:
            care_id = save_alt_care(request, params)
        else:
            # This is to handle edits / deletion
            care_id = params['care_id']
            case = get_object_or_404(AFCMain, care_id=care_id)
            if case:
                # Void this record and delete case_info data
                care_id = case.pk
                case.is_void = True
                case.save(update_fields=["is_void"])
    except Exception as e:
        print('Error saving AFC %s' % (str(e)))
    else:
        return care_id


def get_alt_care(request, case_id, q=0):
    """Method to get Alt Care case."""
    try:
        if q == 1:
            case = AFCMain.objects.get(care_id=case_id, is_void=False)
        else:
            case = AFCMain.objects.get(case_id=case_id, is_void=False)
    except Exception:
        return False
    else:
        return case


def get_crs(request, case_id):
    """Method to get Alt Care case."""
    try:
        case = OVCCaseRecord.objects.get(case_id=case_id, is_void=False)
    except Exception:
        return False
    else:
        return case


def save_care(request, case_id, event_date, care_type, person_id, oid=0):
    """Method to get Alt Care case."""
    try:
        # Org unit and user
        ou_id = request.session.get('ou_primary', 0)
        org_unit_id = 1 if not ou_id else ou_id
        if oid:
            org_unit_id = oid
        user_id = request.user.id
        obj, created = AFCMain.objects.update_or_create(
            case_id=case_id, is_void=False,
            defaults={'case_date': event_date, 'care_type': care_type,
                      'person_id': person_id, 'org_unit_id': org_unit_id,
                      'created_by_id': user_id},
        )
    except Exception as e:
        print('Error saving care - %s' % str(e))
        return False
    else:
        return obj


def save_alt_care(request, params):
    """Method to save Main case data."""
    try:
        case_id = params['case_id']
        person_id = params['person_id']
        case_date = request.POST.get('case_date')
        care_type = request.POST.get('care_option')
        care_sub_type = request.POST.get('care_sub_option', None)
        event_date = convert_date(case_date)
        # save details
        obj = save_care(
            request, case_id, event_date, care_type, person_id)
        if care_sub_type:
            obj.care_sub_type = care_sub_type
            obj.save()
        # Save other common fields
        care_id = obj.pk
        person_id = obj.person_id
        ndatas = save_form_info(request, care_id, person_id, fm_pref='AFC_FM')
        # Get original info for deleting diff changes
        odatas = get_form_info(request, care_id, person_id, False)
        old_ids = []
        for ndt in ndatas:
            if ndt in odatas:
                odts = odatas[ndt]
                ndts = ndatas[ndt]
                for dv in odts:
                    if dv in ndts:
                        ndts.remove(dv)
                    else:
                        old_ids.append({dv: ndt})
        # print('old_ids', old_ids)
        for itms in old_ids:
            for item_value in itms:
                item_id = itms[item_value]
                AFCInfo.objects.filter(care_id=care_id,
                                       person_id=person_id,
                                       item_id=item_id,
                                       item_value=item_value).delete()
    except Exception as e:
        print('Error saving AFC %s' % (str(e)))
    else:
        return obj.care_id


def save_altcare_form(request, form_id, ev_id=0):
    """Method to save forms."""
    try:
        response = True
        case_id = request.POST.get('case_id')
        care_id = request.POST.get('care_id')
        person_id = request.POST.get('person_id')
        event_date = request.POST.get('event_date')
        lid = get_last_form(request, form_id, care_id, person_id)
        print('Last ID', lid)
        # Default to existing care
        response = care_id
        if case_id == care_id:
            print('Form Zero has not been filled')
            print('Request', request.POST)
            care_date = '1900-01-01'
            care_type = None
            obj = save_care(
                request, case_id, care_date, care_type, person_id)
            care_id = obj.pk
            response = care_id
        # if form_id in ['6A']:
        ev_count = ev_id if ev_id > 0 else lid
        user_id = request.user.id
        print('CID,FID,CAID,EV', case_id, form_id, care_id, ev_count)
        obj, created = AFCEvents.objects.update_or_create(
            case_id=case_id, form_id=form_id, care_id=care_id,
            event_count=ev_count,
            defaults={'event_date': convert_date(event_date),
                      'person_id': person_id, 'created_by_id': user_id})
        event_id = obj.pk
        # Schoool details in some forms
        ecare = get_alt_care(request, case_id)
        if form_id == '1A':
            school_level = request.POST.get('school_level')
            # Save School details
            if school_level and school_level != 'SLNS':
                school_class = request.POST.get('school_class')
                school_id = request.POST.get('school')
                admin_type = request.POST.get('admission_type')
                obj, created = OVCEducation.objects.update_or_create(
                    person_id=person_id, is_void=False,
                    defaults={'school_id': school_id,
                              'school_level': school_level,
                              'school_class': school_class,
                              'admission_type': admin_type, 'is_void': False},
                )
            # Update main table
            if ecare:
                ecare.school_level = school_level
                ecare.save(update_fields=["school_level"])
        save_form_data(request, form_id, event_id)
        pref = 'qf%s' % (form_id)
        extract_params(request, pref)
    except Exception as e:
        print('Error saving form - %s' % (str(e)))
        return False
    else:
        return response


def get_last_form(request, form_id, care_id, person_id):
    """Method to get the last form."""
    try:
        last_form = AFCEvents.objects.filter(
            form_id=form_id, care_id=care_id,
            person_id=person_id).latest('event_count').event_count
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
                # print('itm', itms, itm)
                # itdm = 'QTXT' if itms.endswith('_txt') else itm
                # itdl = itm if itms.endswith('_txt') else None
                itdm, itdl = get_field_type(itm, itms)
                # print('itm after', itms, itm, itdl)
                obj, created = AFCForms.objects.update_or_create(
                    event_id=event_id, question_id=itms,
                    defaults={'item_value': itdm, 'item_detail': itdl},
                )
    except Exception as e:
        print('Error saving TIP %s' % (str(e)))
    else:
        return True


def save_form_info(request, care_id, person_id, fm_pref='AFC_FM'):
    """Method to save form common elements."""
    try:
        all_itms = extract_params(request, fm_pref)
        print('all_itms', all_itms)
        now = timezone.now()
        for itms in all_itms:
            for itm in all_itms[itms]:
                # itdm = 'QTXT' if itms.endswith('_txt') else itm
                # itdl = itm if itms.endswith('_txt') else None
                itdm, itdl = get_field_type(itm, itms)
                obj, created = AFCInfo.objects.update_or_create(
                    care_id=care_id, person_id=person_id,
                    item_id=itms, item_value=itdm,
                    defaults={'item_detail': itdl, 'is_void': False,
                              'timestamp_modified': now},
                )
    except Exception as e:
        print('Save info error - %s' % (str(e)))
        return {}
    else:
        return all_itms


def get_form_info(request, care_id, person_id, raw=True, infos=[]):
    """Method to get form infos."""
    try:
        fdatas = {}
        form_infos = AFCInfo.objects.filter(
            care_id=care_id, person_id=person_id)
        for fm in form_infos:
            item_id = fm.item_id
            item_value = fm.item_value
            if item_id not in fdatas:
                fdatas[item_id] = [item_value]
            else:
                fdatas[item_id].append(item_value)
    except Exception as e:
        raise e
    else:
        if raw:
            return form_infos
        else:
            return fdatas


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
        print('params', params)
    except Exception as e:
        print('Error extracting params - %s' % (e))
        return []
    else:
        return params


def get_area(area_id):
    """Get area name from id."""
    try:
        area = SetupGeography.objects.get(area_id=area_id)
    except Exception:
        return 'N/A'
    else:
        return area.area_name


def get_education(person_id):
    """Get area name from id."""
    try:
        ed = OVCEducation.objects.get(person_id=person_id, is_void=False)
    except Exception:
        return None
    else:
        return ed


def get_class_levels():
    """Method to get all class levels."""
    try:
        # Class levels
        vals = get_dict(field_name=['class_level_id'])
        levels, nlevels = {}, {}
        levels["SLNS"] = []
        nlevels["SLNS"] = []
        levels["SLEC"] = ["BABY,Baby Class", "MIDC,Middle Class",
                          "PREU,Pre-Unit"]
        levels["SLPR"] = ["CLS1,Class 1", "CLS2,Class 2", "CLS3,Class 3",
                          "CLS4,Class 4", "CLS5,Class 5", "CLS6,Class 6",
                          "CLS7,Class 7", "CLS8,Class 8"]
        levels["SLSE"] = ["FOM1,Form 1", "FOM2,Form 2", "FOM3,Form 3",
                          "FOM4,Form 4", "FOM5,Form 5", "FOM6,Form 6"]
        levels["SLUN"] = ["YER1,Year 1", "YER2,Year 2", "YER3,Year 3",
                          "YER4,Year 4", "YER5,Year 5", "YER6,Year 6"]
        levels["SLTV"] = ["TVC1,Year 1", "TVC2,Year 2", "TVC3,Year 3",
                          "TVC4,Year 4", "TVC5,Year 5"]
        for level in levels:
            for lvl in levels[level]:
                c_lvl, c_nm = lvl.split(",")
                new_cnm = vals[c_lvl] if c_lvl in vals else c_nm
                n_lvl = str("%s,%s" % (c_lvl, new_cnm))
                # print(lvl, n_lvl)
                if level not in nlevels:
                    nlevels[level] = [n_lvl]
                else:
                    nlevels[level].append(n_lvl)
    except Exception as e:
        print('Error getting class levels - %s' % (str(e)))
        return {}
    else:
        return nlevels


def get_field_type(itm, itms):
    """Get area name from id."""
    try:
        itdm, itdl = 'QTXT', itm
        if itms.endswith('_rdo'):
            itdm, itdl = itm, None
        if itms.endswith('_sdd'):
            itdm, itdl = itm, None
        if itms.endswith('_msc'):
            itdm, itdl = itm, None
    except Exception:
        return itm, None
    else:
        return itdm, itdl
