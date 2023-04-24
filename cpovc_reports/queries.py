QUERIES = {}
# Reports
REPORTS = {}
# Reports listings
REPORTS[1] = 'registration'
REPORTS[2] = 'registration'
REPORTS[3] = 'registration'
REPORTS[4] = 'registration'
REPORTS[5] = 'not_served'
REPORTS[6] = 'pepfar_detailed'
REPORTS[7] = 'registration'
REPORTS[8] = 'registration'
REPORTS[9] = 'registration'
REPORTS[10] = 'registration'
REPORTS[11] = 'form1b_summary'
REPORTS[12] = 'ovc_served_list'

REPORTS['GOK_1'] = 'org_units'
REPORTS['GOK_2'] = 'institution_register'
REPORTS['GOK_3'] = 'case_load'
REPORTS['GOK_4'] = 'excel_tool_a'
REPORTS['GOK_5'] = 'missing_children'
REPORTS['GOK_6'] = 'vac'
REPORTS['GOK_7'] = 'vac'
REPORTS['GOK_8'] = 'services'
REPORTS['GOK_9'] = 'institution_population'
REPORTS['GOK_10'] = 'tip'
REPORTS['GOK_11'] = 'tip_new'
REPORTS['GOK_12'] = 'u_case_load'
# Registers
REPORTS['GOK_21'] = 'case_load_register'
REPORTS['GOK_22'] = 'institution_register'
REPORTS['GOK_23'] = 'case_load'
REPORTS['GOK_24'] = 'cases_hl'
REPORTS['GOK_25'] = 'cases_hl'
# AFC
REPORTS['AFC_1'] = 'afc_summary'
REPORTS['AFC_2'] = 'afc_identification'
REPORTS['AFC_3'] = 'afc_assessment_child'
REPORTS['AFC_4'] = 'afc_assessment_family'
REPORTS['AFC_5'] = 'afc_case_plan'
REPORTS['AFC_6'] = 'afc_case_plan'
REPORTS['AFC_7'] = 'afc_monitoring'
REPORTS['AFC_8'] = 'afc_case_review'
REPORTS['AFC_9'] = 'afc_case_review_ya'
REPORTS['AFC_10'] = 'afc_closure'
REPORTS['AFC_11'] = 'afc_consent'
REPORTS['AFC_12'] = 'afc_transfer'
REPORTS['AFC_13'] = 'afc_referral'
REPORTS['AFC_14'] = 'afc_disability'
REPORTS['AFC_15'] = 'afc_feedback_caregiver'
REPORTS['AFC_16'] = 'afc_feedback_child'

QUERIES['org_units'] = '''
select
ROW_NUMBER () OVER (ORDER BY rp.date_linked) as SNO,
ou.org_unit_name as "case category", ou.org_unit_type_id as "type name",
concat(pp.first_name,' ',pp.surname,' ',pp.other_names) as Names,
CASE pp.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Sex,
CASE
WHEN  date_part('year', age(timestamp '{end_date}', pp.date_of_birth)) < 35 THEN 'a.[< 35 yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', pp.date_of_birth)) BETWEEN 35 AND 50 THEN 'b.[35 - 50 yrs]'
ELSE 'c.[50+ yrs]' END AS agerange,
rp.primary_unit,
1 as ovccount
from reg_persons_org_units as rp
inner join reg_org_unit as ou on ou.id=rp.org_unit_id
inner join reg_person as pp on pp.id=rp.person_id
where rp.is_void = False
'''

QUERIES['institution_register'] = '''
SELECT
ROW_NUMBER () OVER (ORDER BY ovc_placement.timestamp_created) as SNO,
concat(pp.first_name,' ',pp.surname,' ',pp.other_names) as Names,
date_part('year', age(admission_date, pp.date_of_birth)) AS Admission_Age,
CASE pp.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Sex,
admission_date as "admission date", df.date_of_discharge as "discharge date",
CASE
WHEN  date_part('year', age(admission_date, pp.date_of_birth)) < 6 THEN 'a.[0 - 5 yrs]'
WHEN  date_part('year', age(admission_date, pp.date_of_birth)) BETWEEN 6 AND 9 THEN 'b.[6 - 9 yrs]' 
WHEN  date_part('year', age(admission_date, pp.date_of_birth)) BETWEEN 10 AND 15 THEN 'c.[10 - 15 yrs]' 
WHEN  date_part('year', age(admission_date, pp.date_of_birth)) BETWEEN 16 AND 18 THEN 'd.[16 - 18 yrs]' 
ELSE 'e.[18+ yrs]' END AS agerange,
c_cat.item_description as "case category",
CASE ovc_placement.is_active WHEN 'TRUE' THEN 'Active' ELSE 'Discharged' END AS Status,
1 as ovccount
from ovc_placement
inner join reg_person as pp on person_id = pp.id
left outer join ovc_case_record as cr on cr.case_id = ovc_placement.case_record_id
left outer join ovc_case_category as cc on cc.case_id_id = cr.case_id
left outer join list_general c_cat on c_cat.item_id=cc.case_category and c_cat.field_name = 'case_category_id'
left outer join ovc_discharge_followup as df on df.placement_id_id = ovc_placement.placement_id
where ovc_placement.is_void = False and admission_date between '{start_date}' and '{end_date}'
and residential_institution_name = '{org_unit}'
'''

QUERIES['case_load'] = '''
select ovc_case_record.person_id as cpims_id,
TO_CHAR(date_case_opened :: DATE, 'dd-Mon-yyyy') as case_date,
to_char(date_case_opened, 'YYYY')::INTEGER as "case_year",
TO_CHAR(date_case_opened :: DATE, 'MM-Mon') as "case_month",
case
when to_char(date_case_opened, 'MM')::INTEGER BETWEEN 1 AND 3 THEN 3
when to_char(date_case_opened, 'MM')::INTEGER BETWEEN 4 AND 6 THEN 4
when to_char(date_case_opened, 'MM')::INTEGER BETWEEN 7 AND 9 THEN 1
else 2 end as "case_qtr",
case_serial, concat(case_serial,' - ',c_cat.item_description) as serial_case_category,
CASE risk_level WHEN 'RLHG' THEN 'High' WHEN 'RLMD' THEN 'Medium' ELSE 'Low' END AS risk_level,
CASE perpetrator_status WHEN 'PSSL' THEN 'Self' WHEN 'PKNW' THEN 'Unknown'
WHEN 'PUNK' THEN 'Unknown' ELSE 'Not Available' END AS perpetrator_status,
cr_cat.item_description as case_reporter,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS sex,
date_part('year', age(date_case_opened, reg_person.date_of_birth)) AS age,
CASE
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) < 6 THEN 'a.[0 - 5 yrs]'
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 6 AND 9 THEN 'b.[6 - 9 yrs]' 
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 10 AND 15 THEN 'c.[10 - 15 yrs]' 
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 16 AND 18 THEN 'd.[16 - 18 yrs]' 
ELSE 'e.[18+ yrs]' END AS agerange,
CASE
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) < 5 THEN 'a.[0 - 4 yrs]'
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'b.[5 - 9 yrs]' 
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'c.[10 - 14 yrs]' 
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 15 AND 18 THEN 'd.[15 - 18 yrs]'
ELSE 'e.[18+ yrs]' END AS knbs_agerange,
CASE
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) < 6 THEN 'a.[0 - 5 yrs]'
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 6 AND 9 THEN 'b.[6 - 9 yrs]' 
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'c.[10 - 14 yrs]' 
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'd.[15 - 17 yrs]'
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) = 18 THEN 'e.[18 yrs]'
ELSE 'f.[18+ yrs]' END AS un_agerange,
CASE case_stage WHEN 2 THEN 'Closed' WHEN 1 THEN 'Active' ELSE 'Pending' END AS Case_status,
case_status as case_state,
CASE ccat.case_nature WHEN 'OOEV' THEN 'One Off' ELSE 'Chronic' END AS Case_Nature,
ev_cat.item_description as place_of_event, c_cat.item_description as "case category",
cs_cat.item_description as case_sub_category,
reg_org_unit.org_unit_name as org_unit, scou_geo.area_name as sub_county,
cou_geo.area_name as county,
case omed.mental_condition when 'MNRM' THEN 'Normal' else 'Has Condition' End as mental_condition,
case omed.physical_condition when 'PNRM' THEN 'Normal' else 'Has Condition' End as physical_condition,
case omed.other_condition when 'CHNM' THEN 'Normal' else 'Has Condition' End as other_condition,
CASE cen.service_provided WHEN cen.service_provided THEN intv.item_description ELSE 'Case Open' END AS intervention,
TO_CHAR(ovc_case_record.timestamp_created :: DATE, 'dd-Mon-yyyy') as system_date,
1 as ovccount
from ovc_case_record
inner join ovc_case_category as ccat on case_id = ccat.case_id_id
inner join ovc_case_geo as cgeo on cgeo.case_id_id = case_id
inner join ovc_medical as omed on omed.case_id_id = case_id
left outer join reg_person on ovc_case_record.person_id=reg_person.id
left outer join reg_org_unit on reg_org_unit.id=cgeo.report_orgunit_id
left outer join list_geo as scou_geo on scou_geo.area_id=cgeo.report_subcounty_id and scou_geo.area_id > 47
left outer join list_geo as cou_geo on cou_geo.area_id=scou_geo.parent_area_id and cou_geo.area_id < 48
left outer join ovc_case_sub_category cscat on cscat.case_category_id=ccat.case_category_id
left outer join list_general c_cat on c_cat.item_id=ccat.case_category and c_cat.field_name = 'case_category_id'
left outer join list_general ev_cat on ev_cat.item_id=ccat.place_of_event and ev_cat.field_name = 'event_place_id'
left outer join list_general cr_cat on cr_cat.item_id=case_reporter and cr_cat.field_name = 'case_reporter_id'
left outer join list_general cs_cat on cs_cat.item_id=cscat.sub_category_id
left join ovc_case_events as cev on cev.case_id_id = case_id and cev.case_event_type_id = 'CLOSURE' and cev.is_void = false
left join ovc_case_event_encounters as cen on cen.case_event_id_id=cev.case_event_id
left outer join list_general intv on intv.item_id=cen.service_provided and intv.field_name = 'intervention_id'
where date_case_opened between '{start_date}' and '{end_date}' {other_params};
'''

# Serial	SubCounty	Date	Case Category	Sex	Age	Case Intervention	Special Comments	ReportingMonth	Date of Birth
QUERIES['excel_tool_a'] = '''
select case_serial as "Case Number",
ROW_NUMBER () OVER (ORDER BY ovc_case_record.timestamp_created) as Serial,
cou_geo.area_name as County, scou_geo.area_name as SubCounty,
date_case_opened as Date, c_cat.item_description as "Case Category",
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Sex,
date_part('year', age(date_case_opened, reg_person.date_of_birth)) AS Age,
CASE
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) < 6 THEN 'a.[0 - 5 yrs]'
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 6 AND 9 THEN 'b.[6 - 9 yrs]' 
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 10 AND 15 THEN 'c.[10 - 15 yrs]' 
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 16 AND 18 THEN 'd.[16 - 18 yrs]' 
ELSE 'e.[18+ yrs]' END AS AgeRange,
NULL as "Case Intervention", NULL as "Special Comments",
TO_CHAR(reg_person.date_of_birth :: DATE, 'dd-Mon-yyyy') as "Date of Birth",
1 as ovccount
from ovc_case_record
inner join ovc_case_category as ccat on case_id = ccat.case_id_id
inner join ovc_case_geo as cgeo on cgeo.case_id_id = case_id
left outer join reg_person on ovc_case_record.person_id=reg_person.id
left outer join list_geo as scou_geo on scou_geo.area_id=cgeo.report_subcounty_id and scou_geo.area_id > 47
left outer join list_geo as cou_geo on cou_geo.area_id=scou_geo.parent_area_id and cou_geo.area_id < 48
left outer join list_general c_cat on c_cat.item_id=ccat.case_category and c_cat.field_name = 'case_category_id'
where date_case_opened between '{start_date}' and '{end_date}' {other_params}
ORDER BY ovc_case_record.timestamp_created ASC;
'''

