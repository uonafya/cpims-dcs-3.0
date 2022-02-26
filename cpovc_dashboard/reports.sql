
---Actives
Select count(distinct(cpims_ovc_id)),cbo, ward,constituency, county, gender, agerange from vw_cpims_registration where exit_status='ACTIVE' group by cbo_id, cbo, ward, constituency, county, gender, agerange;

+++ case management
---Current case plans

Select count(distinct(cpims_ovc_id)),cbo, ward,constituency, county, gender from vw_cpims_case_plan where current_date- date_of_event<=400 group by cbo_id, cbo, ward, constituency, county, gender;

---Current case plans
Select count(distinct(cpims_ovc_id)),cbo, ward,constituency, county, gender from vw_cpims_cpara where current_date- date_of_event<=400 group by cbo_id, cbo, ward, constituency, county, gender;

--current cpara
Select count(distinct(cpims_ovc_id)),cbo, ward,constituency, county, gender from vw_cpims_cpara where current_date- date_of_event<=400 group by cbo_id, cbo, ward, constituency, county, gender;


+++ services  reporting
--services  
Select count(distinct(cpims_ovc_id)),cbo, ward,constituency, county, gender, agerange from vw_cpims_cpara where current_date- date_of_event<=400 group by cbo_id, cbo, ward, constituency, county, gender, agerange;



--Graduation pathways

Select count(distinct(cpims_ovc_id)),cbo, ward,constituency, county, gender, graduationpath from vw_cpims_benchmark_achieved where current_date- date_of_event<=400 group by cbo_id, cbo, ward, constituency, county, gender, graduationpath;


+++Services

--Services reporting
--Actives
Select count(distinct(cpims_ovc_id)),cbo, ward,constituency, county, genderfrom vw_cpims_registration where exit_status='ACTIVE' group by cbo_id, cbo, ward, constituency, county, gender;

--served




--served two quarters
Select count(distinct(person_id)),cbo, ward,constituency, county, gender, graduationpath from vw_cpims_two_quarters where current_date- date_of_event<=400 group by cbo_id, cbo, ward, constituency, county, gender;

---Current case plans
Select count(distinct(cpims_ovc_id)),cbo, ward,constituency, county, gender from vw_cpims_cpara where current_date- date_of_event<=400 group by cbo_id, cbo, ward, constituency, county, gender;

--current cpara
Select count(distinct(cpims_ovc_id)),cbo, ward,constituency, county, gender from vw_cpims_cpara where current_date- date_of_event<=400 group by cbo_id, cbo, ward, constituency, county, gender;


---graduated
Select count(distinct(cpims_ovc_id)),cbo, ward,constituency, county, gender from vw_cpims_benchmark_achieved where current_date- date_of_event<=400 AND cpara_score=17 group by cbo_id, cbo, ward, constituency, county, gender;


--active_beneficiary
Select count(distinct(cpims_ovc_id)),cbo, ward,constituency, county, gender from vw_cpims_active_beneficiary  group by cbo_id, cbo, ward, constituency, county, gender;

---ovc_serv


---hivstat

--Exit without graduation
Select count(distinct(cpims_ovc_id)),cbo, ward,constituency, county, gender from vw_cpims_registration where exit_status='ACTIVE'
AND NOT IN (select vw_cpims_registration.cpims_ovc_id from vw_cpims_two_quarters )
group by cbo_id, cbo, ward, constituency, county, gender, agerange;


---served by domain
Select count(distinct(cpims_ovc_id)),cbo, ward,constituency, county, gender, domain from vw_cpims_list_served group by cbo_id, cbo, ward, constituency, county, gender, domain


--ovc_serv by beneficiary categories


--benchmark scores
Select count(distinct(cpims_ovc_id)),cbo, ward,constituency, county, gender, cpara_score from vw_cpims_benchmark_achieved where current_date- date_of_event<=400 AND cpara_score=17 group by cbo_id, cbo, ward, constituency, county, gender, cpara_score;


--benchmark performance
Select count(distinct(cpims_ovc_id)),cbo, ward,constituency, county, gender, bench1, bench2, bench3, bench4, bench5, bench6, bench7, bench8, bench9, bench10,bench11, bench12, bench13, bench14, bench15, bench16, bench17 from vw_cpims_benchmark_achieved where current_date- date_of_event<=400 AND cpara_score=17 group by cbo_id, cbo, ward, constituency, county, gender, bench1, bench2, bench3, bench4, bench5, bench6, bench7, bench8, bench9, bench10,bench11, bench12, bench13, bench14, bench15, bench16, bench17 ;


+++HIVSTAT and VL

--vl cascade
--active
Select count(distinct(cpims_ovc_id)),cbo, ward,constituency, county, gender from vw_cpims_registration where exit_status='ACTIVE' group by cbo_id, cbo, ward, constituency, county, gender;

--positive
Select count(distinct(cpims_ovc_id)),cbo, ward,constituency, county, gender from vw_cpims_registration where exit_status='ACTIVE' and ovchivstatus='POSITIVE' group by cbo_id, cbo, ward, constituency, county, gender;


--on ART
Select count(distinct(cpims_ovc_id)),cbo, ward,constituency, county, gender from vw_cpims_registration where exit_status='ACTIVE' and ovchivstatus='POSITIVE' AND artstatus='ART' group by cbo_id, cbo, ward, constituency, county, gender;


--vl accessed
Select count(distinct(cpims_ovc_id)),cbo, ward,constituency, county, gender from vw_cpims_viral_load group by cbo_id, cbo, ward, constituency, county, gender;


--current vl
Select count(distinct(cpims_ovc_id)),cbo, ward,constituency, county, gender from vw_cpims_viral_load where current_date - max(date_of_event) <=400 group by cbo_id, cbo, ward, constituency, county, gender;

--supressed
Select count(distinct(cpims_ovc_id)),cbo, ward,constituency, county, gender from vw_cpims_viral_load where current_date - max(date_of_event) <401 and viral_load < 1001 group by cbo_id, cbo, ward, constituency, county, gender;

--not suppressed
Select count(distinct(cpims_ovc_id)),cbo, ward,constituency, county, gender from vw_cpims_viral_load where current_date - max(date_of_event) <401 and viral_load > 1000 group by cbo_id, cbo, ward, constituency, county, gender;


--Viral load > 10,000
Select count(distinct(cpims_ovc_id)),cbo, ward,constituency, county, gender, agerange from vw_cpims_viral_load where current_date - max(date_of_event) <401 and viral_load > 10000 group by cbo_id, cbo, ward, constituency, county, gender, agerange;

--ovc_hivstat

--95 -95 -95 cascade (update as we had discussed)

-- 2A ---
-- Actives
Select count(distinct(cpims_ovc_id)) as dcount, gender as sex_id from vw_cpims_registration where exit_status='ACTIVE' {cbos} group by gender;
