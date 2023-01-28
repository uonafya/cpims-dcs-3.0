import base64
import pandas as pd
from django.utils import timezone
from django.forms.models import model_to_dict
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image)
from cpovc_reports.functions import get_styles, get_header, draw_page, Canvas
from cpovc_forms.functions import validate_serialnumber
from reportlab.lib import colors
from .models import NOTTTravel, NOTTChaperon, NOTTChild
from .vurugu import save_vm_changes
from cpovc_forms.models import (
    OVCBasicPerson, OVCCaseRecord, OVCCaseCategory, OVCCaseSubCategory,
    OVCCaseGeo, OVCReferral, OVCEconomicStatus, OVCFamilyStatus,
    OVCHobbies, OVCFriends, OvcCasePersons, OVCMedical,
    OVCMedicalSubconditions, OVCNeeds, FormsLog)
from cpovc_registry.models import (
    RegPerson, RegPersonsTypes, RegPersonsSiblings, RegOrgUnit,
    RegPersonsGuardians, RegPersonsGeo, RegPersonsOrgUnits)
from cpovc_main.models import SetupGeography
from cpovc_main.functions import new_guid_32

from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from cpovc_reports.documents import (
    logo_path, checked_image_path, unchecked_image_path)


def get_travel(request, travel_id=0, params={}):
    """Method to get travels."""
    try:
        if travel_id > 0:
            travel = NOTTTravel.objects.get(pk=travel_id)
        else:
            travel = NOTTTravel.objects.filter(pk=travel_id)
    except Exception as e:
        raise e
    else:
        return travel


def get_travel_details(request, element, travel):
    """Method to get travel details."""
    try:
        data = [['Travel Details', '']]
        travel_id = travel.id
        summary = 'Applied (%s), ' % (travel.no_applied)
        summary += 'Cleared (%s), ' % (travel.no_cleared)
        summary += 'Returned (%s)' % (travel.no_returned)
        tdate = travel.travel_date
        rdate = travel.return_date
        data.append(['Institution Name', travel.institution_name])
        data.append(['Country of Travel', travel.country_name])
        data.append(['Date of Travel', tdate.strftime("%d-%B-%Y")])
        data.append(['Date of Return', rdate.strftime("%d-%B-%Y")])
        data.append(['Reason of Travel', travel.reason])
        data.append(['Summary of Children Traveling', summary])
        data.append(['Sponsor', travel.sponsor])
        df = pd.DataFrame.from_records(data)
        print(df)
        # dt_size = len(df.index)
        # col_size = len(df.columns)
        # ds = dt_size + 2
        style = TableStyle(
            [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
             ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
             ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
             # ('ALIGN', (1, 3), (-1, -1), 'RIGHT'),
             ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
             ('BACKGROUND', (0, 0), (-1, 0), '#89CFF0')])
        d0 = 27.86 - 11.0
        cols = (11.0 * cm, d0 * cm)
        t1 = Table(data, colWidths=cols)
        t1.setStyle(style)
        element.append(t1)
        element.append(Spacer(0.1 * cm, .8 * cm))
        # Chaperons
        style = TableStyle(
            [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
             ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
             ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
             ('FONTNAME', (0, 0), (3, 1), 'Helvetica-Bold'),
             ('BACKGROUND', (0, 0), (-1, 0), '#89CFF0')])
        cnt = 0
        chaps = [['', 'Chaperons', '', ''],
                 ['#', 'Names', 'Sex', 'Passport Number']]
        chaperons = NOTTChaperon.objects.filter(travel_id=travel_id)
        for chap in chaperons:
            cnt += 1
            first_name = chap.other_person.person_first_name
            surname = chap.other_person.person_surname
            other_names = chap.other_person.person_other_names
            sex_id = chap.other_person.person_sex
            passport_no = chap.other_person.person_identifier
            names = '%s %s %s' % (first_name, surname, other_names)
            sex = 'Male' if sex_id == 'SMAL' else 'Female'
            chaps.append([str(cnt), names, sex, passport_no])
        t2 = Table(chaps, colWidths=(1.0 * cm, 10.0 * cm, 7 * cm, 9.86 * cm))
        t2.setStyle(style)
        element.append(t2)
        element.append(Spacer(0.1 * cm, .8 * cm))
        # Children
        style = TableStyle(
            [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
             ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
             ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
             ('FONTNAME', (0, 0), (5, 1), 'Helvetica-Bold'),
             ('BACKGROUND', (0, 0), (-1, 0), '#89CFF0')])
        chnt = 0
        ctitle = ['#', 'Names', 'Sex', 'Passport Number',
                  'Cleared', 'Returned']
        childls = [['', 'Children', '', '', '', ''], ctitle]
        children = NOTTChild.objects.filter(travel_id=travel_id)
        for child in children:
            chnt += 1
            first_name = child.person.first_name
            surname = child.person.surname
            other_names = child.person.other_names
            sex_id = child.person.sex_id
            passport_no = child.passport
            cleared = child.cleared
            returned = child.returned
            tcl = 'Yes' if cleared else 'No'
            tret = 'Yes' if returned else 'No'
            names = '%s %s %s' % (first_name, surname, other_names)
            sex = 'Male' if sex_id == 'SMAL' else 'Female'
            cdetails = [str(chnt), names, sex, passport_no, tcl, tret]
            childls.append(cdetails)
        ccol = (1.0 * cm, 10.0 * cm, 7 * cm, 5.86 * cm, 2 * cm, 2 * cm)
        t2 = Table(childls, colWidths=ccol)
        t2.setStyle(style)
        element.append(t2)
    except Exception as e:
        raise e
    else:
        pass