QUERIES['vac'] = '''
select case_serial as "Case Number",
ROW_NUMBER () OVER (ORDER BY ovc_case_record.timestamp_created) as Serial,
cou_geo.area_name as County, scou_geo.area_name as SubCounty,
date_case_opened as Date, c_cat.item_description as "Case Category",
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Sex,
date_part('year', age(date_case_opened, reg_person.date_of_birth)) AS Age,
CASE
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) < 6 THEN 'a.[0 - 5 yrs]'
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 6 AND 9 THEN 'b.[6 - 9 yrs]' 
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 10 AND 15 THEN 'c.[10 - 15 yrs]' 
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 16 AND 18 THEN 'd.[16 - 18 yrs]' 
ELSE 'e.[18+ yrs]' END AS AgeRange,
NULL as "Case Intervention",
TO_CHAR(reg_person.date_of_birth :: DATE, 'dd-Mon-yyyy') as "Date of Birth",
1 as ovccount
from ovc_case_record
inner join ovc_case_category as ccat on case_id = ccat.case_id_id
inner join ovc_case_geo as cgeo on cgeo.case_id_id = case_id
left outer join reg_person on ovc_case_record.person_id=reg_person.id
left outer join list_geo as scou_geo on scou_geo.area_id=cgeo.report_subcounty_id and scou_geo.area_id > 47
left outer join list_geo as cou_geo on cou_geo.area_id=scou_geo.parent_area_id and cou_geo.area_id < 48
left outer join list_general c_cat on c_cat.item_id=ccat.case_category and c_cat.field_name = 'case_category_id'
where ccat.case_category in ('CCCM', 'CSHV', 'CCDF', 'CCEA', 'CSCS', 'CSCU', 'CSDF', 'CSIC', 'CCOA', 'CSNG', 'CSRC', 'CSRG', 'CSSO')
and date_case_opened between '{start_date}' and '{end_date}' {other_params}
ORDER BY ovc_case_record.timestamp_created ASC;
'''


QUERIES['missing_children'] = '''
select case_serial as "Case Number",
ROW_NUMBER () OVER (ORDER BY ovc_case_record.timestamp_created) as Serial,
cou_geo.area_name as County, scou_geo.area_name as SubCounty,
date_case_opened as Date, c_cat.item_description as "Case Category",
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Sex,
date_part('year', age(date_case_opened, reg_person.date_of_birth)) AS Age,
CASE
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) < 6 THEN 'a.[0 - 5 yrs]'
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 6 AND 9 THEN 'b.[6 - 9 yrs]' 
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 10 AND 15 THEN 'c.[10 - 15 yrs]' 
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 16 AND 18 THEN 'd.[16 - 18 yrs]' 
ELSE 'e.[18+ yrs]' END AS AgeRange,
NULL as "Case Intervention",
TO_CHAR(reg_person.date_of_birth :: DATE, 'dd-Mon-yyyy') as "Date of Birth",
1 as ovccount
from ovc_case_record
inner join ovc_case_category as ccat on case_id = ccat.case_id_id
inner join ovc_case_geo as cgeo on cgeo.case_id_id = case_id
left outer join reg_person on ovc_case_record.person_id=reg_person.id
left outer join list_geo as scou_geo on scou_geo.area_id=cgeo.report_subcounty_id and scou_geo.area_id > 47
left outer join list_geo as cou_geo on cou_geo.area_id=scou_geo.parent_area_id and cou_geo.area_id < 48
left outer join list_general c_cat on c_cat.item_id=ccat.case_category and c_cat.field_name = 'case_category_id'
where ccat.case_category in ('CHCP', 'CDSA', 'CLFC')
and date_case_opened between '{start_date}' and '{end_date}' {other_params}
ORDER BY ovc_case_record.timestamp_created ASC;
'''


# Registration List
QUERIES['registration'] = '''
/*

select reg_org_unit.org_unit_name AS CBO,
reg_person.first_name, reg_person.surname,
reg_person.other_names, reg_person.date_of_birth, registration_date,
date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
date_part('year', age(ovc_registration.registration_date, reg_person.date_of_birth)) AS age_at_reg,
child_cbo_id as OVCID,
list_geo.area_name as ward, scc.area_name as constituency, cc.area_name as county,
CASE
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
CASE has_bcert WHEN 'True' THEN 'HAS BIRTHCERT' ELSE 'NO BIRTHCERT' END AS BirthCert,
CASE has_bcert WHEN 'True' THEN 'BCERT' ELSE NULL END AS BCertNumber,
CASE is_disabled WHEN 'True' THEN 'HAS DISABILITY' ELSE 'NO DISABILITY' END AS OVCDisability,
CASE is_Disabled WHEN 'True' THEN 'NCPWD' ELSE NULL END AS NCPWDNumber,
CASE
WHEN hiv_status = 'HSTP' THEN 'POSITIVE'
WHEN hiv_status = 'HSTN' THEN 'NEGATIVE'
ELSE 'NOT KNOWN' END AS OVCHIVstatus,
CASE hiv_status WHEN 'HSTP' THEN 'ART' ELSE NULL END AS ARTStatus,
concat(chw.first_name,' ',chw.surname,' ',chw.other_names) as CHW,
concat(cgs.first_name,' ',cgs.surname,' ',cgs.other_names) as parent_names,
CASE is_active WHEN 'True' THEN 'ACTIVE' ELSE 'EXITED' END AS Exit_status,
CASE is_active WHEN 'False' THEN exit_date ELSE NULL END AS Exit_date,
CASE
WHEN school_level = 'SLTV' THEN 'Tertiary'
WHEN school_level = 'SLUN' THEN 'University'
WHEN school_level = 'SLSE' THEN 'Secondary'
WHEN school_level = 'SLPR' THEN 'Primary'
WHEN school_level = 'SLEC' THEN 'ECDE'
ELSE 'Not in School' END AS Schoollevel,
CASE immunization_status
WHEN 'IMFI' THEN 'Fully Immunized'
WHEN 'IMNI' THEN 'Not Immunized'
WHEN 'IMNC' THEN 'Not Completed'
ELSE 'Not Known' END AS immunization
from ovc_registration
left outer join reg_person on person_id=reg_person.id
left outer join reg_person chw on child_chv_id=chw.id
left outer join reg_person cgs on caretaker_id=cgs.id
left outer join reg_org_unit on child_cbo_id=reg_org_unit.id
left outer join reg_persons_geo on ovc_registration.person_id=reg_persons_geo.person_id
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
left outer join list_geo as cc on cc.area_id=scc.parent_area_id
where reg_persons_geo.area_id > 337 and reg_persons_geo.is_void = False and child_cbo_id in ({cbos})
and ovc_registration.registration_date between '{start_date}' and '{end_date}';

*/

SELECT * from vw_cpims_registration where cbo_id in ({cbos})
and vw_cpims_registration.registration_date between '{start_date}' and '{end_date}'
order by  chv_id ASC, vw_cpims_registration.dob ASC, cbo_id ASC, ward_id ASC;

'''

# PEPFAR
QUERIES['pepfar'] = '''
select
cast(count(distinct ovc_care_events.person_id) as integer) as OVCCount,
reg_org_unit.org_unit_name AS CBO,
list_geo.area_name as ward, scc.area_name as constituency, cc.area_name as county,
date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
CASE
WHEN date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
CASE ovc_care_services.service_provided
WHEN 'HC1S' THEN 'Health' {domains}
ELSE 'Unknown'
END AS Domain
from ovc_care_services
INNER JOIN ovc_care_events ON ovc_care_events.event=ovc_care_services.event_id
INNER JOIN reg_person ON ovc_care_events.person_id=reg_person.id
LEFT OUTER JOIN ovc_registration ON ovc_care_events.person_id=ovc_registration.person_id
LEFT OUTER JOIN reg_org_unit ON reg_org_unit.id=ovc_registration.child_cbo_id
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id
LEFT OUTER JOIN list_geo ON list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
left outer join list_geo as cc on cc.area_id=scc.parent_area_id
WHERE reg_persons_geo.area_id > 337 and reg_persons_geo.is_void = False
and ovc_care_services.is_void = False
and ovc_care_events.event_type_id='FSAM'
and ovc_care_events.date_of_event between '{start_date}' and '{end_date}'
and ovc_registration.child_cbo_id in ({cbos})
GROUP BY ovc_care_services.service_provided, reg_person.date_of_birth,
reg_person.sex_id, ovc_registration.child_cbo_id,
reg_org_unit.org_unit_name, reg_persons_geo.area_id,
ward, constituency, county;'''

# PEPFAR SUMMARY
QUERIES['pepfar_sum'] = '''
'''

# DATIM
QUERIES['datim'] = '''
select
cast(count(distinct ovc_registration.person_id) as integer) as OVCCount,
reg_org_unit.org_unit_name AS CBO,
list_geo.area_name as ward, scc.area_name as constituency, cc.area_name as county,
date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
CASE
WHEN date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
CASE ovc_registration.hiv_status
WHEN 'HSTP' THEN '2a. (i) OVC_HIVSTAT: HIV+'
WHEN 'HSTN' THEN '2b. OVC_HIVSTAT: HIV-'
ELSE '2c. OVC_HIVSTAT: HIV Status NOT Known'
END AS Domain,
0 as Wardactive, 0 as WARDGraduated, 0 as WARDTransferred,
0 as WARDExitedWithoutGraduation
from ovc_registration
INNER JOIN reg_person ON ovc_registration.person_id=reg_person.id
LEFT OUTER JOIN reg_org_unit ON reg_org_unit.id=ovc_registration.child_cbo_id
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id
LEFT OUTER JOIN list_geo ON list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
left outer join list_geo as cc on cc.area_id=scc.parent_area_id
WHERE reg_persons_geo.area_id > 337 and reg_persons_geo.is_void = False
and ovc_registration.is_active = True
and ovc_registration.child_cbo_id in ({cbos})
and ((ovc_registration.is_active = True and ovc_registration.registration_date <= '{end_date}') 
or (ovc_registration.is_active = False 
and (ovc_registration.registration_date between '{start_date}' and '{end_date}' )) 
or (ovc_registration.is_active = False and ovc_registration.registration_date <= '{end_date}' 
and ovc_registration.exit_date > '{end_date}' ) 
or (ovc_registration.is_active = False and ovc_registration.registration_date <= '{end_date}' 
and ovc_registration.exit_date between '{start_date}' and '{end_date}' )) 
and not (ovc_registration.school_level = 'SLNS'
and date_part('year', '{end_date}'::date) - date_part('year', reg_person.date_of_birth::date) > 17)
GROUP BY ovc_registration.person_id, reg_person.date_of_birth,
reg_person.sex_id, ovc_registration.child_cbo_id,
reg_org_unit.org_unit_name, reg_persons_geo.area_id,
ovc_registration.hiv_status, ward, constituency, county
;'''


# DATIM - Served
QUERIES['datim_1'] = '''
select 
cast(count(distinct ovc_care_events.person_id) as integer) as OVCCount,
reg_org_unit.org_unit_name AS CBO,
list_geo.area_name as ward, scc.area_name as constituency, cc.area_name as county,
date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
CASE
WHEN date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
'1. OVC_Serv' as Domain
from ovc_care_services
INNER JOIN ovc_care_events ON ovc_care_events.event=ovc_care_services.event_id
INNER JOIN reg_person ON ovc_care_events.person_id=reg_person.id
LEFT OUTER JOIN ovc_registration ON ovc_care_events.person_id=ovc_registration.person_id
LEFT OUTER JOIN reg_org_unit ON reg_org_unit.id=ovc_registration.child_cbo_id
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id
LEFT OUTER JOIN list_geo ON list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
left outer join list_geo as cc on cc.area_id=scc.parent_area_id
WHERE  reg_persons_geo.area_id > 337 and reg_persons_geo.is_void = False
and ovc_care_services.is_void = False 
and ovc_care_events.event_type_id='FSAM'
and ovc_care_events.date_of_event between '{start_date}' and '{end_date}'
and ovc_registration.child_cbo_id in ({cbos})
and ((ovc_registration.is_active = True and ovc_registration.registration_date <= '{end_date}') 
or (ovc_registration.is_active = False 
and (ovc_registration.registration_date between '{start_date}' and '{end_date}' )) 
or (ovc_registration.is_active = False and ovc_registration.registration_date <= '{end_date}' 
and ovc_registration.exit_date > '{end_date}' ) 
or (ovc_registration.is_active = False and ovc_registration.registration_date <= '{end_date}' 
and ovc_registration.exit_date between '{start_date}' and '{end_date}' )) 
and not (ovc_registration.school_level = 'SLNS'
and date_part('year', '{end_date}'::date) - date_part('year', reg_person.date_of_birth::date) > 17)
GROUP BY reg_person.date_of_birth,
reg_person.sex_id, ovc_registration.child_cbo_id,
reg_org_unit.org_unit_name, reg_persons_geo.area_id,
ward, constituency, county;'''

