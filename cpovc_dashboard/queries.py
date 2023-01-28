QUERIES = {}

QUERIES['1A'] = '''
SELECT count(distinct(cpims_ovc_id)) as dcount,
gender as sex_id, agerange
from vw_cpims_registration {ocbos} {oareas} {odate}
group by gender, agerange
'''

QUERIES['1B'] = '''
SELECT count(distinct(cpims_ovc_id)) as dcount,
gender as sex_id,
CASE exit_status WHEN 'ACTIVE' THEN 'Active'
ELSE 'Exited' END AS active_status
from vw_cpims_registration {ocbos} {oareas} {odate}
group by gender, active_status
UNION
SELECT count(distinct(cpims_ovc_id)) as dcount,
gender as sex_id, 'Ever Registered' AS active_status
from vw_cpims_registration {ocbos} {oareas} {odate}
group by gender
'''

QUERIES['1C'] = '''
SELECT count(distinct(cpims_ovc_id)) as dcount,
gender as sex_id, schoollevel as school_level
from vw_cpims_registration where exit_status='ACTIVE' {cbos} {areas} {fdate}
group by gender, schoollevel
'''

QUERIES['1D'] = '''
SELECT count(distinct(cpims_ovc_id)) as dcount,
gender as sex_id, 'Active' as services
from vw_cpims_registration where exit_status='ACTIVE' {cbos} {areas} {fdate}
group by gender
UNION
SELECT count(distinct(cpims_ovc_id)) as dcount,
gender as sex_id, 'Has Birth Certificate' as services
from vw_cpims_registration where exit_status='ACTIVE'
and birthcert = 'HAS BIRTHCERT' {cbos} {areas} {fdate}
group by gender
UNION
SELECT count(distinct(cpims_ovc_id)) as dcount,
gender as sex_id, 'Has Disability' as services
from vw_cpims_registration where exit_status='ACTIVE'
and ovcdisability = 'HAS DISABILITY' {cbos} {areas} {fdate}
group by gender
UNION
SELECT count(distinct(cpims_ovc_id)) as dcount,
gender as sex_id, 'School Going' as services
from vw_cpims_registration where exit_status='ACTIVE'
and schoollevel != 'Not in School' {cbos} {areas} {fdate}
group by gender
'''

QUERIES['1E'] = '''
Select count(distinct(cpims_ovc_id)) AS dcount,
gender as sex_id,
CASE
when ovchivstatus='POSITIVE' THEN 'HIV Status +Ve'
when ovchivstatus='NEGATIVE' THEN 'HIV Status -Ve'
when ovchivstatus='NOT KNOWN' THEN 'HIV Status Unknown'
when ovchivstatus='HIV Test Not Required' THEN 'HIV Test not Required'
when ovchivstatus='HIV Referred For Testing' THEN 'HIV Referred For Testing'
ELSE 'Others' END AS hivstat
from vw_cpims_registration where exit_status='ACTIVE' {cbos} {areas} {fdate}
group by gender, ovchivstatus
'''

QUERIES['1F'] = '''
SELECT count(cpims_ovc_id) as dcount,
gender as sex_id, eligibility
from vw_cpims_registration {ocbos} {oareas} {odate}
group by gender, eligibility
'''

QUERIES['1G'] = '''
SELECT count(cpims_ovc_id) as dcount,
gender as sex_id, exit_reason
from vw_cpims_registration where exit_status = 'EXITED'
and dcount > 0 {cbos} {areas} {fdate}
group by gender, exit_reason
'''

QUERIES['1H'] = '''
SELECT count(distinct(cpims_ovc_id)) as dcount,
gender as sex_id, 'OVC Registration' as services
from vw_cpims_registration where exit_status = 'ACTIVE' {cbos} {areas} {dates}
group by gender
UNION
SELECT count(distinct(cpims_ovc_id)) as dcount,
gender as sex_id, 'OVC Exit' as services
from vw_cpims_registration where exit_status = 'EXITED' {cbos} {areas} {dates}
group by gender
'''