def travel_pdf(request, response, file_name):
    """Method to generate pdf."""
    try:
        rid = 5
        fnames = file_name.split('_')
        travel_id = int(fnames[2])
        tid = '{0:05d}'.format(travel_id)
        # Get some parameters
        travel = get_travel(request, travel_id)
        tarehe = travel.travel_date
        report_name = 'SNo. %s - Travel Authorization ' % (tid)
        region = 'National'
        dates = 'Date %s' % (tarehe.strftime("%d, %B %Y"))
        styles = get_styles()
        element = []
        get_header(element, report_name, region, dates, styles)
        # Write the data
        get_travel_details(request, element, travel)
        doc = SimpleDocTemplate(
            response, pagesize=A4, rightMargin=20,
            leftMargin=20, topMargin=30, bottomMargin=36.5,
            keywords="CPIMS, Child Protection in Kenya, UNICEF, DCS, <!NMA!>")
        if rid in [1, 3, 4, 5]:
            doc.pagesize = landscape(A4)
        element.append(Spacer(0.1 * cm, .2 * cm))
        # doc.build(element)
        doc.watermark = 'CPIMS'
        doc.fund_name = ''
        doc.report_info = ''
        doc.source = 'Child Protection Information Management System (CPIMS)'
        doc.build(element, onFirstPage=draw_page, onLaterPages=draw_page,
                  canvasmaker=Canvas)
    except Exception as e:
        raise e
    else:
        pass


def handle_integration(request, case, case_id):
    """Method to handle integrations."""
    try:
        response = {}
        case_status = request.POST.get('case_status')
        case_comments = request.POST.get('case_comments')
        case_org_unit_id = request.POST.get('case_org_unit')
        case_serial = ''
        case_record_id = None
        payload = {}
        if case_status == 'AYES':
            print('Approve Case')
            status_id = 1
            payload["verification_status"] = "002"
            payload["dco_followup1"] = case_comments
            crs = create_crs(request, case, case_id)
            if 'case_serial' in crs:
                case_serial = crs['case_serial']
                case_record_id = case_id
                payload['case_serial'] = case_serial
        else:
            print('Reject Case')
            status_id = 2
            payload["verification_status"] = "003"
            payload["dco_followup1"] = case_comments
        case.status = status_id
        case.case_comments = case_comments
        case.case_serial = case_serial
        case.case_record_id = case_record_id
        case.case_org_unit_id = case_org_unit_id
        flds = ["status", "case_comments", "case_serial",
                "case_record_id", "case_org_unit_id"]
        case.save(update_fields=flds)
        if case.account.username == 'vurugumapper':
            # Send feedback to VM to stop SMS propagation
            response = save_vm_changes(case_id, payload)
    except Exception as e:
        print('error with integration - %s' % (e))
        return {"status": 9}
    else:
        return response


def get_geo(area_code, area_type='GDIS'):
    """Method to get area id."""
    try:
        # print(area_code, area_type)
        geo = SetupGeography.objects.get(
            area_code=area_code, area_type_id=area_type)
    except Exception as e:
        print('error getting geo - %s' % (e))
        return None
    else:
        return geo


def get_person_geo(request):
    """method to get person geos."""
    try:
        county_ids, area_ids = [], []
        person_id = request.user.reg_person.id
        geos = RegPersonsGeo.objects.filter(
            person_id=person_id, is_void=False)
        for geo in geos:
            aid = geo.area_id
            pid = geo.area.parent_area_id
            if aid and aid not in area_ids and aid > 47:
                area_ids.append(aid)
                area_ids.append(str(aid).zfill(3))
            if pid and pid not in county_ids:
                county_ids.append(pid)
                county_ids.append(str(pid).zfill(3))
    except Exception as e:
        print('Error getting area_id - %s' % (e))
        return [], []
    else:
        return county_ids, area_ids