# DATIM ART
QUERIES['datim_2'] = '''
select
cast(count(distinct ovc_registration.person_id) as integer) as OVCCount,
reg_org_unit.org_unit_name AS CBO,
list_geo.area_name as ward, scc.area_name as constituency, cc.area_name as county,
date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
CASE
WHEN date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
CASE ovc_care_health.art_status
WHEN 'ARAR' THEN '2a. (ii) OVC_HIVSTAT: HIV+ on ARV Treatment'
WHEN 'ARPR' THEN '2a. (ii) OVC_HIVSTAT: HIV+ on ARV Treatment'
ELSE '2a. (iii) OVC_HIVSTAT: HIV+ NOT on ARV Treatment'
END AS Domain,
0 as Wardactive, 0 as WARDGraduated, 0 as WARDTransferred,
0 as WARDExitedWithoutGraduation
from ovc_registration
INNER JOIN reg_person ON ovc_registration.person_id=reg_person.id
LEFT OUTER JOIN reg_org_unit ON reg_org_unit.id=ovc_registration.child_cbo_id
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id
LEFT OUTER JOIN list_geo ON list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
left outer join list_geo as cc on cc.area_id=scc.parent_area_id
LEFT OUTER JOIN ovc_care_health ON ovc_care_health.person_id=ovc_registration.person_id
WHERE reg_persons_geo.area_id > 337 and reg_persons_geo.is_void = False
AND ovc_registration.hiv_status = 'HSTP'
and ovc_registration.child_cbo_id in ({cbos})
and ((ovc_registration.is_active = True and ovc_registration.registration_date <= '{end_date}') 
or (ovc_registration.is_active = False 
and (ovc_registration.registration_date between '{start_date}' and '{end_date}' )) 
or (ovc_registration.is_active = False and ovc_registration.registration_date <= '{end_date}' 
and ovc_registration.exit_date > '{end_date}' ) 
or (ovc_registration.is_active = False and ovc_registration.registration_date <= '{end_date}' 
and ovc_registration.exit_date between '{start_date}' and '{end_date}' )) 
and not (ovc_registration.school_level = 'SLNS'
and date_part('year', '{end_date}'::date) - date_part('year', reg_person.date_of_birth::date) > 17)
GROUP BY ovc_registration.person_id, reg_person.date_of_birth,
reg_person.sex_id, ovc_registration.child_cbo_id,
reg_org_unit.org_unit_name, reg_persons_geo.area_id, list_geo.parent_area_id,
ovc_registration.hiv_status, ovc_care_health.art_status,
ward, constituency, county;'''

# Datim Ward summary
QUERIES['datim_3'] = '''
SELECT *
FROM crosstab(
  'select cast(ward as text), graduation,
  cast(sum(ccount) as integer) as ovcs from (
select cast(count(*) as integer) as ccount,
list_geo.area_name as ward,
case exit_reason
WHEN ''ERDE'' THEN ''WARDExitedWithoutGraduation''
WHEN ''EROE'' THEN ''WARDGraduated''
WHEN ''ERFI'' THEN ''WARDGraduated''
WHEN ''ERFR'' THEN ''WARDGraduated''
WHEN ''ERFS'' THEN ''WARDGraduated''
WHEN ''ERAD'' THEN ''WARDGraduated''
WHEN ''ERSE'' THEN ''WARDGraduated''
WHEN ''ERIN'' THEN ''WARDExitedWithoutGraduation''
WHEN ''ERRL'' THEN ''WARDTransferred''
WHEN ''ERDU'' THEN ''WARDTransferred''
WHEN ''ERTR'' THEN ''WARDGraduated''
WHEN ''ERLW'' THEN ''WARDExitedWithoutGraduation''
WHEN ''ERMA'' THEN ''WARDExitedWithoutGraduation''
WHEN ''ERTL'' THEN ''WARDTransferred''
WHEN ''ERDO'' THEN ''WARDExitedWithoutGraduation''
else ''WardActive'' END AS Graduation
from ovc_registration
INNER JOIN reg_person ON ovc_registration.person_id=reg_person.id
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id
LEFT OUTER JOIN list_geo ON list_geo.area_id=reg_persons_geo.area_id
WHERE reg_persons_geo.area_id > 337 and reg_persons_geo.is_void = False
and ovc_registration.child_cbo_id in ({cbos})
and ((ovc_registration.is_active = True and ovc_registration.registration_date <= ''{end_date}'' ) 
or (ovc_registration.is_active = False 
and (ovc_registration.registration_date between ''{start_date}'' and ''{end_date}'' )) 
or (ovc_registration.is_active = False and ovc_registration.registration_date <= ''{end_date}'' 
and ovc_registration.exit_date > ''{end_date}'' ) 
or (ovc_registration.is_active = False and ovc_registration.registration_date <= ''{end_date}'' 
and ovc_registration.exit_date between ''{start_date}'' and ''{end_date}'' )) 
and not (ovc_registration.school_level = ''SLNS''
and date_part(''year'', ''{end_date}''::date) - date_part(''year'', reg_person.date_of_birth::date) > 17)
group by exit_reason, list_geo.area_name order by ward) as wc
group by ward, graduation
   order by 1,2')
AS ct("ward" text, "WardActive" int, "WARDGraduated" int,
"WARDTransferred" int, "WARDExitedWithoutGraduation" int);;'''

# KPI
QUERIES['kpi'] = '''
select
cast(count(distinct ovc_registration.person_id) as integer) as OVCCount,
ovc_registration.child_cbo_id,
reg_org_unit.org_unit_name,
reg_persons_geo.area_id,
list_geo.area_name,
date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
CASE
WHEN date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
CASE ovc_care_health.art_status
WHEN 'ARAR' THEN '2a. (ii) OVC_HIVSTAT: HIV+ on ARV Treatment'
WHEN 'ARPR' THEN '2a. (ii) OVC_HIVSTAT: HIV+ on ARV Treatment'
ELSE '2a. (iii) OVC_HIVSTAT: HIV+ NOT on ARV Treatment'
END AS Domain
from ovc_registration
INNER JOIN reg_person ON ovc_registration.person_id=reg_person.id
LEFT OUTER JOIN reg_org_unit ON reg_org_unit.id=ovc_registration.child_cbo_id
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id
LEFT OUTER JOIN list_geo ON list_geo.area_id=reg_persons_geo.area_id
LEFT OUTER JOIN ovc_care_health ON ovc_care_health.person_id=ovc_registration.person_id
WHERE reg_persons_geo.area_id > 337 and reg_persons_geo.is_void = False
and ovc_registration.is_active = True
AND ovc_registration.hiv_status = 'HSTP'
%s
GROUP BY ovc_registration.person_id, reg_person.date_of_birth,
reg_person.sex_id, ovc_registration.child_cbo_id,
reg_org_unit.org_unit_name, reg_persons_geo.area_id,
ovc_registration.hiv_status, list_geo.area_name, ovc_care_health.art_status;'''

QUERIES['served'] = '''
SELECT * FROM (%s) a
INNER JOIN (%s) b
ON a.ward = b.ward;'''

# NOT SERVED LIST
QUERIES['not_served_list'] = '''
select person_id from(
select person_id, count(person_id) as scnts
from(
select person_id, domain, count(distinct(domain)) as domaincount from (
select ovc_registration.person_id, event_type_id, domain from ovc_care_assessment
inner join ovc_care_events on ovc_care_assessment.event_id=ovc_care_events.event
inner join ovc_registration on ovc_care_events.person_id = ovc_registration.person_id
where ovc_registration.child_cbo_id in ({cbos})
and domain in ('DHNU', 'DPSS')
and ovc_care_events.date_of_event between '{start_date}' and '{end_date}'
union all
select ovc_registration.person_id, event_type_id,
CASE
  WHEN (service_provided = 'SC1S' or service_provided = 'SC2S' or service_provided = 'SC3S'
     or service_provided = 'SC4S' or service_provided = 'SC5S' or service_provided = 'SC6S'
     or service_provided = 'SC7S') THEN 'DSHC'
  WHEN (service_provided = 'PS1S' or service_provided = 'PS2S' or service_provided = 'PS3S'
     or service_provided = 'PS4S' or service_provided = 'PS5S') THEN 'DPSS'
  WHEN (service_provided = 'PT1S' or service_provided = 'PT2S' or service_provided = 'PT3S'
     or service_provided = 'PT4S' or service_provided = 'PT5S') THEN 'DPRO'
  WHEN (service_provided = 'HE1S' or service_provided = 'HE2S' or service_provided = 'HE3S'
     or service_provided = 'HE4S') THEN 'DHES'
  WHEN (service_provided = 'HC1S' or service_provided = 'HC2S' or service_provided = 'HC3S'
     or service_provided = 'HC4S' or service_provided = 'HC5S' or service_provided = 'HC6S'
     or service_provided = 'HC7S' or service_provided = 'HC8S' or service_provided = 'HC9S'
     or service_provided = 'HC10S') THEN 'DHNU'
  WHEN (service_provided = 'SE1S' or service_provided = 'SE2S' or service_provided = 'SE3S'
     or service_provided = 'SE4S' or service_provided = 'SE5S' or service_provided = 'SE6S'
     or service_provided = 'SE7S' or service_provided = 'SE8S') THEN 'DEDU'
  ELSE 'NULL'
 END AS domain
from ovc_care_services
inner join ovc_care_events on ovc_care_services.event_id=ovc_care_events.event
inner join ovc_registration on ovc_care_events.person_id = ovc_registration.person_id
where ovc_registration.child_cbo_id in ({cbos})
and ovc_care_events.date_of_event between '{start_date}' and '{end_date}') as dcs
group by person_id, domain) as scounts
group by person_id) as fp where scnts > 0'''

# NOT Served
QUERIES['not_served'] = '''
select reg_org_unit.org_unit_name AS CBO,
reg_person.first_name, reg_person.surname,
reg_person.other_names, reg_person.date_of_birth, registration_date,
date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
date_part('year', age(ovc_registration.registration_date,
reg_person.date_of_birth)) AS age_at_reg,
child_cbo_id as OVCID,
list_geo.area_name as ward, scc.area_name as constituency, cc.area_name as county,
CASE
WHEN date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', 
age(reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
CASE has_bcert WHEN 'True' THEN 'HAS BIRTHCERT' ELSE 'NO BIRTHCERT' END AS BirthCert,
CASE has_bcert WHEN 'True' THEN 'BCERT' ELSE NULL END AS BCertNumber,
CASE is_disabled WHEN 'True' THEN 'HAS DISABILITY' ELSE 'NO DISABILITY' END AS OVCDisability,
CASE is_Disabled WHEN 'True' THEN 'NCPWD' ELSE NULL END AS NCPWDNumber,
CASE
WHEN hiv_status = 'HSTP' THEN 'POSITIVE'
WHEN hiv_status = 'HSTN' THEN 'NEGATIVE'
ELSE 'NOT KNOWN' END AS OVCHIVstatus,
CASE hiv_status WHEN 'HSTP' THEN 'ART' ELSE NULL END AS ARTStatus,
concat(chw.first_name,' ',chw.surname,' ',chw.other_names) as CHW,
concat(cgs.first_name,' ',cgs.surname,' ',cgs.other_names) as parent_names,
CASE is_active WHEN 'True' THEN 'ACTIVE' ELSE 'EXITED' END AS Exit_status,
CASE is_active WHEN 'False' THEN exit_date ELSE NULL END AS Exit_date,
CASE
WHEN school_level = 'SLTV' THEN 'Tertiary'
WHEN school_level = 'SLUN' THEN 'University'
WHEN school_level = 'SLSE' THEN 'Secondary'
WHEN school_level = 'SLPR' THEN 'Primary'
WHEN school_level = 'SLEC' THEN 'ECDE'
ELSE 'Not in School' END AS Schoollevel,
CASE immunization_status
WHEN 'IMFI' THEN 'Fully Immunized'
WHEN 'IMNI' THEN 'Not Immunized'
WHEN 'IMNC' THEN 'Not Completed'
ELSE 'Not Known' END AS immunization
from ovc_registration
left outer join reg_person on person_id=reg_person.id
left outer join reg_person chw on child_chv_id=chw.id
left outer join reg_person cgs on caretaker_id=cgs.id
left outer join reg_org_unit on child_cbo_id=reg_org_unit.id
left outer join reg_persons_geo on ovc_registration.person_id=reg_persons_geo.person_id
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
left outer join list_geo as cc on cc.area_id=scc.parent_area_id
where reg_persons_geo.area_id > 337 and reg_persons_geo.is_void = False
and child_cbo_id in ({cbos})
and ovc_registration.registration_date between '{start_date}' and '{end_date}'
and ovc_registration.person_id not in (%s);''' % (QUERIES['not_served_list'])