QUERIES['2A'] = '''
SELECT count(distinct(cpims_ovc_id)) as dcount,
gender as sex_id, 'Active' as hivstat
from vw_cpims_registration where exit_status='ACTIVE' {cbos} {fdate}
group by gender
UNION
Select count(distinct(cpims_ovc_id)) AS dcount,
gender as sex_id, 'Positive' as hivstat
from vw_cpims_registration where exit_status='ACTIVE'
and ovchivstatus='POSITIVE' {cbos} {fdate} group by gender
UNION
Select count(distinct(cpims_ovc_id)) as dcount,
gender as sex_id, 'On ART' as hivstat
from vw_cpims_registration where exit_status='ACTIVE'
and ovchivstatus='POSITIVE' AND artstatus='ART' {cbos} {fdate}
group by gender
UNION
Select count(distinct(cpims_ovc_id)) as dcount,
gender as sex_id, 'VL Accessed' as hivstat
from vw_cpims_viral_load {ocbos}
group by gender
UNION
Select count(distinct(v.cpims_ovc_id)) as dcount,
v.gender as sex_id, 'Current VL' as hivstat
from vw_cpims_viral_load v
inner join (
select cpims_ovc_id, max(date_of_event) as most_current_vl_date
from vw_cpims_viral_load
group by cpims_ovc_id ) vl on v.cpims_ovc_id = vl.cpims_ovc_id
and v.date_of_event=vl.most_current_vl_date
where current_date - vl.most_current_vl_date <= 400 {vcbos}
group by v.gender
UNION
Select count(distinct(v.cpims_ovc_id)) AS dcount,
v.gender as sex_id, 'Suppressed' as hivstat
from vw_cpims_viral_load v
inner join (
select cpims_ovc_id, max(date_of_event) as most_current_vl_date
from vw_cpims_viral_load
group by cpims_ovc_id ) vl on v.cpims_ovc_id = vl.cpims_ovc_id
and v.date_of_event=vl.most_current_vl_date
where current_date - vl.most_current_vl_date <= 400
and v.viral_load < 1001 {vcbos} group by v.gender
UNION
Select count(distinct(v.cpims_ovc_id)) AS dcount,
v.gender as sex_id, 'Not Suppressed' as hivstat
from vw_cpims_viral_load v
inner join (
select cpims_ovc_id, max(date_of_event) as most_current_vl_date
from vw_cpims_viral_load
group by cpims_ovc_id ) vl on v.cpims_ovc_id=vl.cpims_ovc_id
and v.date_of_event=vl.most_current_vl_date
where current_date - vl.most_current_vl_date <=400
and v.viral_load > 1000 {vcbos}
group by v.gender
'''

QUERIES['2B'] = '''
Select count(distinct(cpims_ovc_id)) as dcount, gender as sex_id, agerange
from vw_cpims_viral_load where (current_date - date_of_event) < 401
and viral_load > 10000 {cbos} group by gender, agerange
'''

QUERIES['2C'] = '''
select sum(x.cnt) as dcount, x.gender as sex_id,
'OVC_SERV' as hivstat from
(
Select count(distinct(cpims_ovc_id)) as cnt,
gender from vw_cpims_active_beneficiary {ocbos}
group by gender
UNION ALL
Select count(distinct(cpims_ovc_id)), gender
from vw_cpims_benchmark_achieved where (current_date - date_of_event) <= 400
AND cpara_score = 17 {cbos} group by gender
) x group by x.gender
UNION
Select count(distinct(cpims_ovc_id)) AS dcount,
gender as sex_id,
CASE
when ovchivstatus='POSITIVE' THEN 'HIV Status +Ve'
when ovchivstatus='NEGATIVE' THEN 'HIV Status -Ve'
when ovchivstatus='NOT KNOWN' THEN 'HIV Status Unknown'
when ovchivstatus='HIV Test Not Required' THEN 'HIV Test not Required'
when ovchivstatus='HIV Referred For Testing' THEN 'HIV Referred For Testing'
ELSE 'Others' END AS hivstat
from vw_cpims_registration where cpims_ovc_id in
(select distinct(x.cpims_ovc_id) from
(
Select distinct(cpims_ovc_id)
from vw_cpims_active_beneficiary {ocbos}
UNION ALL
Select distinct(cpims_ovc_id)
from vw_cpims_benchmark_achieved where (current_date - date_of_event) <= 400
AND cpara_score = 17 {cbos}
) x)
and exit_status='ACTIVE' {cbos} {areas} {fdate}
group by gender, ovchivstatus
'''

QUERIES['2D'] = '''
SELECT count(distinct(cpims_ovc_id)) as dcount,
'Male' as sex_id, 'HIV Status' as hivstat
from vw_cpims_registration where exit_status='ACTIVE' {cbos}
UNION
Select count(distinct(cpims_ovc_id)) AS dcount,
'Male' as sex_id, 'ART Status' as hivstat
from vw_cpims_registration where exit_status='ACTIVE'
and ovchivstatus='POSITIVE' {cbos}
UNION
Select count(distinct(v.cpims_ovc_id)) as dcount,
'Male' as sex_id, 'Suppression' as hivstat
from vw_cpims_viral_load v
inner join (
select cpims_ovc_id, max(date_of_event) as most_current_vl_date
from vw_cpims_viral_load
group by cpims_ovc_id ) vl on v.cpims_ovc_id = vl.cpims_ovc_id
and v.date_of_event=vl.most_current_vl_date
where current_date - vl.most_current_vl_date <= 400 {vcbos}
UNION
Select count(distinct(cpims_ovc_id)) AS dcount,
'Female' as sex_id, 'HIV Status' as hivstat
from vw_cpims_registration where exit_status='ACTIVE'
and (ovchivstatus='POSITIVE' or ovchivstatus='NEGATIVE'
or ovchivstatus='NOT KNOWN' or ovchivstatus='HIV Test Not Required'
or ovchivstatus='HIV Referred For Testing') {cbos}
UNION
Select count(distinct(cpims_ovc_id)) as dcount,
'Female' as sex_id, 'ART Status' as hivstat
from vw_cpims_registration where exit_status='ACTIVE'
and ovchivstatus='POSITIVE' AND artstatus='ART' {cbos}
UNION
Select count(distinct(v.cpims_ovc_id)) AS dcount,
'Female' as sex_id, 'Suppression' as hivstat
from vw_cpims_viral_load v
inner join (
select cpims_ovc_id, max(date_of_event) as most_current_vl_date
from vw_cpims_viral_load
group by cpims_ovc_id ) vl on v.cpims_ovc_id = vl.cpims_ovc_id
and v.date_of_event=vl.most_current_vl_date
where current_date - vl.most_current_vl_date <= 400
and v.viral_load < 1001 {vcbos}
'''

