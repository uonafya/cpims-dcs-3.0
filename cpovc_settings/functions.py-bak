import uuid
from django.utils import timezone
from django.db.models import Count
from cpovc_forms.models import (
    OVCCaseCategory, OVCCaseGeo, OVCCaseEvents, OVCCaseRecord)
from .models import CaseDuplicates
from cpovc_main.models import SetupGeography


def handle_duplicates(request):
    """Handle duplicates."""
    try:
        results = {}
        results['status'] = 0
        results['message'] = "Successfully marked as duplicates"

        case_ids = request.POST.getlist('case_id[]')
        # print case_ids
        if len(case_ids) <= 1:
            results['status'] = 1
            results['message'] = "You must check two or more records."
            return results
        else:
            params = []
            case_units, cintervens = {}, {}
            children, categories = [], []
            cases = OVCCaseCategory.objects.filter(case_id_id__in=case_ids)
            case_geos = OVCCaseGeo.objects.filter(case_id_id__in=case_ids)
            # Calculations of interventions
            case_intvs = OVCCaseEvents.objects.filter(
                case_id_id__in=case_ids).values(
                'case_id_id').annotate(dcount=Count('case_id_id'))
            # print(case_intvs)
            for case_intv in case_intvs:
                cintervens[case_intv['case_id_id']] = case_intv['dcount']
            for case_geo in case_geos:
                org_unit = case_geo.report_orgunit_id
                case_geo_id = case_geo.case_id_id
                case_units[case_geo_id] = org_unit
            for case in cases:
                child_id = case.person_id
                category_id = case.case_category
                case_id = case.case_id_id
                creator_id = case.case_id.created_by
                ou_id = case_units[case_id] if case_id in case_units else None
                intv_cnt = cintervens[case_id] if case_id in cintervens else 0
                params.append({'person_id': child_id, 'case_id': case_id,
                               'category_id': category_id,
                               'creator_id': creator_id,
                               'org_unit': ou_id, 'case_intv': intv_cnt})
                if child_id not in children:
                    children.append(child_id)
                if category_id not in categories:
                    categories.append(category_id)
            print('DUPS', children, categories, case_ids)
            msg = "This can only be duplicates if it is the same"
            if len(children) > 1 or len(categories) > 1:
                results['status'] = 2
                results['message'] = "%s child and same case category." % (msg)
                return results
            else:
                res = save_duplicates(params)
                results['message'] += " %s records" % (res)

            results['message'] += ". Go to duplicates module for more action."
    except Exception as e:
        print("error with deduplication - %s" % (str(e)))
        return {'status': 9, 'message': "Error processing de-duplication"}
    else:
        return results


def save_duplicates(params):
    """Method to save duplicates."""
    try:
        print(params)
        dup_id = uuid.uuid4()
        cnt = 0
        for param in params:
            # print param
            p, created = CaseDuplicates.objects.get_or_create(
                case_id=param['case_id'],
                defaults={'created_by_id': param['creator_id'],
                          'case_category_id': param['category_id'],
                          'organization_unit_id': param['org_unit'],
                          'person_id': param['person_id'],
                          'duplicate_id': dup_id,
                          'interventions': param['case_intv']},
            )
            # print(param['case_id'], created)
            if created:
                cnt += 1
    except Exception as e:
        raise e
    else:
        return cnt


def get_duplicates(request):
    """Method to get duplicates."""
    try:
        duplicates = CaseDuplicates.objects.filter(
            action_id=1).order_by('case_id', '-interventions')
    except Exception as e:
        raise e
    else:
        return duplicates


def remove_duplicates(request):
    """Method to remove duplicates."""
    try:
        cnt = 0
        ret_ids, del_ids = [], []
        msg = "Could not delete case as this has more Interventions."
        results = {'status': 9, 'message': msg}
        case_id = request.POST.get('case_id')
        duplicate_id = request.POST.get('duplicate_id')
        user_id = int(request.user.id)
        print(user_id, duplicate_id, case_id)
        duplicates = CaseDuplicates.objects.filter(
            duplicate_id=duplicate_id).order_by('-interventions')
        for dups in duplicates:
            cnt += 1
            sys_case_id = str(dups.case_id)
            if cnt == 1:
                '''
                dups.updated_by_id = user_id
                dups.action_id = 2
                dups.updated_at = timezone.now()
                dups.save()
                '''
                ret_ids.append(sys_case_id)
            if cnt > 1 and sys_case_id == case_id:
                del_ids.append(sys_case_id)
                results['status'] = 0
                results['message'] = "Successfully Deleted record."
            print(str(sys_case_id), duplicate_id, user_id)
        if ret_ids and del_ids:
            CaseDuplicates.objects.filter(
                case_id__in=ret_ids).update(
                updated_by_id=user_id, action_id=2, updated_at=timezone.now())
            # Remove other records and void case record
            CaseDuplicates.objects.filter(
                case_id__in=del_ids).update(
                updated_by_id=user_id, action_id=3, updated_at=timezone.now())
            # Void other records
            OVCCaseRecord.objects.filter(
                case_id__in=del_ids).update(is_void=False)
            OVCCaseCategory.objects.filter(
                case_id_id__in=del_ids).update(is_void=False)
            OVCCaseGeo.objects.filter(
                case_id_id__in=del_ids).update(is_void=False)
    except Exception as e:
        print('error - %s' % str(e))
        raise e
    else:
        return results


def get_geo(area_code):
    """Method to get area geo"""
    try:
        # acode = area_code.zfill(3)
        acode = str(int(area_code))
        res = SetupGeography.objects.get(area_code=acode)
    except Exception:
        return None
    else:
        return res.area_name