# PEPFAR DETAILED SUMMARY
QUERIES['pepfar_detailed'] = '''
select * FROM (
select cast('CBO' as text) as level,
CASE
WHEN scnts = 0 THEN 'Not Served' 
WHEN scnts = 1 THEN '1 or 2 Services' 
WHEN scnts = 2 THEN '1 or 2 Services' 
WHEN scnts > 2 THEN '3 or More Services' END AS Services,
Gender, age, AgeRange, CBO as name, count(scnts) AS OVCCOUNT from(
select person_id, count(person_id) as scnts, Gender, age, AgeRange, CBO
from(
select person_id, domain, Gender, age, AgeRange, CBO, count(distinct(domain)) as domaincount from (
select ovc_registration.person_id, event_type_id, domain,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
CASE
WHEN date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
reg_org_unit.org_unit_name AS CBO
 from ovc_care_assessment
inner join ovc_care_events on ovc_care_assessment.event_id=ovc_care_events.event
inner join ovc_registration on ovc_care_events.person_id=ovc_registration.person_id
inner join reg_person on reg_person.id = ovc_registration.person_id
left outer join reg_org_unit on ovc_registration.child_cbo_id=reg_org_unit.id
where domain in ('DHNU', 'DPSS')
and ovc_registration.child_cbo_id in ({cbos})
and ovc_care_events.date_of_event between '{start_date}' and '{end_date}'
union all
select ovc_registration.person_id, event_type_id,
CASE
  WHEN (service_provided = 'SC1S' or service_provided = 'SC2S' or service_provided = 'SC3S'
    or service_provided = 'SC4S' or service_provided = 'SC5S' or service_provided = 'SC6S'
    or service_provided = 'SC7S') THEN 'DSHC'
  WHEN (service_provided = 'PS1S' or service_provided = 'PS2S' or service_provided = 'PS3S'
    or service_provided = 'PS4S' or service_provided = 'PS5S') THEN 'DPSS'
  WHEN (service_provided = 'PT1S' or service_provided = 'PT2S' or service_provided = 'PT3S'
    or service_provided = 'PT4S' or service_provided = 'PT5S') THEN 'DPRO'
  WHEN (service_provided = 'HE1S' or service_provided = 'HE2S' or service_provided = 'HE3S'
    or service_provided = 'HE4S') THEN 'DHES'
  WHEN (service_provided = 'HC1S' or service_provided = 'HC2S' or service_provided = 'HC3S'
    or service_provided = 'HC4S' or service_provided = 'HC5S' or service_provided = 'HC6S'
    or service_provided = 'HC7S' or service_provided = 'HC8S' or service_provided = 'HC9S'
    or service_provided = 'HC10S') THEN 'DHNU'
  WHEN (service_provided = 'SE1S' or service_provided = 'SE2S' or service_provided = 'SE3S'
    or service_provided = 'SE4S' or service_provided = 'SE5S' or service_provided = 'SE6S'
    or service_provided = 'SE7S' or service_provided = 'SE8S') THEN 'DEDU'
  ELSE 'NULL'
 END AS domain,
 CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
 date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
 CASE
WHEN date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
reg_org_unit.org_unit_name AS CBO
from ovc_care_services
inner join ovc_care_events on ovc_care_services.event_id=ovc_care_events.event
inner join ovc_registration on ovc_care_events.person_id=ovc_registration.person_id
inner join reg_person on reg_person.id = ovc_registration.person_id
left outer join reg_org_unit on ovc_registration.child_cbo_id=reg_org_unit.id
where  ovc_care_events.date_of_event between '{start_date}' and '{end_date}'
and ovc_registration.child_cbo_id in ({cbos})) as dcs
group by person_id, domain, Gender, age, AgeRange, CBO) as scounts
group by person_id, Gender, age, AgeRange, CBO
union all
select ovc_registration.person_id, 0 as scnts,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
 date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
 CASE
WHEN date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
reg_org_unit.org_unit_name AS CBO
 from ovc_registration
 inner join reg_person on reg_person.id = ovc_registration.person_id
 left outer join reg_org_unit on ovc_registration.child_cbo_id=reg_org_unit.id
 where ovc_registration.child_cbo_id in ({cbos})
 ) as fp group by Gender, age, AgeRange, scnts, cbo) a
INNER JOIN (
select count(ovc_registration.person_id) as active,
reg_org_unit.org_unit_name as name
from ovc_registration
inner join reg_org_unit on reg_org_unit.id = ovc_registration.child_cbo_id
where ovc_registration.is_active = True
and ovc_registration.child_cbo_id in ({cbos})
group by ovc_registration.child_cbo_id, name) b
ON a.name = b.name;'''

# Blanks to fill up all services, ages, genders
QUERIES['pepfar_detailed_blank'] = '''
select * FROM (
select cast('CBO' as text) as level,
CASE
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) < 15 THEN cast('1 or 2 Services' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) BETWEEN 15 AND 28 THEN cast('3 or More Services' as text)
ELSE cast('Not Served' as text) END AS Services,
CASE
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (
1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41) THEN cast('Female' as text)
ELSE cast('Male' as text) END AS Gender,
0 as age,
CASE
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (1,2,15,16,29,30) THEN cast('a.[<1yrs]' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (3,4,16,17,31,32) THEN cast('b.[1-4yrs]' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (5,6,18,19,33,34) THEN cast('c.[5-9yrs]' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (7,8,20,21,35,36) THEN cast('d.[10-14yrs]' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (9,10,22,23,37,38) THEN cast('e.[15-17yrs]' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (11,12,24,25,39,40) THEN cast('f.[18-24yrs]' as text)
ELSE cast('g.[25+yrs]' as text) END AS AgeRange,
reg_org_unit.org_unit_name AS name,
0 as OVCCOUNT from ovc_registration
left outer join reg_org_unit on ovc_registration.child_cbo_id=reg_org_unit.id
where ovc_registration.child_cbo_id in ({cbos}) limit 42) a
INNER JOIN (
select count(ovc_registration.person_id) as active,
reg_org_unit.org_unit_name as name
from ovc_registration
inner join reg_org_unit on reg_org_unit.id = ovc_registration.child_cbo_id
where ovc_registration.is_active = True
and ovc_registration.child_cbo_id in ({cbos})
group by ovc_registration.child_cbo_id, name) b
ON a.name = b.name;'''

# For constituency
QUERIES['pepfar_detailed_1'] = '''
select * FROM (
select cast('Constituency' as text) as level,
CASE
WHEN scnts = 0 THEN 'Not Served' 
WHEN scnts = 1 THEN '1 or 2 Services' 
WHEN scnts = 2 THEN '1 or 2 Services' 
WHEN scnts > 2 THEN '3 or More Services' END AS Services,
Gender, age, AgeRange, scounty as name, count(scnts) AS OVCCOUNT from(
select person_id, count(person_id) as scnts, Gender, age, AgeRange, scounty
from(
select person_id, domain, Gender, age, AgeRange, scounty, count(distinct(domain)) as domaincount from (
select ovc_registration.person_id, event_type_id, domain,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
CASE
WHEN date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
scc.area_name AS scounty
 from ovc_care_assessment
inner join ovc_care_events on ovc_care_assessment.event_id=ovc_care_events.event
inner join ovc_registration on ovc_care_events.person_id=ovc_registration.person_id
inner join reg_person on reg_person.id = ovc_registration.person_id
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
where reg_persons_geo.area_id > 337 and reg_persons_geo.is_void = False
and domain in ('DHNU', 'DPSS')
and ovc_registration.child_cbo_id in ({cbos})
and ovc_care_events.date_of_event between '{start_date}' and '{end_date}'
union all
select ovc_registration.person_id, event_type_id,
CASE
  WHEN (service_provided = 'SC1S' or service_provided = 'SC2S' or service_provided = 'SC3S'
    or service_provided = 'SC4S' or service_provided = 'SC5S' or service_provided = 'SC6S'
    or service_provided = 'SC7S') THEN 'DSHC'
  WHEN (service_provided = 'PS1S' or service_provided = 'PS2S' or service_provided = 'PS3S'
    or service_provided = 'PS4S' or service_provided = 'PS5S') THEN 'DPSS'
  WHEN (service_provided = 'PT1S' or service_provided = 'PT2S' or service_provided = 'PT3S'
    or service_provided = 'PT4S' or service_provided = 'PT5S') THEN 'DPRO'
  WHEN (service_provided = 'HE1S' or service_provided = 'HE2S' or service_provided = 'HE3S'
    or service_provided = 'HE4S') THEN 'DHES'
  WHEN (service_provided = 'HC1S' or service_provided = 'HC2S' or service_provided = 'HC3S'
    or service_provided = 'HC4S' or service_provided = 'HC5S' or service_provided = 'HC6S'
    or service_provided = 'HC7S' or service_provided = 'HC8S' or service_provided = 'HC9S'
    or service_provided = 'HC10S') THEN 'DHNU'
  WHEN (service_provided = 'SE1S' or service_provided = 'SE2S' or service_provided = 'SE3S'
    or service_provided = 'SE4S' or service_provided = 'SE5S' or service_provided = 'SE6S'
    or service_provided = 'SE7S' or service_provided = 'SE8S') THEN 'DEDU'
  ELSE 'NULL'
 END AS domain,
 CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
 date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
 CASE
WHEN date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
scc.area_name AS scounty
from ovc_care_services
inner join ovc_care_events on ovc_care_services.event_id=ovc_care_events.event
inner join ovc_registration on ovc_care_events.person_id=ovc_registration.person_id
inner join reg_person on reg_person.id = ovc_registration.person_id
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
where reg_persons_geo.area_id > 337 and reg_persons_geo.is_void = False
and ovc_care_events.date_of_event between '{start_date}' and '{end_date}'
and ovc_registration.child_cbo_id in ({cbos})) as dcs
group by person_id, domain, Gender, age, AgeRange, scounty) as scounts
group by person_id, Gender, age, AgeRange, scounty
union all
select ovc_registration.person_id, 0 as scnts,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
 date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
 CASE
WHEN date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
scc.area_name AS scounty
 from ovc_registration
 inner join reg_person on reg_person.id = ovc_registration.person_id
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
where reg_persons_geo.area_id > 337 and reg_persons_geo.is_void = False
and ovc_registration.child_cbo_id in ({cbos})
 ) as fp group by Gender, age, AgeRange, scnts, scounty) a
INNER JOIN (
select count(ovc_registration.person_id) as active,
scc.area_name as name
from ovc_registration
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
where reg_persons_geo.area_id > 337 and reg_persons_geo.is_void = False
and ovc_registration.is_active = True
and ovc_registration.child_cbo_id in ({cbos})
group by name) b
ON a.name = b.name;'''

# For consituency blanks
QUERIES['pepfar_detailed_blank_1'] = '''
select * FROM (
select cast('Constituency' as text) as level,
CASE
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) < 15 THEN cast('1 or 2 Services' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) BETWEEN 15 AND 28 THEN cast('3 or More Services' as text)
ELSE cast('Not Served' as text) END AS Services,
CASE
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (
1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41) THEN cast('Female' as text)
ELSE cast('Male' as text) END AS Gender,
0 as age,
CASE
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (1,2,15,16,29,30) THEN cast('a.[<1yrs]' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (3,4,16,17,31,32) THEN cast('b.[1-4yrs]' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (5,6,18,19,33,34) THEN cast('c.[5-9yrs]' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (7,8,20,21,35,36) THEN cast('d.[10-14yrs]' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (9,10,22,23,37,38) THEN cast('e.[15-17yrs]' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (11,12,24,25,39,40) THEN cast('f.[18-24yrs]' as text)
ELSE cast('g.[25+yrs]' as text) END AS AgeRange,
scc.area_name AS name,
0 as OVCCOUNT from ovc_registration
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
where reg_persons_geo.area_id > 337 and reg_persons_geo.is_void = False
and ovc_registration.child_cbo_id in ({cbos}) limit 42) a
INNER JOIN (
select count(ovc_registration.person_id) as active,
scc.area_name as name
from ovc_registration
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
where reg_persons_geo.area_id > 337 and reg_persons_geo.is_void = False
and ovc_registration.is_active = True
and ovc_registration.child_cbo_id in ({cbos})
group by name) b
ON a.name = b.name;'''