QUERIES['3A'] = '''
SELECT count(distinct(cpims_ovc_id)) as dcount,
gender as sex_id, 'Active' as services
from vw_cpims_registration where exit_status='ACTIVE' {cbos} group by gender
UNION
Select count(distinct(person_id)) AS dcount,
gender as sex_id, 'Served Two Quarters' as services
from vw_cpims_two_quarters where (current_date - date_of_event) <=400 {cbos}
group by gender
UNION
Select count(distinct(cpims_ovc_id)) as dcount,
gender, 'Case Plans' as services
from vw_cpims_case_plan where (current_date - date_of_event) <= 400 {cbos}
group by gender
UNION
Select count(distinct(cpims_ovc_id)) as dcount,
gender, 'CPARA' as services
from vw_cpims_cpara where (current_date - date_of_event) <= 400 {cbos}
group by gender
UNION
Select count(distinct(cpims_ovc_id)) as dcount,
gender as sex_id, 'Graduated' as services
from vw_cpims_benchmark_achieved
where (current_date - date_of_event) <= 400
AND cpara_score = 17 {cbos}
group by gender
UNION
Select count(distinct(cpims_ovc_id)) as dcount,
gender as sex_id, 'Active Beneficiary' as services
from vw_cpims_active_beneficiary {ocbos}
group by gender
UNION
select sum(x.cnt) as dcount, x.gender as sex_id,
'OVC_SERV' as hivstat from
(
Select count(distinct(cpims_ovc_id)) as cnt,
gender from vw_cpims_active_beneficiary {ocbos}
group by gender
UNION ALL
Select count(distinct(cpims_ovc_id)), gender
from vw_cpims_benchmark_achieved where (current_date - date_of_event) <= 400
AND cpara_score = 17 {cbos} group by gender
) x group by x.gender
UNION
Select count(distinct(cpims_ovc_id)) as dcount,
gender as sex_id, 'Exit without Graduation' as services
from vw_cpims_registration where exit_status='ACTIVE'
AND cpims_ovc_id NOT IN
(select distinct(vw_cpims_registration.cpims_ovc_id)
from vw_cpims_two_quarters ) {cbos}
group by gender
'''

QUERIES['3B'] = '''
Select count(distinct(cpims_ovc_id)) as dcount,
gender as sex_id, domain as services
from vw_cpims_list_served {ocbos} group by gender, domain
'''

QUERIES['3C'] = '''
SELECT count(distinct(cpims_ovc_id)) as dcount,
gender as sex_id, 'OVC Comprehensive' as services
from vw_cpims_registration where exit_status='ACTIVE' {cbos} group by gender
'''

QUERIES['3D'] = '''
Select count(distinct(cpims_ovc_id)) as dcount,
gender as sex_id, cpara_score as services
from vw_cpims_benchmark_achieved
where (current_date - date_of_event) <= 400 {cbos}
group by gender, cpara_score
'''

QUERIES['3E'] = '''
Select count(distinct(cpims_ovc_id)) as dcount,
gender as sex_id, service as services
from vw_cpims_list_served
where {odates} {cbos}
group by gender, service
order by dcount desc
'''

QUERIES['4A'] = '''
SELECT count(distinct(cpims_ovc_id)) as dcount,
gender as sex_id, 'Active' as services
from vw_cpims_registration where exit_status='ACTIVE' {cbos} group by gender
UNION
Select count(distinct(cpims_ovc_id)) as dcount,
gender, 'Current Case Plan' as services
from vw_cpims_case_plan where (current_date - date_of_event) <= 400 {cbos}
group by gender
UNION
Select count(distinct(cpims_ovc_id)) as dcount,
gender, 'Current CPARA' as services
from vw_cpims_cpara where (current_date - date_of_event) <= 400 {cbos}
group by gender
'''

QUERIES['4B'] = '''
Select count(distinct(cpims_ovc_id)) as dcount,
gender as sex_id, graduationpath as services
from vw_cpims_benchmark_achieved
where (current_date - date_of_event) <= 400 {cbos}
group by gender, graduationpath;
'''