def get_person_orgs(request):
    """method to get person geos."""
    try:
        org_ids, ou_ids = [], []
        person_id = request.user.reg_person.id
        orgs = RegPersonsOrgUnits.objects.filter(
            person_id=person_id, is_void=False)
        for org in orgs:
            org_id = org.org_unit.id
            org_type_id = org.org_unit.org_unit_type_id
            if org_type_id == 'TNGP':
                ou_ids.append(org_id)
            org_ids.append(org_id)
        sub_orgs = RegOrgUnit.objects.filter(
            parent_org_unit_id__in=ou_ids, is_void=False)
        for sorg in sub_orgs:
            org_id = sorg.id
            org_ids.append(org_id)
    except Exception as e:
        print('Error getting org_id - %s' % (e))
        return []
    else:
        return org_ids


def save_persons(request, params, person_type):
    """Method to save persons."""
    try:
        print(params, person_type)
        user_id = request.user.id
        today = timezone.now()
        designation = params['designation']
        first_name = params['first_name'].upper()
        onames = params['other_names'] if 'other_names' in params else ''
        other_names = onames.upper() if onames else None
        surname = params['surname'].upper()
        sex_id = params['sex']
        phone = params['phone'] if 'phone' in params else None
        dob = params['dob'] if 'dob' in params else None
        area_id = params['area_id'] if 'area_id' in params else None
        phone_number = phone if phone else None
        person = RegPerson(
            designation=designation,
            first_name=first_name,
            other_names=other_names,
            surname=surname, sex_id=sex_id,
            des_phone_number=phone_number,
            date_of_birth=dob, created_by_id=user_id)
        person.save()
        person_id = person.pk
        # Save Person Types
        ptype = RegPersonsTypes(
            person_id=person_id, person_type_id=person_type,
            date_began=today)
        ptype.save()
        # Save Persons Geo
        pgeo = RegPersonsGeo(
            person_id=person_id, area_id=area_id,
            area_type='GLTL', date_linked=today)
        pgeo.save()
        print('person saved')
    except Exception as e:
        print('Error saving persons - %s' % (e))
        return None
    else:
        return person


def save_household(child_id, person, relation):
    """Method to save Household members."""
    try:
        today = timezone.now()
        if person:
            member_id = person.id
            if relation == 'TBVC':
                hh = RegPersonsSiblings(
                    child_person_id=child_id,
                    sibling_person_id=member_id,
                    date_linked=today).save()
            else:
                hh = RegPersonsGuardians(
                    child_person_id=child_id,
                    guardian_person_id=member_id,
                    relationship=relation,
                    date_linked=today)
                hh.save()
    except Exception as e:
        raise e
    else:
        pass


def handle_persons(request, case, case_id):
    """Method to handle persons."""
    try:
        person_ids = []
        persons = OVCBasicPerson.objects.filter(
            case_id=case_id, is_void=False)
        for person in persons:
            person_type = person.person_type
            print('person type', person_type)
            if person_type == 'PTCH':
                print('Child')
                params = {'designation': 'CGSI'}
                # Parents and caregivers
                params = {'designation': 'CCGV'}
                print(params)
    except Exception as e:
        raise e
    else:
        return person_ids


def get_param(item_id, params):
    """Method to get param."""
    try:
        param = params[item_id] if item_id in params else ''
    except Exception:
        return None
    else:
        return param


def save_photo(request, img_name, img_string):
    """Method to save images."""
    try:
        img_data = base64.b64decode(img_string)
        file_name = 'some_image.jpg'
        with open(file_name, 'wb') as f:
            f.write(img_data)
    except Exception as e:
        raise e
    else:
        pass