# For County
QUERIES['pepfar_detailed_2'] = '''
select * FROM (
select cast('County' as text) as level,
CASE
WHEN scnts = 0 THEN 'Not Served' 
WHEN scnts = 1 THEN '1 or 2 Services' 
WHEN scnts = 2 THEN '1 or 2 Services' 
WHEN scnts > 2 THEN '3 or More Services' END AS Services,
Gender, age, AgeRange, scounty as name, count(scnts) AS OVCCOUNT from(
select person_id, count(person_id) as scnts, Gender, age, AgeRange, scounty
from(
select person_id, domain, Gender, age, AgeRange, scounty, count(distinct(domain)) as domaincount from (
select ovc_registration.person_id, event_type_id, domain,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
CASE
WHEN date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
cc.area_name AS scounty
 from ovc_care_assessment
inner join ovc_care_events on ovc_care_assessment.event_id=ovc_care_events.event
inner join ovc_registration on ovc_care_events.person_id=ovc_registration.person_id
inner join reg_person on reg_person.id = ovc_registration.person_id
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
left outer join list_geo as cc on cc.area_id=scc.parent_area_id
where reg_persons_geo.area_id > 337 and reg_persons_geo.is_void = False
and domain in ('DHNU', 'DPSS')
and ovc_registration.child_cbo_id in ({cbos})
and ovc_care_events.date_of_event between '{start_date}' and '{end_date}'
union all
select ovc_registration.person_id, event_type_id,
CASE
  WHEN (service_provided = 'SC1S' or service_provided = 'SC2S' or service_provided = 'SC3S'
    or service_provided = 'SC4S' or service_provided = 'SC5S' or service_provided = 'SC6S'
    or service_provided = 'SC7S') THEN 'DSHC'
  WHEN (service_provided = 'PS1S' or service_provided = 'PS2S' or service_provided = 'PS3S'
    or service_provided = 'PS4S' or service_provided = 'PS5S') THEN 'DPSS'
  WHEN (service_provided = 'PT1S' or service_provided = 'PT2S' or service_provided = 'PT3S'
    or service_provided = 'PT4S' or service_provided = 'PT5S') THEN 'DPRO'
  WHEN (service_provided = 'HE1S' or service_provided = 'HE2S' or service_provided = 'HE3S'
    or service_provided = 'HE4S') THEN 'DHES'
  WHEN (service_provided = 'HC1S' or service_provided = 'HC2S' or service_provided = 'HC3S'
    or service_provided = 'HC4S' or service_provided = 'HC5S' or service_provided = 'HC6S'
    or service_provided = 'HC7S' or service_provided = 'HC8S' or service_provided = 'HC9S'
    or service_provided = 'HC10S') THEN 'DHNU'
  WHEN (service_provided = 'SE1S' or service_provided = 'SE2S' or service_provided = 'SE3S'
    or service_provided = 'SE4S' or service_provided = 'SE5S' or service_provided = 'SE6S'
    or service_provided = 'SE7S' or service_provided = 'SE8S') THEN 'DEDU'
  ELSE 'NULL'
 END AS domain,
 CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
 date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
 CASE
WHEN date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
cc.area_name AS scounty
from ovc_care_services
inner join ovc_care_events on ovc_care_services.event_id=ovc_care_events.event
inner join ovc_registration on ovc_care_events.person_id=ovc_registration.person_id
inner join reg_person on reg_person.id = ovc_registration.person_id
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
left outer join list_geo as cc on cc.area_id=scc.parent_area_id
where reg_persons_geo.area_id > 337 and reg_persons_geo.is_void = False
and ovc_care_events.date_of_event between '{start_date}' and '{end_date}'
and ovc_registration.child_cbo_id in ({cbos})) as dcs
group by person_id, domain, Gender, age, AgeRange, scounty) as scounts
group by person_id, Gender, age, AgeRange, scounty
union all
select ovc_registration.person_id, 0 as scnts,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
 date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
 CASE
WHEN date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
cc.area_name AS scounty
 from ovc_registration
 inner join reg_person on reg_person.id = ovc_registration.person_id
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
left outer join list_geo as cc on cc.area_id=scc.parent_area_id
where reg_persons_geo.area_id > 337 and reg_persons_geo.is_void = False
and ovc_registration.child_cbo_id in ({cbos})
 ) as fp group by Gender, age, AgeRange, scnts, scounty) a
INNER JOIN (
select count(ovc_registration.person_id) as active,
cc.area_name as name
from ovc_registration
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
left outer join list_geo as cc on cc.area_id=scc.parent_area_id
where reg_persons_geo.area_id > 337 and reg_persons_geo.is_void = False
and ovc_registration.is_active = True
and ovc_registration.child_cbo_id in ({cbos})
group by name) b
ON a.name = b.name;'''

# For county blank
QUERIES['pepfar_detailed_blank_2'] = '''
select * FROM (
select cast('County' as text) as level,
CASE
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) < 15 THEN cast('1 or 2 Services' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) BETWEEN 15 AND 28 THEN cast('3 or More Services' as text)
ELSE cast('Not Served' as text) END AS Services,
CASE
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (
1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41) THEN cast('Female' as text)
ELSE cast('Male' as text) END AS Gender,
0 as age,
CASE
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (1,2,15,16,29,30) THEN cast('a.[<1yrs]' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (3,4,16,17,31,32) THEN cast('b.[1-4yrs]' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (5,6,18,19,33,34) THEN cast('c.[5-9yrs]' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (7,8,20,21,35,36) THEN cast('d.[10-14yrs]' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (9,10,22,23,37,38) THEN cast('e.[15-17yrs]' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (11,12,24,25,39,40) THEN cast('f.[18-24yrs]' as text)
ELSE cast('g.[25+yrs]' as text) END AS AgeRange,
cc.area_name AS name,
0 as OVCCOUNT from ovc_registration
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
left outer join list_geo as cc on cc.area_id=scc.parent_area_id
where reg_persons_geo.area_id > 337 and reg_persons_geo.is_void = False
and ovc_registration.child_cbo_id in ({cbos}) limit 42) a
INNER JOIN (
select count(ovc_registration.person_id) as active,
cc.area_name as name
from ovc_registration
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
left outer join list_geo as cc on cc.area_id=scc.parent_area_id
where reg_persons_geo.area_id > 337 and reg_persons_geo.is_void = False
and ovc_registration.is_active = True
and ovc_registration.child_cbo_id in ({cbos})
group by name) b
ON a.name = b.name;'''

#  Constituency active
'''
select count(ovc_registration.person_id),
list_geo.area_name as ward,
list_geo.parent_area_id as sc, scc.area_name as sc_name,
scc.parent_area_id as cid, cc.area_name as county
from ovc_registration
left outer join reg_org_unit on child_cbo_id=reg_org_unit.id
left outer join reg_person on person_id=reg_person.id
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
left outer join list_geo as cc on cc.area_id=scc.parent_area_id
where reg_persons_geo.area_id > 337 and reg_persons_geo.is_void = False
and ovc_registration.is_active = True
group by ovc_registration.child_cbo_id, ward, sc, sc_name, cid, county
'''
QUERIES['form1b_summary'] = '''
'''



# List of OVC Served

# List of OVC Served
QUERIES['ovc_served_list'] = '''
select * from vw_cpims_list_served where cbo_id in ({cbos})
AND date_of_service between '{start_date}' and '{end_date}'
AND service != '' and service is not null;
'''




