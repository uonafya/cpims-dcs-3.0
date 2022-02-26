QUERY = {}
TXT = {}
# County Coordinators
QUERY[1] = '''
select rp.email from reg_persons_org_units rpou
inner join reg_org_unit ou on ou.id=rpou.org_unit_id
inner join reg_person rp on rp.id = person_id
where date_delinked is null and ou.org_unit_type_id = 'TNGP'
and rp.email != '' and rp.designation in ('DPCO', 'DSCC', 'DSSD');
'''

# Statutory Institutions - Staff
QUERY[2] = '''
select rp.email from reg_persons_org_units rpou
inner join reg_org_unit ou on ou.id=rpou.org_unit_id
inner join reg_person rp on rp.id = person_id
where date_delinked is null and ou.org_unit_type_id
in ('TNAP', 'TNRH', 'TNRS', 'TNRR') and rp.email != '';
'''

# Sub-county Children Officers
QUERY[3] = '''
select rp.email from reg_persons_org_units rpou
inner join reg_org_unit ou on ou.id=rpou.org_unit_id
inner join reg_person rp on rp.id = person_id
where date_delinked is null and ou.org_unit_type_id
in ('TNGD') and rp.email != ''
order by org_unit_id;
'''

TXT[1] = '''
Total records for case management for this week are <b>(%s)</b> and
<font color="red"> NOTE that the details are ONLY available if
input in CPIMS before due date.</font> This is to assist in the
Management of Summons, Court Sessions and Discharges.
'''

TXT[2] = '''
Total records for your action are <b>(%s)</b> and <font color="red">
NOTE that some are ONLY warnings and do NOT require editing.</font>
<b>DQA Sex:</b> Cases with gender incompatibility e.g FGM for a boy;
<b>DQA DoB:</b> Missing date of birth or over age for age > 25 years old;
<b>DQA Age:</b> Cases where age is incompatible e.g Truancy for a 5 year old;
<b>Case Status:</b> Pending where case was only registered
and No action thereafter.'
'''

TXT[3] = '''
No data Found in the system for this organization unit in the period
specified for automation.
'''

TXT[4] = '''
Total records from the system are <b>(%s)</b> and <font color="red">
NOTE that this is the data input in the system within the period.</font>
Data must be input by the 5<sup>th</sup> of every next month and institution
placements must be before Monday of the following week.
'''