def create_crs(request, case, case_id):
    """Method to save CRS."""
    try:
        response = {}
        persons, case_ids = [], []
        today = timezone.now()
        user_id = request.user.id
        sub_county = case.constituency
        case_ids.append(case_id)
        sc_id = int(sub_county) if sub_county else 0
        # Form variables
        case_org_unit = request.POST.get('case_org_unit')
        case_sub_county = request.POST.get('case_sub_county')
        case_county = request.POST.get('case_county')
        # Get Geos
        geo = get_geo(sc_id)
        if geo:
            sub_county_id = geo.area_id
            county_id = geo.parent_area_id
        else:
            sub_county_id = int(case_sub_county)
            county_id = int(case_county)
        area_id = sub_county_id
        if case.account.username != 'vurugumapper':
            return response
        if case.case_params:
            case_params = eval(str(case.case_params))
            print(case_params)
            # Save Index Child
            onames = get_param('child_other_names', case_params)
            ichild_params = {'designation': 'CGOC',
                             'sex': case_params['child_sex']}
            ichild_params['first_name'] = case_params['child_first_name']
            ichild_params['other_names'] = onames
            ichild_params['surname'] = case_params['child_surname']
            ichild_params['dob'] = case_params['child_dob']
            ichild_params['area_id'] = area_id
            ichild_params['phone'] = ''
            person = save_persons(request, ichild_params, 'TBVC')
            child_id = person.pk
            persons.append(child_id)
            # Save Siblings
            for sibling_params in case_params['siblings']:
                sibling_params['designation'] = 'CGSI'
                sibling_params['area_id'] = area_id
                sibling_params['phone'] = ''
                fcheck = get_param('first_name', sibling_params)
                if fcheck:
                    person = save_persons(request, sibling_params, 'TBVC')
                    # Save siblings relation
                    save_household(child_id, person, 'TBVC')
            # Save Parents
            cnt = 0
            for parents_params in case_params['parents']:
                cnt += 1
                parents_params['designation'] = 'CCGV'
                parents_params['area_id'] = area_id
                relation = 'CGPF' if cnt == 1 else 'CGPM'
                sex_id = 'SMAL' if cnt == 1 else 'SFEM'
                parents_params['sex'] = sex_id
                fcheck = get_param('first_name', parents_params)
                if fcheck:
                    person = save_persons(request, parents_params, 'TBGR')
                    # Save Parents
                    save_household(child_id, person, relation)
            # Save Caregivers
            for caregiver_params in case_params['caregivers']:
                caregiver_params['designation'] = 'CCGV'
                caregiver_params['area_id'] = area_id
                fcheck = get_param('first_name', caregiver_params)
                if fcheck:
                    relation = get_param('relationship', caregiver_params)
                    person = save_persons(request, caregiver_params, 'TBGR')
                    # Save Caregivers
                    save_household(child_id, person, relation)
        else:
            persons = handle_persons(request, case, case_id)
            case_params = model_to_dict(case)
        # Save Case Record Sheet
        serial_number = ''
        perp_first_name = ''
        perp_other_names = ''
        perp_surname = ''
        perp_relationship = ''
        court_name = ''
        court_number = ''
        police_station = ''
        ob_number = ''
        all_perps = []
        perpetrator_status = case_params['perpetrator_status']
        case_reporter = case_params['case_reporter']
        perps = get_param('perpetrators', case_params)
        perpetrators = perps if perps else []
        if len(perpetrators) > 0:
            perps = perpetrators[0]
            if 'first_name' in perps:
                perp_first_name = perps['first_name']
                perp_other_names = perps['other_names']
                perp_surname = perps['surname']
                perp_relationship = perps['relationship']
        if len(perpetrators) > 1:
            pnt = 0
            for perp in perpetrators:
                pnt += 1
                if pnt > 1:
                    all_perps.append(perp)
        # Reporter details
        reporter_first_name = case_params['reporter_first_name']
        reporter_other_names = case_params['reporter_other_names']
        reporter_surname = case_params['reporter_surname']
        reporter_contacts = case_params['reporter_telephone']
        date_case_opened = case_params['case_date']
        date_of_summon = None
        case_remarks = get_param('case_narration', case_params)
        risk_level = case_params['risk_level']
        refferal_present = 'ANNO'
        for person_id in persons:
            serial_number = validate_serialnumber(
                person_id, sub_county_id, serial_number)
            response['case_serial'] = serial_number
            # OVCCaseRecord
            ovccaserecord = OVCCaseRecord(
                case_id=case_id,
                case_serial=serial_number,
                perpetrator_status=perpetrator_status,
                perpetrator_first_name=perp_first_name,
                perpetrator_other_names=perp_other_names,
                perpetrator_surname=perp_surname,
                perpetrator_relationship_type=perp_relationship,
                case_reporter=case_reporter,
                court_name=court_name,
                court_number=court_number,
                police_station=police_station,
                ob_number=ob_number,
                case_reporter_first_name=reporter_first_name,
                case_reporter_other_names=reporter_other_names,
                case_reporter_surname=reporter_surname,
                case_reporter_contacts=reporter_contacts,
                date_case_opened=date_case_opened,
                risk_level=risk_level,
                date_of_summon=date_of_summon,
                case_remarks=case_remarks,
                referral_present=refferal_present,
                timestamp_created=today,
                created_by=user_id,
                person_id=person_id).save()

            # OVCCaseCategory
            category_lists = case_params['case_details']
            for case_category in category_lists:
                category_name = case_category['category']
                date_of_event = case_category['date_of_event']
                place_of_event = case_category['place_of_event']
                case_nature = case_category['nature_of_event']
                em_explain = get_param('emergency_explain', case_category)
                case_grouping_id = new_guid_32()
                print('Emergency', em_explain)
                ovccasecategory = OVCCaseCategory(
                    case_id_id=case_id,
                    case_grouping_id=case_grouping_id,
                    case_category=category_name,
                    date_of_event=date_of_event,
                    place_of_event=place_of_event,
                    case_nature=case_nature,
                    timestamp_created=today,
                    person_id=person_id
                )
                ovccasecategory.save()
                case_cat_id = ovccasecategory.pk

                # OVCCaseSubCategory
                case_subcategory_lists = [category_name]
                for i, case_subcat in enumerate(case_subcategory_lists):
                    OVCCaseSubCategory(
                        case_category_id=case_cat_id,
                        case_grouping_id=case_grouping_id,
                        sub_category_id=case_subcat,
                        timestamp_created=today,
                        person_id=person_id
                    ).save()

            # OVCCaseGeo
            report_ward = ''
            report_village = ''
            occurence_ward = ''
            occurence_village = case_params['case_village']
            org_unit_id = case_org_unit
            report_sc_id = case_sub_county
            OVCCaseGeo(
                case_id_id=case_id,
                report_subcounty_id=report_sc_id,
                report_ward=report_ward,
                report_village=report_village,
                report_orgunit_id=org_unit_id,
                occurence_county_id=county_id,
                occurence_subcounty_id=sub_county_id,
                occurence_ward=occurence_ward,
                occurence_village=occurence_village,
                timestamp_created=today,
                person_id=person_id).save()

            # OVCReferral
            referrals = []
            referral = get_param('referral_destination', case_params)
            # SA Referral
            referral_sa = get_param('referral_destination_sa', case_params)
            referral_reason_sa = get_param('referral_reason_sa', case_params)
            # NSA Referral
            referral_nsa = get_param('referral_destination_nsa', case_params)
            referral_reason_nsa = get_param('referral_reason_nsa', case_params)
            if referral == 'RDSA':
                refs = {}
                refs['actor_type'] = referral
                refs['refferal_to'] = referral_sa
                refs['destination'] = referral_reason_sa
                referrals.append(refs)
            elif referral == 'RDNA':
                refs = {}
                refs['actor_type'] = referral
                refs['refferal_to'] = referral_nsa
                refs['destination'] = referral_reason_nsa
                referrals.append(refs)
            # Now save the referrals
            for referralactors in referrals:
                actor_type = referralactors['actor_type']
                actor_description = referralactors['destination']
                referral_to = referralactors['refferal_to']
                referral_grouping_id = new_guid_32()
                OVCReferral(
                    case_id_id=case_id,
                    refferal_actor_type=actor_type,
                    refferal_actor_specify=actor_description,
                    refferal_to=referral_to,
                    referral_grouping_id=referral_grouping_id,
                    case_category=None,
                    timestamp_created=today,
                    person_id=person_id).save()

            # OVCEconomicStatus
            hh_economic_status = case_params['hh_economic_status']
            OVCEconomicStatus(
                case_id_id=case_id,
                household_economic_status=hh_economic_status,
                timestamp_created=today,
                person_id=person_id).save()

            # OVCFamilyStatus
            family_status = case_params['family_status']
            if family_status:
                family_status = str(family_status).split(',')
                for familystatus in family_status:
                    OVCFamilyStatus(
                        case_id_id=case_id,
                        family_status=familystatus,
                        timestamp_created=today,
                        person_id=person_id).save()

            # OVCHobbies
            hobbies = get_param('hobbies', case_params)
            if hobbies:
                hobbies = str(hobbies).split(",")
                for hobby in hobbies:
                    OVCHobbies(
                        case_id_id=case_id,
                        hobby=hobby.upper(),
                        timestamp_created=today,
                        person_id=person_id).save()

            # OVCFriends
            friends = get_param('friends', case_params)
            if friends:
                friends = str(friends).split(",")
                for friend in friends:
                    ffname = friend
                    foname = 'XXXX'
                    fsname = 'XXXX'
                    OVCFriends(
                        case_id_id=case_id,
                        friend_firstname=ffname.upper(),
                        friend_other_names=foname.upper(),
                        friend_surname=fsname.upper(),
                        timestamp_created=today,
                        person_id=person_id).save()
            # Save Other perpetrators
            if all_perps:
                for one_perp in all_perps:
                    relation = one_perp['relationship']
                    sex_id = one_perp['sex']
                    OvcCasePersons(
                        person_first_name=one_perp['first_name'],
                        person_other_names=one_perp['other_names'],
                        person_surname=one_perp['surname'],
                        person_relation=relation,
                        case_id=case_id, person_sex=sex_id,
                        person_id=person_id).save()

            # OVCMedical
            medical_id = new_guid_32()
            mental_condition = case_params['mental_condition']
            physical_condition = case_params['physical_condition']
            other_condition = case_params['other_condition']
            OVCMedical(
                medical_id=medical_id, case_id_id=case_id,
                mental_condition=mental_condition,
                physical_condition=physical_condition,
                other_condition=other_condition,
                timestamp_created=today,
                person_id=person_id).save()
            # OVCMedicalSubconditions
            mental_subconditions = []
            phy_subconditions = []
            other_subconditions = []
            med_conditions = []
            if not mental_condition == "MNRM":
                for i, mental_subcondition in enumerate(mental_subconditions):
                    mental_subcondition = mental_subcondition.split(',')
                    for mcondition in mental_subcondition:
                        med_conditions.append(
                            {"medical_condition": "Mental",
                             "medical_subcondition": mcondition})
            if not physical_condition == "PNRM":
                for i, physical_subcondition in enumerate(phy_subconditions):
                    physical_subcondition = physical_subcondition.split(
                        ',')
                    for pcondition in physical_subcondition:
                        med_conditions.append(
                            {"medical_condition": "Physical",
                             "medical_subcondition": pcondition})
            if not other_condition == "CHNM":
                for i, other_subcondition in enumerate(other_subconditions):
                    other_subcondition = other_subcondition.split(',')
                    for ocondition in other_subcondition:
                        med_conditions.append(
                            {"medical_condition": "Other",
                             "medical_subcondition": ocondition})

            for med_condition in med_conditions:
                OVCMedicalSubconditions(
                    medicalsubcond_id=new_guid_32(),
                    medical_id_id=medical_id,
                    medical_condition=med_condition['medical_condition'],
                    medical_subcondition=med_condition['medical_subcondition'],
                    timestamp_created=today,
                    person_id=person_id).save()

            # OVCNeeds
            im_needs = get_param('immediate_needs', case_params)
            lt_needs = get_param('long_term_needs', case_params)
            if im_needs:
                immediate_need = str(im_needs).split(',')
                for immediateneed in immediate_need:
                    OVCNeeds(
                        case_id_id=case_id, need_type='IMMEDIATE',
                        need_description=immediateneed.upper(),
                        timestamp_created=today,
                        person_id=person_id
                    ).save()
            if lt_needs:
                future_need = str(lt_needs).split(',')
                for futureneed in future_need:
                    OVCNeeds(
                        case_id_id=case_id, need_type='FUTURE',
                        need_description=futureneed.upper(),
                        timestamp_created=today,
                        person_id=person_id
                    ).save()

            # FormsLog
            FormsLog(
                form_id=str(case_id).replace('-', ''),
                form_type_id='FTPC',
                timestamp_created=today,
                app_user=user_id,
                person_id=person_id).save()

            # Collect CaseIds Used ##
            case_ids.append(str(case_id))

            # Setup parent_case_id
            parent_case_id = case_ids[0]
            case_ids.pop(0)
            if case_ids:
                ovccaserecords = OVCCaseRecord.objects.filter(
                    case_id__in=case_ids)
                for ovccaserecord in ovccaserecords:
                    ovccaserecord.parent_case_id = parent_case_id
                    ovccaserecord.save(update_fields=['parent_case_id'])
    except Exception as e:
        print('error saving CRS - %s' % (str(e)))
        raise e
    else:
        return response