QUERIES['pivot_report'] = '''
select
cou_geo.area_name as "County",
scou_geo.area_name as "Sub County",
reg_org_unit.org_unit_name as "Organization Unit",
ou_type.item_description as "Unit Type",
c_cat.item_description as "Category",
TO_CHAR(ovc_case_record.date_case_opened :: DATE, 'dd-Mon-yyyy') as "Case Date",
to_char(date_case_opened, 'YYYY')::INTEGER as "Year",
TO_CHAR(date_case_opened :: DATE, 'MM-Mon') as "Month",
case
when to_char(date_case_opened, 'MM')::INTEGER BETWEEN 1 AND 3 THEN 3
when to_char(date_case_opened, 'MM')::INTEGER BETWEEN 4 AND 6 THEN 4
when to_char(date_case_opened, 'MM')::INTEGER BETWEEN 7 AND 9 THEN 1
else 2 end as "Qtr",
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS "Sex",
date_part('year', age(date_case_opened, reg_person.date_of_birth)) AS "Age",
CASE
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) < 6 THEN 'a.[0 - 5 yrs]'
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 6 AND 9 THEN 'b.[6 - 9 yrs]' 
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 10 AND 15 THEN 'c.[10 - 15 yrs]' 
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 16 AND 18 THEN 'd.[16 - 18 yrs]' 
ELSE 'e.[18+ yrs]' END AS "Age Set",
CASE
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) < 5 THEN 'a.[0 - 4 yrs]'
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'b.[5 - 9 yrs]' 
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'c.[10 - 14 yrs]' 
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 15 AND 18 THEN 'd.[15 - 18 yrs]' 
ELSE 'e.[18+ yrs]' END AS "KNBS Age Set",
CASE case_stage WHEN 2 THEN 'Closed' WHEN 1 THEN 'Active' ELSE 'Pending' END AS "Case Status",
case_status as "Case State",
TO_CHAR(ovc_case_record.timestamp_created :: DATE, 'dd-Mon-yyyy') as "System Date",
1 as "OVCCount"
from ovc_case_record
inner join ovc_case_category as ccat on case_id = ccat.case_id_id
inner join ovc_case_geo as cgeo on cgeo.case_id_id = case_id
left outer join reg_person on ovc_case_record.person_id=reg_person.id
left outer join reg_org_unit on reg_org_unit.id=cgeo.report_orgunit_id
left outer join list_geo as scou_geo on scou_geo.area_id=cgeo.report_subcounty_id and scou_geo.area_id > 47
left outer join list_geo as cou_geo on cou_geo.area_id=scou_geo.parent_area_id and cou_geo.area_id < 48
left outer join ovc_case_sub_category cscat on cscat.case_category_id=ccat.case_category_id
left outer join list_general c_cat on c_cat.item_id=ccat.case_category and c_cat.field_name = 'case_category_id'
left outer join list_general ou_type on ou_type.item_id=reg_org_unit.org_unit_type_id
where date_case_opened between '{start_date}' and '{end_date}' {extras}
'''
# GOK Newest Reports
QUERIES['services'] = '''
select ocr.person_id as cpims_id,
CASE pp.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Sex,
date_part('year', age(ocr.date_case_opened, pp.date_of_birth)) AS "Admission Age",
cee.service_provided,
CASE
WHEN  date_part('year', age(ocr.date_case_opened, pp.date_of_birth)) < 6 THEN 'a.[0 - 5 yrs]'
WHEN  date_part('year', age(ocr.date_case_opened, pp.date_of_birth)) BETWEEN 6 AND 9 THEN 'b.[6 - 9 yrs]' 
WHEN  date_part('year', age(ocr.date_case_opened, pp.date_of_birth)) BETWEEN 10 AND 15 THEN 'c.[10 - 15 yrs]' 
WHEN  date_part('year', age(ocr.date_case_opened, pp.date_of_birth)) BETWEEN 16 AND 18 THEN 'd.[16 - 18 yrs]' 
ELSE 'e.[18+ yrs]' END AS agerange,
c_cat.item_description as "case category",
cee.date_of_encounter_event as service_date, 1 as ovccount
from ovc_case_event_encounters as cee
inner join ovc_case_events ce on ce.case_event_id = cee.case_event_id_id
inner join ovc_case_record ocr on ce.case_id_id = ocr.case_id
inner join reg_person as pp on ocr.person_id = pp.id
inner join ovc_case_category as ccat on case_id = ocr.case_id
inner join ovc_case_geo as cgeo on cgeo.case_id_id = ocr.case_id
left outer join list_general c_cat on c_cat.item_id=ccat.case_category and c_cat.field_name = 'case_category_id'
where ce.date_of_event between '{start_date}' and '{end_date}' {other_params}
'''
# Institution population detailed report to handle origin of CRS
QUERIES['institution_population'] = '''
SELECT
ROW_NUMBER () OVER (ORDER BY ovc_placement.timestamp_created) as SNO,
pp.id as CPIMS_ID,
date_part('year', age(admission_date, pp.date_of_birth)) AS "Admission Age",
CASE admission_reason WHEN 'RAOF' THEN 'Offender' ELSE 'C & P' END AS "Admission Reason",
a_type.item_description as "Admission Type",
CASE has_court_committal_order WHEN 'AYES' THEN 'Yes' ELSE 'No' END AS "Has Court CO",
CASE pp.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Sex,
admission_date as "admission date", df.date_of_discharge as "discharge date",
CASE
WHEN  date_part('year', age(admission_date, pp.date_of_birth)) < 6 THEN 'a.[0 - 5 yrs]'
WHEN  date_part('year', age(admission_date, pp.date_of_birth)) BETWEEN 6 AND 9 THEN 'b.[6 - 9 yrs]' 
WHEN  date_part('year', age(admission_date, pp.date_of_birth)) BETWEEN 10 AND 15 THEN 'c.[10 - 15 yrs]' 
WHEN  date_part('year', age(admission_date, pp.date_of_birth)) BETWEEN 16 AND 18 THEN 'd.[16 - 18 yrs]' 
ELSE 'e.[18+ yrs]' END AS agerange,
c_cat.item_description as "case category",
reg_org_unit.org_unit_name as org_unit,
cou_geo.area_name as county, scou_geo.area_name as sub_county,
CASE ovc_placement.is_active WHEN 'TRUE' THEN 'Active' ELSE 'Discharged' END AS Status,
1 as ovccount
from ovc_placement
inner join reg_person as pp on person_id = pp.id
left outer join ovc_case_record as cr on cr.case_id = ovc_placement.case_record_id
left outer join ovc_case_category as cc on cc.case_id_id = cr.case_id
left outer join list_general c_cat on c_cat.item_id=cc.case_category and c_cat.field_name = 'case_category_id'
left outer join list_general a_type on a_type.item_id=ovc_placement.admission_type and a_type.field_name = 'admission_type_id'
left outer join ovc_discharge_followup as df on df.placement_id_id = ovc_placement.placement_id
left outer join ovc_case_geo as cgeo on cgeo.case_id_id = ovc_placement.case_record_id
left outer join reg_org_unit on reg_org_unit.id=cgeo.report_orgunit_id
left outer join list_geo as scou_geo on scou_geo.area_id=cgeo.report_subcounty_id and scou_geo.area_id > 47
left outer join list_geo as cou_geo on cou_geo.area_id=scou_geo.parent_area_id and cou_geo.area_id < 48
where ovc_placement.is_void = False and admission_date between '{start_date}' and '{end_date}'
and residential_institution_id IN ({org_unit})
'''
# Trafficking in Persons Report
QUERIES['tip'] = '''
select case_serial as "Case Number",
ROW_NUMBER () OVER (ORDER BY ovc_case_record.timestamp_created) as Serial,
cou_geo.area_name as County, scou_geo.area_name as SubCounty,
date_case_opened as Date, c_cat.item_description as "Case Category",
cs_cat.item_description as "Case sub category",
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Sex,
date_part('year', age(date_case_opened, reg_person.date_of_birth)) AS Age,
CASE
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) < 6 THEN 'a.[0 - 5 yrs]'
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 6 AND 9 THEN 'b.[6 - 9 yrs]' 
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 10 AND 15 THEN 'c.[10 - 15 yrs]' 
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 16 AND 18 THEN 'd.[16 - 18 yrs]' 
ELSE 'e.[18+ yrs]' END AS AgeRange,
NULL as "Case Intervention",
TO_CHAR(reg_person.date_of_birth :: DATE, 'dd-Mon-yyyy') as "Date of Birth",
1 as ovccount
from ovc_case_record
inner join ovc_case_category as ccat on case_id = ccat.case_id_id
inner join ovc_case_geo as cgeo on cgeo.case_id_id = case_id
left outer join reg_person on ovc_case_record.person_id=reg_person.id
left outer join list_geo as scou_geo on scou_geo.area_id=cgeo.report_subcounty_id and scou_geo.area_id > 47
left outer join list_geo as cou_geo on cou_geo.area_id=scou_geo.parent_area_id and cou_geo.area_id < 48
left outer join list_general c_cat on c_cat.item_id=ccat.case_category and c_cat.field_name = 'case_category_id'
left outer join ovc_case_sub_category cscat on cscat.case_category_id=ccat.case_category_id
left outer join list_general cs_cat on cs_cat.item_id=cscat.sub_category_id
where ccat.case_category in ('CSTC', 'CTRF')
and date_case_opened between '{start_date}' and '{end_date}'
ORDER BY ovc_case_record.timestamp_created ASC;
'''
# Registers
QUERIES['cases_hl'] = '''
SELECT case_serial, 
case when TRIM(c_cat.item_description) is null then 'Not Available' 
WHEN TRIM(c_cat.item_description) = '' THEN 'Not Available' else c_cat.item_description end as "Case Category",
CASE obp.sex WHEN 'SFEM' THEN 'Female' WHEN 'SMAL' THEN 'Male' ELSE 'Uknown' END AS Sex,
CASE
WHEN  date_part('year', age(obcr.case_date, obp.dob)) < 6 THEN 'a.[0 - 5 yrs]'
WHEN  date_part('year', age(obcr.case_date, obp.dob)) BETWEEN 6 AND 9 THEN 'b.[6 - 9 yrs]' 
WHEN  date_part('year', age(obcr.case_date, obp.dob)) BETWEEN 10 AND 15 THEN 'c.[10 - 15 yrs]' 
WHEN  date_part('year', age(obcr.case_date, obp.dob)) BETWEEN 16 AND 18 THEN 'd.[16 - 18 yrs]' 
ELSE 'e.[18+ yrs]' END AS AgeRange,
case_date, county as county_id, constituency as constituency_id,
cou_geo.area_name as "county", scou_geo.area_name as "constituency",
case_landmark, case_narration, longitude, latitude, reporter_telephone,
CASE risk_level WHEN 'RLHG' THEN 'High' WHEN 'RLMD' THEN 'Medium' ELSE 'Low' END AS risk_level,
CASE status WHEN 0 THEN 'Pending' ELSE 'In Action' END AS "Case Status",
1 as ovccount, obcr.timestamp_created
FROM ovc_basic_case_record obcr
left outer join ovc_basic_category obc on obc.case_id=obcr.case_id
left outer join list_general c_cat on c_cat.item_id=obc.case_category and c_cat.field_name = 'case_category_id'
left outer join list_geo as scou_geo on scou_geo.area_code::int=constituency::int and scou_geo.area_id > 47 and scou_geo.area_id < 337
left outer join list_geo as cou_geo on cou_geo.area_id=scou_geo.parent_area_id and cou_geo.area_id < 48
left outer join ovc_basic_person obp on obp.case_id=obcr.case_id
WHERE obp.relationship = 'TBVC'
'''

QUERIES['case_load_register'] = '''
select ovc_case_record.person_id as cpims_id,
concat(reg_person.first_name, ' ', reg_person.surname, ' ', reg_person.other_names) as names,
TO_CHAR(date_case_opened :: DATE, 'dd-Mon-yyyy') as case_date,
to_char(date_case_opened, 'YYYY')::INTEGER as "case_year",
TO_CHAR(date_case_opened :: DATE, 'MM-Mon') as "case_month",
case
when to_char(date_case_opened, 'MM')::INTEGER BETWEEN 1 AND 3 THEN 3
when to_char(date_case_opened, 'MM')::INTEGER BETWEEN 4 AND 6 THEN 4
when to_char(date_case_opened, 'MM')::INTEGER BETWEEN 7 AND 9 THEN 1
else 2 end as "case_qtr",
case_serial, concat(case_serial,' - ',c_cat.item_description) as serial_case_category,
CASE risk_level WHEN 'RLHG' THEN 'High' WHEN 'RLMD' THEN 'Medium' ELSE 'Low' END AS risk_level,
CASE perpetrator_status WHEN 'PSSL' THEN 'Self' WHEN 'PKNW' THEN 'Unknown'
WHEN 'PUNK' THEN 'Unknown' ELSE 'Not Available' END AS perpetrator_status,
cr_cat.item_description as case_reporter,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS sex,
date_part('year', age(date_case_opened, reg_person.date_of_birth)) AS age,
CASE
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) < 6 THEN 'a.[0 - 5 yrs]'
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 6 AND 9 THEN 'b.[6 - 9 yrs]' 
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 10 AND 15 THEN 'c.[10 - 15 yrs]' 
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 16 AND 18 THEN 'd.[16 - 18 yrs]' 
ELSE 'e.[18+ yrs]' END AS agerange,
CASE
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) < 5 THEN 'a.[0 - 4 yrs]'
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'b.[5 - 9 yrs]' 
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'c.[10 - 14 yrs]' 
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 15 AND 18 THEN 'd.[15 - 18 yrs]' 
ELSE 'e.[18+ yrs]' END AS knbs_agerange,
CASE case_stage WHEN 2 THEN 'Closed' WHEN 1 THEN 'Active' ELSE 'Pending' END AS Case_status,
case_status as case_state,
CASE ccat.case_nature WHEN 'OOEV' THEN 'One Off' ELSE 'Chronic' END AS Case_Nature,
ev_cat.item_description as place_of_event, c_cat.item_description as "case category",
cs_cat.item_description as case_sub_category,
reg_org_unit.org_unit_name as org_unit, scou_geo.area_name as sub_county,
cou_geo.area_name as county,
case omed.mental_condition when 'MNRM' THEN 'Normal' else 'Has Condition' End as mental_condition,
case omed.physical_condition when 'PNRM' THEN 'Normal' else 'Has Condition' End as physical_condition,
case omed.other_condition when 'CHNM' THEN 'Normal' else 'Has Condition' End as other_condition,
CASE cen.service_provided WHEN cen.service_provided THEN intv.item_description ELSE 'Case Open' END AS intervention,
TO_CHAR(ovc_case_record.timestamp_created :: DATE, 'dd-Mon-yyyy') as system_date,
1 as ovccount
from ovc_case_record
inner join ovc_case_category as ccat on case_id = ccat.case_id_id
inner join ovc_case_geo as cgeo on cgeo.case_id_id = case_id
inner join ovc_medical as omed on omed.case_id_id = case_id
left outer join reg_person on ovc_case_record.person_id=reg_person.id
left outer join reg_org_unit on reg_org_unit.id=cgeo.report_orgunit_id
left outer join list_geo as scou_geo on scou_geo.area_id=cgeo.report_subcounty_id and scou_geo.area_id > 47
left outer join list_geo as cou_geo on cou_geo.area_id=scou_geo.parent_area_id and cou_geo.area_id < 48
left outer join ovc_case_sub_category cscat on cscat.case_category_id=ccat.case_category_id
left outer join list_general c_cat on c_cat.item_id=ccat.case_category and c_cat.field_name = 'case_category_id'
left outer join list_general ev_cat on ev_cat.item_id=ccat.place_of_event and ev_cat.field_name = 'event_place_id'
left outer join list_general cr_cat on cr_cat.item_id=case_reporter and cr_cat.field_name = 'case_reporter_id'
left outer join list_general cs_cat on cs_cat.item_id=cscat.sub_category_id
left join ovc_case_events as cev on cev.case_id_id = case_id and cev.case_event_type_id = 'CLOSURE' and cev.is_void = false
left join ovc_case_event_encounters as cen on cen.case_event_id_id=cev.case_event_id
left outer join list_general intv on intv.item_id=cen.service_provided and intv.field_name = 'intervention_id'
where date_case_opened between '{start_date}' and '{end_date}' {other_params};
'''
# Trafficking in Persons Report - New
QUERIES['tip_new'] = '''
select ROW_NUMBER () OVER (ORDER BY ocr.timestamp_created) as Serial,
case_serial as "Case Number", ocr.person_id as CPIMS_ID,
cou_geo.area_name as County, scou_geo.area_name as SubCounty,
date_case_opened as Date, c_cat.item_description as "Case Category",
cs_cat.item_description as "Case sub category",
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Sex,
TO_CHAR(reg_person.date_of_birth :: DATE, 'dd-Mon-yyyy') as "Date of Birth",
date_part('year', age(date_case_opened, reg_person.date_of_birth)) AS Age,
CASE
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) < 6 THEN 'a.[0 - 5 yrs]'
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 6 AND 9 THEN 'b.[6 - 9 yrs]' 
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 10 AND 15 THEN 'c.[10 - 15 yrs]' 
WHEN  date_part('year', age(date_case_opened, reg_person.date_of_birth)) BETWEEN 16 AND 18 THEN 'd.[16 - 18 yrs]' 
ELSE 'e.[18+ yrs]' END AS AgeRange,
NULL as "Case Intervention",
1 as ovccount
from ovc_case_record as ocr
inner join ovc_case_category as ccat on ocr.case_id = ccat.case_id_id
inner join ovc_case_geo as cgeo on cgeo.case_id_id = ocr.case_id
inner join ovc_ctip_main as tip_main on tip_main.case_id = ocr.case_id
left outer join reg_person on ocr.person_id=reg_person.id
left outer join list_geo as scou_geo on scou_geo.area_id=cgeo.report_subcounty_id and scou_geo.area_id > 47
left outer join list_geo as cou_geo on cou_geo.area_id=scou_geo.parent_area_id and cou_geo.area_id < 48
left outer join list_general c_cat on c_cat.item_id=ccat.case_category and c_cat.field_name = 'case_category_id'
left outer join ovc_case_sub_category cscat on cscat.case_category_id=ccat.case_category_id
left outer join list_general cs_cat on cs_cat.item_id=cscat.sub_category_id
where date_case_opened between '{start_date}' and '{end_date}' {other_params}
ORDER BY ocr.timestamp_created ASC;
'''

QUERIES['u_case_load'] = '''
select ocr.person_id as cpims_id,
CASE rp.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS sex,
date_part('year', age(ocr.date_case_opened, rp.date_of_birth)) AS age,
CASE
WHEN  date_part('year', age(date_case_opened, rp.date_of_birth)) < 6 THEN 'a.[0 - 5 yrs]'
WHEN  date_part('year', age(date_case_opened, rp.date_of_birth)) BETWEEN 6 AND 9 THEN 'b.[6 - 9 yrs]' 
WHEN  date_part('year', age(date_case_opened, rp.date_of_birth)) BETWEEN 10 AND 15 THEN 'c.[10 - 15 yrs]' 
WHEN  date_part('year', age(date_case_opened, rp.date_of_birth)) BETWEEN 16 AND 18 THEN 'd.[16 - 18 yrs]' 
ELSE 'e.[18+ yrs]' END AS agerange,
TO_CHAR(ocr.date_case_opened :: DATE, 'dd-Mon-yyyy') as case_date,
to_char(ocr.date_case_opened, 'YYYY')::INTEGER as "case_year",
TO_CHAR(ocr.date_case_opened :: DATE, 'MM-Mon') as "case_month",
c_cat.item_description as case_category,
string_agg(cs_cat.item_description, ',') as case_sub_categories,
CASE ocr.case_stage WHEN 2 THEN 'Closed' WHEN 1 THEN 'Active' ELSE 'Pending' END AS Case_status,
ous.item_description as org_unit_type, ou.org_unit_name as org_unit,
cou_geo.area_name as county, scou_geo.area_name as sub_county,
CASE cen.service_provided WHEN cen.service_provided THEN intv.item_description ELSE 'Case Open' END AS intervention,
TO_CHAR(ocr.timestamp_created :: DATE, 'dd-Mon-yyyy') as system_date,
1 as ovccount
from ovc_case_record ocr
inner join ovc_case_category as ccat on case_id = ccat.case_id_id
inner join ovc_case_geo as cgeo on cgeo.case_id_id = case_id
inner join ovc_medical as omed on omed.case_id_id = case_id
left outer join reg_person rp on ocr.person_id=rp.id
left outer join list_geo as scou_geo on scou_geo.area_id=cgeo.report_subcounty_id and scou_geo.area_id > 47
left outer join list_geo as cou_geo on cou_geo.area_id=scou_geo.parent_area_id and cou_geo.area_id < 48
left outer join reg_org_unit as ou on ou.id=cgeo.report_orgunit_id
left outer join ovc_case_sub_category ocsc on ocsc.case_category_id = ccat.case_category_id
left outer join list_general c_cat on c_cat.item_id=ccat.case_category and c_cat.field_name = 'case_category_id'
inner join list_general cs_cat on cs_cat.item_id=ocsc.sub_category_id
left join ovc_case_events as cev on cev.case_id_id = case_id and cev.case_event_type_id = 'CLOSURE' and cev.is_void = false
left join ovc_case_event_encounters as cen on cen.case_event_id_id=cev.case_event_id
left outer join list_general intv on intv.item_id=cen.service_provided and intv.field_name = 'intervention_id'
left outer join list_general ous on ous.item_id=ou.org_unit_type_id
where date_case_opened between '{start_date}' and '{end_date}' {other_params}
group by ocr.person_id, ocr.date_case_opened, rp.sex_id, ous.item_description,
rp.date_of_birth, c_cat.item_description, ou.org_unit_name,
scou_geo.area_name, cou_geo.area_name, ocr.case_stage, ocr.timestamp_created,
cen.service_provided, intv.item_description
'''

# AFC Reports
QUERIES['afc_summary'] = '''
SELECT
ROW_NUMBER () OVER (ORDER BY ovc_afc_main.timestamp_created) as SNO,
concat(pp.first_name,' ',pp.surname,' ',pp.other_names) as Names,
date_part('year', age(case_date, pp.date_of_birth)) AS Age,
CASE pp.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Sex,
case_date as "case date",
CASE
WHEN  date_part('year', age(case_date, pp.date_of_birth)) < 6 THEN 'a.[0 - 5 yrs]'
WHEN  date_part('year', age(case_date, pp.date_of_birth)) BETWEEN 6 AND 9 THEN 'b.[6 - 9 yrs]' 
WHEN  date_part('year', age(case_date, pp.date_of_birth)) BETWEEN 10 AND 15 THEN 'c.[10 - 15 yrs]' 
WHEN  date_part('year', age(case_date, pp.date_of_birth)) BETWEEN 16 AND 18 THEN 'd.[16 - 18 yrs]' 
ELSE 'e.[18+ yrs]' END AS agerange,
c_type.item_description as "care type",
c_cat.item_description as "case category",
CASE ovc_afc_main.case_status WHEN 'TRUE' THEN 'Active' ELSE 'Closed' END AS Status,
1 as ovccount
from ovc_afc_main
inner join reg_person as pp on person_id = pp.id
left outer join ovc_case_record as cr on cr.case_id = ovc_afc_main.case_id
left outer join ovc_case_category as cc on cc.case_id_id = cr.case_id
left outer join list_general c_cat on c_cat.item_id=cc.case_category and c_cat.field_name = 'case_category_id'
left outer join list_general c_type on c_type.item_id=ovc_afc_main.care_type and c_type.field_name = 'alternative_family_care_type_id'
where ovc_afc_main.is_void = False and case_date between '{start_date}' and '{end_date}'
and org_unit_id = '{org_unit}'
'''

QUERIES['afc_identification'] = '''
SELECT pp.id as cpims_id, event_date as Identification_date,
CASE pp.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Sex,
date_part('year', age(event_date, pp.date_of_birth)) AS Age,
CASE
WHEN  date_part('year', age(event_date, pp.date_of_birth)) < 6 THEN 'a.[0 - 5 yrs]'
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 6 AND 9 THEN 'b.[6 - 9 yrs]' 
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 10 AND 15 THEN 'c.[10 - 15 yrs]' 
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 16 AND 18 THEN 'd.[16 - 18 yrs]' 
ELSE 'e.[18+ yrs]' END AS agerange,
oaf.question_id,
CASE
WHEN oaf.item_value = 'QTXT' THEN oaf.item_detail
WHEN oaf.item_value != 'QTXT' THEN itd.item_description
ELSE itd.item_description END AS item_value,
1 as ovccount
FROM ovc_afc_event as oae
inner join reg_person as pp on oae.person_id = pp.id
inner join ovc_afc_form as oaf on oae.event_id = oaf.event_id
left outer join list_general itd on itd.item_id = oaf.item_value
where oae.form_id = '1A' and event_date between '{start_date}' and '{end_date}'
'''

QUERIES['afc_assessment_child'] = '''
SELECT pp.id as cpims_id, event_date as Assessment_date,
CASE pp.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Sex,
date_part('year', age(event_date, pp.date_of_birth)) AS Age,
CASE
WHEN  date_part('year', age(event_date, pp.date_of_birth)) < 6 THEN 'a.[0 - 5 yrs]'
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 6 AND 9 THEN 'b.[6 - 9 yrs]' 
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 10 AND 15 THEN 'c.[10 - 15 yrs]' 
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 16 AND 18 THEN 'd.[16 - 18 yrs]' 
ELSE 'e.[18+ yrs]' END AS agerange,
oaf.question_id,
CASE
WHEN oaf.item_value = 'QTXT' THEN oaf.item_detail
WHEN oaf.item_value != 'QTXT' THEN itd.item_description
ELSE itd.item_description END AS item_value,
1 as ovccount
FROM ovc_afc_event as oae
inner join reg_person as pp on oae.person_id = pp.id
inner join ovc_afc_form as oaf on oae.event_id = oaf.event_id
left outer join list_general itd on itd.item_id = oaf.item_value
where oae.form_id = '1B' and event_date between '{start_date}' and '{end_date}'
'''

QUERIES['afc_assessment_family'] = '''
SELECT pp.id as cpims_id, event_date as Assessment_date,
CASE pp.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Sex,
date_part('year', age(event_date, pp.date_of_birth)) AS Age,
CASE
WHEN  date_part('year', age(event_date, pp.date_of_birth)) < 6 THEN 'a.[0 - 5 yrs]'
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 6 AND 9 THEN 'b.[6 - 9 yrs]' 
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 10 AND 15 THEN 'c.[10 - 15 yrs]' 
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 16 AND 18 THEN 'd.[16 - 18 yrs]' 
ELSE 'e.[18+ yrs]' END AS agerange,
oaf.question_id,
CASE
WHEN oaf.item_value = 'QTXT' THEN oaf.item_detail
WHEN oaf.item_value != 'QTXT' THEN itd.item_description
ELSE itd.item_description END AS item_value,
1 as ovccount
FROM ovc_afc_event as oae
inner join reg_person as pp on oae.person_id = pp.id
inner join ovc_afc_form as oaf on oae.event_id = oaf.event_id
left outer join list_general itd on itd.item_id = oaf.item_value
where oae.form_id = '2A' and event_date between '{start_date}' and '{end_date}'
'''

QUERIES['afc_case_plan'] = '''
SELECT pp.id as cpims_id, event_date as Case_plan_date,
CASE pp.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Sex,
date_part('year', age(event_date, pp.date_of_birth)) AS Age,
CASE
WHEN  date_part('year', age(event_date, pp.date_of_birth)) < 6 THEN 'a.[0 - 5 yrs]'
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 6 AND 9 THEN 'b.[6 - 9 yrs]' 
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 10 AND 15 THEN 'c.[10 - 15 yrs]' 
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 16 AND 18 THEN 'd.[16 - 18 yrs]' 
ELSE 'e.[18+ yrs]' END AS agerange,
oaf.question_id,
CASE
WHEN oaf.item_value = 'QTXT' THEN oaf.item_detail
WHEN oaf.item_value != 'QTXT' THEN itd.item_description
ELSE itd.item_description END AS item_value,
1 as ovccount
FROM ovc_afc_event as oae
inner join reg_person as pp on oae.person_id = pp.id
inner join ovc_afc_form as oaf on oae.event_id = oaf.event_id
left outer join list_general itd on itd.item_id = oaf.item_value
where oae.form_id = '4A' and event_date between '{start_date}' and '{end_date}'
'''

QUERIES['afc_placement'] = '''
SELECT pp.id as cpims_id, event_date as Placement_date,
CASE pp.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Sex,
date_part('year', age(event_date, pp.date_of_birth)) AS Age,
CASE
WHEN  date_part('year', age(event_date, pp.date_of_birth)) < 6 THEN 'a.[0 - 5 yrs]'
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 6 AND 9 THEN 'b.[6 - 9 yrs]' 
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 10 AND 15 THEN 'c.[10 - 15 yrs]' 
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 16 AND 18 THEN 'd.[16 - 18 yrs]' 
ELSE 'e.[18+ yrs]' END AS agerange,
oaf.question_id,
CASE
WHEN oaf.item_value = 'QTXT' THEN oaf.item_detail
WHEN oaf.item_value != 'QTXT' THEN itd.item_description
ELSE itd.item_description END AS item_value,
1 as ovccount
FROM ovc_afc_event as oae
inner join reg_person as pp on oae.person_id = pp.id
inner join ovc_afc_form as oaf on oae.event_id = oaf.event_id
left outer join list_general itd on itd.item_id = oaf.item_value
where oae.form_id = '5A' and event_date between '{start_date}' and '{end_date}'
'''