def generate_document(request, response, params, case):
    """Method to generate documents."""
    try:
        doc = SimpleDocTemplate(
        response, rightMargin=.5 * cm, leftMargin=.5 * cm,
        topMargin=1.5 * cm, bottomMargin=1.5 * cm,
        title="Case Record Sheet", author='CPIMS',
        subject="CPIMS - Case Record Sheet", creator="CPIMS",
        keywords="CPIMS, DCS, Case Record Sheet")

        story = []
        # Styles
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
        styles.add(ParagraphStyle(name='Left', alignment=TA_LEFT))
        styles.add(ParagraphStyle(
            name='Line_Data', alignment=TA_LEFT, fontSize=9, leading=18))
        styles.add(ParagraphStyle(
            name='Line_Datas', alignment=TA_LEFT, fontSize=8, leading=10))
        styles.add(ParagraphStyle(
            name='Line_Data_Small', alignment=TA_LEFT, fontSize=7, leading=8))
        styles.add(ParagraphStyle(
            name='Line_Data_Large', alignment=TA_LEFT, fontSize=12, leading=12))
        styles.add(ParagraphStyle(
            name='Line_Data_Largest', alignment=TA_LEFT, fontSize=14, leading=15))
        styles.add(ParagraphStyle(
            name='Line_Label', font='Helvetica-Bold',
            fontSize=8, leading=14, alignment=TA_LEFT))
        styles.add(ParagraphStyle(
            name='Line_Labels', font='Helvetica-Bold',
            fontSize=8, leading=6, alignment=TA_LEFT))
        styles.add(ParagraphStyle(
            name='Line_Title', font='Helvetica-Bold',
            fontSize=10, alignment=TA_LEFT))
        styles.add(ParagraphStyle(
            name='Line_Label_Center', font='Helvetica-Bold',
            fontSize=12, leading=10, alignment=TA_CENTER))

        # Get company information
        data1 = [[Image(logo_path, 1.8 * cm, 1.5 * cm)]]
        tt1 = Table(data1, colWidths=(None,), rowHeights=[0.5 * cm])
        sllc = styles["Line_Label_Center"]
        slds = styles["Line_Data_Small"]

        story.append(tt1)
        story.append(Paragraph("<b>DEPARTMENT OF CHILDREN'S SERVICES</b>", sllc))

        story.append(Spacer(0.1 * cm, .2 * cm))

        story.append(Paragraph("<b>CASE REFERRAL FORM</b>", sllc))

        story.append(Spacer(0.1 * cm, .2 * cm))

        data1 = [[Paragraph('<b>CASE REFERRAL FORM </b>', styles["Line_Title"]),
                  Paragraph("<b><i>Rev. Jul '18</i></b>", slds)]]
        t1 = Table(data1, colWidths=(None, 2.0 * cm), rowHeights=[0.5 * cm])
        t1.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), '#a7a5a5'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(t1)
        story.append(Spacer(0.1 * cm, .1 * cm))
        intro = 'This form is to be filled when making a case referral to other '
        intro += 'agencies, children institutions, VCOs and any other '
        intro += ' relevant agency or office.'
        data1 = [[Paragraph(intro, styles["Line_Label"]), ]]
        t1 = Table(data1, colWidths=(None))
        t1.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(t1)
        story.append(Spacer(0.1 * cm, .1 * cm))
        # story.append(Paragraph('TO', styles["Line_Data_Large"]))
        data0 = [[Paragraph('<b>TO</b>', styles["Line_Label"]),
                  Paragraph(params['ref_to'], styles["Line_Label"])], ['', '']]
        t0 = Table(data0, colWidths=(3*cm, None))
        t0.setStyle(TableStyle([
            ('INNERGRID', (1, 0), (1, 1), 0.25, colors.black),
        ]))
        story.append(t0)
        # From details
        data0 = [[Paragraph('<b>FROM</b>', styles["Line_Label"]),
                  Paragraph(params['ref_from'], styles["Line_Label"])], ['', '']]
        t0 = Table(data0, colWidths=(3*cm, None))
        t0.setStyle(TableStyle([
            ('INNERGRID', (1, 0), (1, 1), 0.25, colors.black),
        ]))
        story.append(t0)

        childs = [[Paragraph('<b>I. PARTICULARS OF THE CHILD(REN)</b>', styles["Line_Label"])]]
        tc = Table(childs, colWidths=(None))
        story.append(tc)
        story.append(Spacer(0.1 * cm, .2 * cm))
        # Siblings
        data1 = [[Paragraph('<b>No.</b>', styles["Line_Label"]),
              Paragraph('<b>Name</b>', styles["Line_Label"]),
              Paragraph('<b>D.O.B</b>', styles["Line_Label"]),
              Paragraph('<b>Sex</b>', styles["Line_Label"]),
              Paragraph('<b>Name of School</b>', styles["Line_Label"]),
              Paragraph('<b>Class</b>', styles["Line_Label"]),
              Paragraph('<b>Remarks</b>', styles["Line_Label"])],
        ]

        t1 = Table(data1, colWidths=(
            0.9 * cm, 5.0 * cm, 2.5 * cm, 2.0 * cm, 5 * cm,
            1.5 * cm, 2.7 * cm), rowHeights = [0.6 * cm])
        t1.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(t1)
        # Sibling details
        kids = 5
        siblings = {}
        for i in range(1, kids):
            name, sex = '', ''
            if i == 1:
                name = params['child']['name']
                sex = params['child']['sex']
            siblings[i] = {'name': name, 'dob': '', 'sex': sex}
        items = [{'sibling': i} for i in range (1, kids)]
        data1 = [[Paragraph(str(product['sibling']), styles["Line_Datas"]),
                 Paragraph(str(siblings[product['sibling']]['name']), styles["Line_Datas"]),
                 Paragraph(str(siblings[product['sibling']]['dob']), styles["Line_Datas"]),
                 Paragraph(str(siblings[product['sibling']]['sex']), styles["Line_Datas"]),
                 '','', ''] for product in items]

        t1 = Table(data1, colWidths=(
            0.9 * cm, 5.0 * cm, 2.5 * cm, 2.0 * cm, 5 * cm, 1.5 * cm, 2.7 * cm))
        t1.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(t1)

        story.append(Spacer(0.1 * cm, .6 * cm))

        data2 = [[Paragraph('<b>II. REASONS FOR REFERRAL</b>', styles["Line_Label"]),
                  Paragraph('<b>III. DOCUMENTS ATTACHED</b>', styles["Line_Label"])]]
        t2 = Table(data2, colWidths=(None, None))
        story.append(t2)
        data1 = [[Image(unchecked_image_path, .25 * cm, .25 * cm),
              Paragraph('By Court Order', styles["Line_Labels"]),
              Image(unchecked_image_path, .25 * cm, .25 * cm),
              Paragraph('Case Record Sheet', styles["Line_Labels"])],
              [Image(unchecked_image_path, .25 * cm, .25 * cm),
              Paragraph('Supervision', styles["Line_Labels"]),
              Image(unchecked_image_path, .25 * cm, .25 * cm),
              Paragraph('Social Enquiry Report', styles["Line_Labels"])],
              [Image(checked_image_path, .25 * cm, .25 * cm),
              Paragraph('Other (Specify)', styles["Line_Labels"]),
              Image(unchecked_image_path, .25 * cm, .25 * cm),
              Paragraph('Court Order', styles["Line_Labels"])],
              ['', '',
              Image(unchecked_image_path, .25 * cm, .25 * cm),
              Paragraph('Individual Treatment Plan', styles["Line_Labels"])],
              [Paragraph('M', styles["Line_Labels"]), Paragraph(params['mum'], styles["Line_Datas"]),
              Image(unchecked_image_path, .25 * cm, .25 * cm),
              Paragraph('Written Promise', styles["Line_Labels"])],
              [Paragraph('F', styles["Line_Labels"]), Paragraph(params['dad'], styles["Line_Datas"]),
              Image(unchecked_image_path, .25 * cm, .25 * cm),
              Paragraph('Any Other documents e.g Medical report / Birth certificate', styles["Line_Labels"]),]

        ]
        t1 = Table(data1, colWidths=(0.6 * cm, None, 0.6 * cm, None))
        t1.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('INNERGRID', (1, 3), (1, 4), 0.25, colors.black),
            ('INNERGRID', (1, 4), (1, 5), 0.25, colors.black),
            ('INNERGRID', (1, 5), (1, 6), 0.25, colors.black),
        ]))
        story.append(t1)
        story.append(Spacer(0.1 * cm, .6 * cm))

        story.append(Paragraph('<b>DETAILS</b>', styles["Line_Label"]))

        story.append(Spacer(0.1 * cm, .6 * cm))

        story.append(Paragraph(case.case_narration, styles["Line_Data"]))
        story.append(Spacer(0.1 * cm, .6 * cm))
        data0 = [[Paragraph('NAME OF OFFICER', styles["Line_Label"]),
                  Paragraph('', styles["Line_Label"])], ['', '']]
        t0 = Table(data0, colWidths=(4 * cm, None))
        t0.setStyle(TableStyle([
            ('INNERGRID', (1, 0), (1, 1), 0.25, colors.black),
        ]))
        story.append(t0)
        story.append(Spacer(0.1 * cm, .6 * cm))
        case_date = case.case_date
        doc_date = str(case_date.strftime('%d %b, %Y'))
        data1 = [
        ['', '', Paragraph(doc_date, styles["Line_Data_Large"])],
        [Paragraph('SIGNATURE', styles["Line_Label"]), '',
         Paragraph('DATE', styles["Line_Label"])]]

        t1 = Table(data1, colWidths=(None, 2 * cm, None))
        t1.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (0, 1), 0.25, colors.black),
            ('INNERGRID', (2, 0), (2, 1), 0.25, colors.black),
        ]))

        story.append(t1)

        doc.build(story)
    except Exception as e:
        raise e
    else:
        pass