QUERIES['afc_monitoring'] = '''
SELECT pp.id as cpims_id, event_date as Monitoring_date,
CASE pp.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Sex,
date_part('year', age(event_date, pp.date_of_birth)) AS Age,
CASE
WHEN  date_part('year', age(event_date, pp.date_of_birth)) < 6 THEN 'a.[0 - 5 yrs]'
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 6 AND 9 THEN 'b.[6 - 9 yrs]' 
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 10 AND 15 THEN 'c.[10 - 15 yrs]' 
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 16 AND 18 THEN 'd.[16 - 18 yrs]' 
ELSE 'e.[18+ yrs]' END AS agerange,
oaf.question_id,
oaq.question_text,
CASE
WHEN oaf.item_value = 'QTXT' THEN oaf.item_detail
WHEN oaf.item_value != 'QTXT' THEN itd.item_description
ELSE itd.item_description END AS item_value,
1 as ovccount
FROM ovc_afc_event as oae
inner join reg_person as pp on oae.person_id = pp.id
inner join ovc_afc_form as oaf on oae.event_id = oaf.event_id
left outer join list_general itd on itd.item_id = oaf.item_value
left outer join ovc_afc_questions oaq on oaq.question_code = oaf.question_id
where oae.form_id = '6A' and event_date between '{start_date}' and '{end_date}'
'''

QUERIES['afc_case_review'] = '''
SELECT pp.id as cpims_id, event_date as Case_review_date,
CASE pp.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Sex,
date_part('year', age(event_date, pp.date_of_birth)) AS Age,
CASE
WHEN  date_part('year', age(event_date, pp.date_of_birth)) < 6 THEN 'a.[0 - 5 yrs]'
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 6 AND 9 THEN 'b.[6 - 9 yrs]' 
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 10 AND 15 THEN 'c.[10 - 15 yrs]' 
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 16 AND 18 THEN 'd.[16 - 18 yrs]' 
ELSE 'e.[18+ yrs]' END AS agerange,
oaf.question_id,
CASE
WHEN oaf.item_value = 'QTXT' THEN oaf.item_detail
WHEN oaf.item_value != 'QTXT' THEN itd.item_description
ELSE itd.item_description END AS item_value,
1 as ovccount
FROM ovc_afc_event as oae
inner join reg_person as pp on oae.person_id = pp.id
inner join ovc_afc_form as oaf on oae.event_id = oaf.event_id
left outer join list_general itd on itd.item_id = oaf.item_value
where oae.form_id = '7A' and event_date between '{start_date}' and '{end_date}'
'''


QUERIES['afc_case_review_ya'] = '''
SELECT pp.id as cpims_id, event_date as Case_review_date,
CASE pp.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Sex,
date_part('year', age(event_date, pp.date_of_birth)) AS Age,
CASE
WHEN  date_part('year', age(event_date, pp.date_of_birth)) < 6 THEN 'a.[0 - 5 yrs]'
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 6 AND 9 THEN 'b.[6 - 9 yrs]' 
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 10 AND 15 THEN 'c.[10 - 15 yrs]' 
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 16 AND 18 THEN 'd.[16 - 18 yrs]' 
ELSE 'e.[18+ yrs]' END AS agerange,
oaf.question_id,
CASE
WHEN oaf.item_value = 'QTXT' THEN oaf.item_detail
WHEN oaf.item_value != 'QTXT' THEN itd.item_description
ELSE itd.item_description END AS item_value,
1 as ovccount
FROM ovc_afc_event as oae
inner join reg_person as pp on oae.person_id = pp.id
inner join ovc_afc_form as oaf on oae.event_id = oaf.event_id
left outer join list_general itd on itd.item_id = oaf.item_value
where oae.form_id = '8A' and event_date between '{start_date}' and '{end_date}'
'''

QUERIES['afc_closure'] = '''
SELECT pp.id as cpims_id, event_date as Identification_date,
CASE pp.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Sex,
date_part('year', age(event_date, pp.date_of_birth)) AS Age,
CASE
WHEN  date_part('year', age(event_date, pp.date_of_birth)) < 6 THEN 'a.[0 - 5 yrs]'
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 6 AND 9 THEN 'b.[6 - 9 yrs]' 
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 10 AND 15 THEN 'c.[10 - 15 yrs]' 
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 16 AND 18 THEN 'd.[16 - 18 yrs]' 
ELSE 'e.[18+ yrs]' END AS agerange,
oaf.question_id,
CASE
WHEN oaf.item_value = 'QTXT' THEN oaf.item_detail
WHEN oaf.item_value != 'QTXT' THEN itd.item_description
ELSE itd.item_description END AS item_value,
1 as ovccount
FROM ovc_afc_event as oae
inner join reg_person as pp on oae.person_id = pp.id
inner join ovc_afc_form as oaf on oae.event_id = oaf.event_id
left outer join list_general itd on itd.item_id = oaf.item_value
where oae.form_id = '9A' and event_date between '{start_date}' and '{end_date}'
'''

QUERIES['afc_consent'] = '''
SELECT pp.id as cpims_id, event_date as Consent_date,
CASE pp.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Sex,
date_part('year', age(event_date, pp.date_of_birth)) AS Age,
CASE
WHEN  date_part('year', age(event_date, pp.date_of_birth)) < 6 THEN 'a.[0 - 5 yrs]'
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 6 AND 9 THEN 'b.[6 - 9 yrs]' 
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 10 AND 15 THEN 'c.[10 - 15 yrs]' 
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 16 AND 18 THEN 'd.[16 - 18 yrs]' 
ELSE 'e.[18+ yrs]' END AS agerange,
oaf.question_id,
CASE
WHEN oaf.item_value = 'QTXT' THEN oaf.item_detail
WHEN oaf.item_value != 'QTXT' THEN itd.item_description
ELSE itd.item_description END AS item_value,
1 as ovccount
FROM ovc_afc_event as oae
inner join reg_person as pp on oae.person_id = pp.id
inner join ovc_afc_form as oaf on oae.event_id = oaf.event_id
left outer join list_general itd on itd.item_id = oaf.item_value
where oae.form_id = '3A' and event_date between '{start_date}' and '{end_date}'
'''

QUERIES['afc_transfer'] = '''
SELECT pp.id as cpims_id, event_date as Transfer_date,
CASE pp.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Sex,
date_part('year', age(event_date, pp.date_of_birth)) AS Age,
CASE
WHEN  date_part('year', age(event_date, pp.date_of_birth)) < 6 THEN 'a.[0 - 5 yrs]'
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 6 AND 9 THEN 'b.[6 - 9 yrs]' 
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 10 AND 15 THEN 'c.[10 - 15 yrs]' 
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 16 AND 18 THEN 'd.[16 - 18 yrs]' 
ELSE 'e.[18+ yrs]' END AS agerange,
oaf.question_id,
CASE
WHEN oaf.item_value = 'QTXT' THEN oaf.item_detail
WHEN oaf.item_value != 'QTXT' THEN itd.item_description
ELSE itd.item_description END AS item_value,
1 as ovccount
FROM ovc_afc_event as oae
inner join reg_person as pp on oae.person_id = pp.id
inner join ovc_afc_form as oaf on oae.event_id = oaf.event_id
left outer join list_general itd on itd.item_id = oaf.item_value
where oae.form_id = '10A' and event_date between '{start_date}' and '{end_date}'
'''

QUERIES['afc_referral'] = '''
SELECT pp.id as cpims_id, event_date as Referral_date,
CASE pp.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Sex,
date_part('year', age(event_date, pp.date_of_birth)) AS Age,
CASE
WHEN  date_part('year', age(event_date, pp.date_of_birth)) < 6 THEN 'a.[0 - 5 yrs]'
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 6 AND 9 THEN 'b.[6 - 9 yrs]' 
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 10 AND 15 THEN 'c.[10 - 15 yrs]' 
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 16 AND 18 THEN 'd.[16 - 18 yrs]' 
ELSE 'e.[18+ yrs]' END AS agerange,
oaf.question_id,
CASE
WHEN oaf.item_value = 'QTXT' THEN oaf.item_detail
WHEN oaf.item_value != 'QTXT' THEN itd.item_description
ELSE itd.item_description END AS item_value,
1 as ovccount
FROM ovc_afc_event as oae
inner join reg_person as pp on oae.person_id = pp.id
inner join ovc_afc_form as oaf on oae.event_id = oaf.event_id
left outer join list_general itd on itd.item_id = oaf.item_value
where oae.form_id = '12A' and event_date between '{start_date}' and '{end_date}'
'''

QUERIES['afc_disability'] = '''
SELECT pp.id as cpims_id, event_date as Case_date,
CASE pp.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Sex,
date_part('year', age(event_date, pp.date_of_birth)) AS Age,
CASE
WHEN  date_part('year', age(event_date, pp.date_of_birth)) < 6 THEN 'a.[0 - 5 yrs]'
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 6 AND 9 THEN 'b.[6 - 9 yrs]' 
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 10 AND 15 THEN 'c.[10 - 15 yrs]' 
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 16 AND 18 THEN 'd.[16 - 18 yrs]' 
ELSE 'e.[18+ yrs]' END AS agerange,
oaf.question_id,
CASE
WHEN oaf.item_value = 'QTXT' THEN oaf.item_detail
WHEN oaf.item_value != 'QTXT' THEN itd.item_description
ELSE itd.item_description END AS item_value,
1 as ovccount
FROM ovc_afc_event as oae
inner join reg_person as pp on oae.person_id = pp.id
inner join ovc_afc_form as oaf on oae.event_id = oaf.event_id
left outer join list_general itd on itd.item_id = oaf.item_value
where oae.form_id = '14A' and event_date between '{start_date}' and '{end_date}'
'''

QUERIES['afc_feedback_caregiver'] = '''
SELECT pp.id as cpims_id, event_date as Feedback_date,
CASE pp.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Sex,
date_part('year', age(event_date, pp.date_of_birth)) AS Age,
CASE
WHEN  date_part('year', age(event_date, pp.date_of_birth)) < 6 THEN 'a.[0 - 5 yrs]'
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 6 AND 9 THEN 'b.[6 - 9 yrs]' 
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 10 AND 15 THEN 'c.[10 - 15 yrs]' 
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 16 AND 18 THEN 'd.[16 - 18 yrs]' 
ELSE 'e.[18+ yrs]' END AS agerange,
oaf.question_id,
CASE
WHEN oaf.item_value = 'QTXT' THEN oaf.item_detail
WHEN oaf.item_value != 'QTXT' THEN itd.item_description
ELSE itd.item_description END AS item_value,
1 as ovccount
FROM ovc_afc_event as oae
inner join reg_person as pp on oae.person_id = pp.id
inner join ovc_afc_form as oaf on oae.event_id = oaf.event_id
left outer join list_general itd on itd.item_id = oaf.item_value
where oae.form_id = '15A' and event_date between '{start_date}' and '{end_date}'
'''

QUERIES['afc_feedback_child'] = '''
SELECT pp.id as cpims_id, event_date as Feedback_date,
CASE pp.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Sex,
date_part('year', age(event_date, pp.date_of_birth)) AS Age,
CASE
WHEN  date_part('year', age(event_date, pp.date_of_birth)) < 6 THEN 'a.[0 - 5 yrs]'
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 6 AND 9 THEN 'b.[6 - 9 yrs]' 
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 10 AND 15 THEN 'c.[10 - 15 yrs]' 
WHEN  date_part('year', age(event_date, pp.date_of_birth)) BETWEEN 16 AND 18 THEN 'd.[16 - 18 yrs]' 
ELSE 'e.[18+ yrs]' END AS agerange,
oaf.question_id,
CASE
WHEN oaf.item_value = 'QTXT' THEN oaf.item_detail
WHEN oaf.item_value != 'QTXT' THEN itd.item_description
ELSE itd.item_description END AS item_value,
1 as ovccount
FROM ovc_afc_event as oae
inner join reg_person as pp on oae.person_id = pp.id
inner join ovc_afc_form as oaf on oae.event_id = oaf.event_id
left outer join list_general itd on itd.item_id = oaf.item_value
where oae.form_id = '16A' and event_date between '{start_date}' and '{end_date}'
'''
