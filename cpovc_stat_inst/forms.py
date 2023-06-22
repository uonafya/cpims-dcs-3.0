from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import RadioSelect,TimeInput,DateInput,TextInput,DateInput

from cpovc_main.functions import get_list, get_org_units_list,get_lists
from cpovc_registry.functions import (
    get_geo_list,
    get_all_geo_list,
    get_all_location_list,
    get_all_sublocation_list,
)
from cpovc_registry.models import RegOrgUnit

# from .functions import get_questions
# Added for CTiP
from cpovc_main.country import OCOUNTRIES
person_type_list = get_list('person_type_id', 'Please Select Type')
school_level_list = get_list('school_level_id', 'Please Select Level')
admission_list = get_list('school_type_id', 'Please Select one')
disability_list = get_list('disability_type_id', 'Please Select one')
severity_list = get_list('severity_level_id', 'Please Select one')
admission_type_list = get_list('admission_type_id', 'Please Select')
admission_reason_list = get_list('care_admission_reason_id')
domain_list = get_list('afc_domain_id', 'Please Select')
list_sex_id = get_list('sex_id')
list_relationship = get_list('relationship_type_id', 'Please Select')
consent_forms_list = get_list('consent_forms', 'Please Select')
# new listings
list_other_adms = get_list('other_form_admission', 'Please Select')
list_other_vulnerability = get_list(
    'vulnerability_at_admission', 'Please Select')
list_relationship = get_list('relationship_type_id', 'Please Select')
list_education_perf = get_list('education_performance')
list_marriage_type = get_list('parents_marriage_type', 'Please Select')
list_items_count = get_list('items_count_id', 'Please Select')
list_special_support = get_list('special_support')
list_community_services = get_list('community_services')
list_school_category = get_list('school_category_id', 'Please Select')
list_range_level = get_list('attachment_level', 'Please Select')
list_range_level_rdo = get_lists(['attachment_level', 'na_option'])
list_child_exhibits = get_list('child_exhibits')
list_income_range = get_list('income_range', 'Please Select')
list_employment_type = get_list('employment_type', 'Please Select')
list_closure_reasons = get_list('case_closure_reasons', 'Please Select')
list_case_transfer_ids = get_list('case_transfer_ids', 'Please Select')
list_satisfied_level = get_list('satisfied_level_ids')
list_feeling_level = get_list('feeling_level_ids')
list_referral_reasons = get_list('referral_reasons_ids', 'Please Select')
list_referral_documents = get_list('referral_documents_ids')
list_case_plan_responsible = get_list('case_plan_responsible', 'Please Select')
psearch_criteria_list = get_list('psearch_criteria_type_id', 'Select Criteria')
org_units_list = get_org_units_list('Please select Unit')
classes_list = get_list('class_level_id', 'Please Select')

all_list = get_all_geo_list()
county_list = get_geo_list(all_list, 'GPRV')
sub_county_list = get_geo_list(all_list, 'GDIS')
ward_list = get_geo_list(all_list, 'GWRD')


disability_actions = get_list('disability_actions')
list_family_types = get_list('family_type_id', 'Please Select')

YESNO_UN_CHOICES = get_list('yesno_una')
list_disability_assessment = get_list('disability_assessment_id')
list_disability_handling = get_list('disability_handling_id')
list_attachment_assessment = get_list(
    'attachment_assessment_id', 'Please select')


YESNO_CHOICES = get_list('yesno_id')
YESNO_UK_CHOICES = get_lists(['yesno_id', 'uk_option'])
care_option_list = get_list(
    'alternative_family_care_type_id', 'Please Select Care')

disability_degree = (('0', '0'), ('1', '1'), ('2', '2'),
                     ('3', '3'), ('4', '4'), )

YESNONA_choices = get_list('yesno_na')
list_sex_other_id = get_list('sex_id', 'Please Select')
list_ratings = get_list('ratings_id')
list_frequency = get_lists(['period_frequency_id', 'na_option'])




ENTRY_CHOICES = (
    ("identified", "Was identified"),
    ("referred", "Was referred"),
    ("own_will", "Came of own will"),
)
GENDER=(
    ("M", "Male"),
    ("F", "Female")
)
DIFFICULTY=(("No", "No"), ("Some difficulty", "Yes, some difficulty"),
            ("A lot of difficulty", "Yes, a lot of difficulty"),
            ("Cannot do it at all", "Cannot do it at all"))

YES_NO_CHOICES = get_list('yesno_id')

REFERRAL_SOURCES = (
    ("Parent", "Parent"),
    ("Family_member", "Family member"),
    ("Guardian", "Guardian"),
    ("Members_of_the_public", "Members of the public"),
    ("Local_leader", "Local leader"),
    ("Police", "Police"),
    ("Lawyer", "Lawyer"),
    ("Court", "Court"),
    ("Childrens_Department", "Children’s Department"),
    ("Local_Administration_Office", "Local Administration Office"),
    ("Other", "Other"),
)

CHILD_CATEGORY = (
    ("Abandoned_child", "Abandoned child"),
    ("Neglected_child", "Neglected child"),
    ("Destitute_child", "Destitute child"),
    ("Street_child", "Street child"),
    ("Refugee_child", "Refugee child"),
    ("Lost_child", "Lost child"),
    ("Abused_child", "Abused child (specify)"),
    ("Victim_of_harmful_cultural", "Victim of harmful cultural"),
    ("practices", "practices"),
    ("harmful_religious_practices", "Victim of harmful religious practices"),
)

ADMISSION_TYPE = (
    ("New_admission", "New admission"),
    ("readmission_after_escape", "readmission after escape"),
    ("readmission_on_relapse", "readmission on relapse"),
    ("transfer_in", "transfer in"),
)

GOAL = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
]

SUB_GOAL = [
    ('1-1', '1-1'),
    ('1-2', '1-2'),
    ('2-1', '1-1'),
    ('2-2', '2-2'),
    ('3-1', '3-1'),
    ('3-2', '3-2')
]


class SIPreAdmission(forms.Form):
    pass


class SIAdmission(forms.Form):
    name = forms.CharField(max_length=100)
    nickname = forms.CharField(max_length=50)
    sex = forms.ChoiceField(
        choices=(("M", "Male"), ("F", "Female")),
        required=False,
        widget=forms.Select(attrs={"class": "form-control", "id": "gender"}),
    )
    date_of_birth = forms.DateField()
    age = forms.IntegerField()
    date_of_admission = forms.DateField()
    current_year_of_school = forms.CharField(max_length=50)
    type_of_entry = forms.ChoiceField(
        choices=ENTRY_CHOICES,
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "id": "type_of_entry",
            }
        ),
    )
    referral_source = forms.ChoiceField(
        choices=REFERRAL_SOURCES,
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "id": "referral_source",
            }
        ),
    )
    child_category = forms.ChoiceField(
        choices=REFERRAL_SOURCES,
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "id": "child_category",
            }
        ),
    )
    abused_child_desc = forms.CharField(max_length=100)
    referral_source_others = forms.CharField(max_length=100)
    referrer_name = forms.CharField(max_length=100)
    referrer_address = forms.CharField(max_length=100)
    referrer_phone = forms.CharField(max_length=100)
    not_contact_child = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "id": "not_contact_child",
            }
        ),
    )
    name_not_contact_child = forms.CharField(max_length=100)
    relationship_to_child_not_contact_child = forms.ChoiceField(
        choices=list_relationship,
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control'}))
    consent_form_signed = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "id": "consent_form_signed",
            }
        ),
    )
    commital_court_order = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "id": "commital_court_order",
            }
        ),
    )
    school_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Name of School"),
                "class": "form-control",
                "id": "school_name",
            }
        ),
    )



class MedicalAssesmentForm(forms.Form):
    name = forms.CharField(label='Name')
    age = forms.IntegerField(label='Age')
    sex = forms.ChoiceField(label='Sex',
                            choices=list_sex_id,
                            widget=forms.RadioSelect)

    height = forms.DecimalField(label='Height',
                                widget=forms.NumberInput(
                                    attrs={'placeholder': _(''),
                                           'class': 'form-control',
                                           'data-parsley-required': "false"}))
    blood_pressure = forms.CharField(label='Blood Pressure',
                                     widget=forms.TextInput(
                                         attrs={'placeholder': _(''),
                                                'class': 'form-control',
                                                'data-parsley-required': "false"}))
    weight = forms.DecimalField(label='Weight',
                                widget=forms.NumberInput(
                                    attrs={'placeholder': _(''),
                                           'class': 'form-control',
                                           'data-parsley-required': "false"}))
    pulse_rate = forms.IntegerField(label='Pulse Rate',
                                    widget=forms.NumberInput(
                                        attrs={'placeholder': _(''),
                                               'class': 'form-control',
                                               'data-parsley-required': "false"}))

    physical_disability = forms.ChoiceField(label='Any Physical Disability',
                                            choices=disability_list,
                                            widget=forms.ChoiceField)


    current_illness = forms.ChoiceField(label='Any Current Illness',
                                      choices=YES_NO_CHOICES,
                                      widget=forms.RadioSelect )

    current_medications = forms.CharField(label='List Current Medications',
                                          widget=forms.TextInput(
                                          attrs={'placeholder': _(''),
                                                   'class': 'form-control',
                                                   'data-parsley-required': "false"}))

    tb_treatment_or_exposure = forms.ChoiceField (label='Any treatment for TB or exposure to a TB patient?',
                                                  choices=YES_NO_CHOICES,
                                                  widget=forms.RadioSelect

                                               )

    mental_illness_history = forms.ChoiceField(label='Any history of mental illness in self or family',
                                             choices=YES_NO_CHOICES,
                                             widget=forms.RadioSelect)

    sleep_problems = forms.ChoiceField(label='Any sleep problems?',
                                       choices=YES_NO_CHOICES,
                                       widget=forms.RadioSelect)
    sleep_problems_description = forms.CharField(label='Elaborate',
                                                 widget=forms.TextInput(
                                                     attrs={'placeholder': _(''),
                                                            'class': 'form-control',
                                                            'data-parsley-required': "false"}))

    seizures_history = forms.ChoiceField(label='Any history of seizures?',
                                         choices=YES_NO_CHOICES,
                                         widget=forms.RadioSelect)
    seizures_duration = forms.CharField(label='List current duration',
                                        widget=forms.TextInput(
                                        attrs={'placeholder': _(''),
                                                   'class': 'form-control',
                                                   'data-parsley-required': "false"}))
    seizures_medications = forms.CharField(label='List current medications',
                                           widget=forms.TextInput(
                                               attrs={'placeholder': _(''),
                                                      'class': 'form-control',
                                                      'data-parsley-required': "false"}))

    known_allergy = forms.ChoiceField(label='Any known allergy?',
                                      choices=YES_NO_CHOICES,
                                      widget=forms.RadioSelect,
                                      required=False)
    known_allergy_list = forms.CharField(label='List',
                                         widget=forms.TextInput(
                                             attrs={'placeholder': _(''),
                                                    'class': 'form-control',
                                                    'data-parsley-required': "false"}))

    # Physical Examination
    general_examination=forms.CharField(label="genral examination",
                                        widget=forms.Textarea(
                                            attrs={'placeholder': _(''),
                                                   'class': 'form-control',
                                                   'data-parsley-required': "false"}))

    orientation_time = forms.TimeField(label='Orientation: Time',
                                           widget=TimeInput(format='%H:%M'))

    orientation_date = forms.DateField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': _('Select date'),
                   'class': 'form-control',
                   'data-parsley-notfuturedate': "dd-M-yy",
                   'id': 'datepicker',
                   'data-parsley-group': 'primary'}))

    orientation_place = forms.CharField(label='Orientation: Place',
                                        widget=forms.TextInput(
                                            attrs={'placeholder': _(''),
                                                   'class': 'form-control',
                                                   'data-parsley-required': "false"}))
    orientation_person = forms.CharField(label='Orientation: Person',
                                         widget=forms.TextInput(
                                             attrs={'placeholder': _(''),
                                                    'class': 'form-control',
                                                    'data-parsley-required': "false"}))
    speech = forms.CharField(label='Speech',
                             widget=forms.TextInput(
                                 attrs={'placeholder': _(''),
                                        'class': 'form-control',
                                        'data-parsley-required': "false"}))
    visual_acuity_re = forms.CharField(label='Visual Acuity: RE',
                                       widget=forms.TextInput(
                                           attrs={'placeholder': _(''),
                                                  'class': 'form-control',
                                                  'data-parsley-required': "false"}))
    visual_acuity_le = forms.CharField(label='Visual Acuity: LE',
                                       widget=forms.TextInput(
                                           attrs={'placeholder': _(''),
                                                  'class': 'form-control',
                                                  'data-parsley-required': "false"}))
    head_and_neck = forms.CharField(label='Head and Neck',
                                    widget=forms.TextInput(
                                        attrs={'placeholder': _(''),
                                               'class': 'form-control',
                                               'data-parsley-required': "false"}))
    ent = forms.CharField(label='ENT',
                          widget=forms.TextInput(
                              attrs={'placeholder': _(''),
                                     'class': 'form-control',
                                     'data-parsley-required': "false"}))
    central_nervous_system = forms.CharField(label='Central Nervous System',
                                             widget=forms.TextInput(
                                                 attrs={'placeholder': _(''),
                                                        'class': 'form-control',
                                                        'data-parsley-required': "false"}))
    cardiovascular_system = forms.CharField(label='Cardiovascular System',
                                            widget=forms.TextInput(
                                                attrs={'placeholder': _(''),
                                                       'class': 'form-control',
                                                       'data-parsley-required': "false"}))
    respiratory_system = forms.CharField(label='Respiratory System',
                                         widget=forms.TextInput(
                                             attrs={'placeholder': _(''),
                                                    'class': 'form-control',
                                                    'data-parsley-required': "false"}))
    git_system = forms.CharField(label='GIT System',
                                 widget=forms.TextInput(
                                     attrs={'placeholder': _(''),
                                            'class': 'form-control',
                                            'data-parsley-required': "false"}))
    musculoskeletal_system = forms.CharField(label='Musculoskeletal System',
                                             widget=forms.TextInput(
                                                 attrs={'placeholder': _(''),
                                                        'class': 'form-control',
                                                        'data-parsley-required': "false"}))
    reproductive_system = forms.CharField(label='Reproductive System',
                                          widget=forms.TextInput(
                                              attrs={'placeholder': _(''),
                                                     'class': 'form-control',
                                                     'data-parsley-required': "false"}))
    skin_condition = forms.CharField(label='Condition of the Skin',
                                     widget=forms.TextInput(
                                         attrs={'placeholder': _(''),
                                                'class': 'form-control',
                                                'data-parsley-required': "false"}))
    dental_condition = forms.ChoiceField(label='Any dental condition?',
                                         choices=YES_NO_CHOICES,
                                         widget=forms.RadioSelect,
                                         required=False)
    urinalysis = forms.CharField(label='Urinalysis',
                                 widget=forms.TextInput(
                                     attrs={'placeholder': _(''),
                                            'class': 'form-control',
                                            'data-parsley-required': "false"}))
    stool_oc = forms.CharField(label='Stool for O/C',
                               widget=forms.TextInput(
                                   attrs={'placeholder': _(''),
                                          'class': 'form-control',
                                          'data-parsley-required': "false"}))
    vdrl_test = forms.CharField(label='VDRL Test',
                                widget=forms.TextInput(
                                    attrs={'placeholder': _(''),
                                           'class': 'form-control',
                                           'data-parsley-required': "false"}))
    pregnancy_test = forms.CharField(label='Pregnancy Test', required=False,
                                     widget=forms.TextInput(
                                         attrs={'placeholder': _(''),
                                                'class': 'form-control',
                                                'data-parsley-required': "false"}))
    covid19_test = forms.CharField(label='COVID-19 Test', required=False,
                                   widget=forms.TextInput(
                                       attrs={'placeholder': _(''),
                                              'class': 'form-control',
                                              'data-parsley-required': "false"}))
    hiv_test = forms.CharField(label='HIV Test', required=False,
                               widget=forms.TextInput(
                                   attrs={'placeholder': _(''),
                                          'class': 'form-control',
                                          'data-parsley-required': "false"}))
    consent = forms.BooleanField(label='Consent')
    xray_report = forms.CharField(label='X-Ray Report',
                                  required=False,
                                  widget=forms.TextInput(
                                      attrs={'placeholder': _(''),
                                             'class': 'form-control',
                                             'data-parsley-required': "false"}))
    medical_observations = forms.CharField(label='Any other medical observations or comments by the doctor',
                                           widget=forms.TextInput(
                                               attrs={'placeholder': _(''),
                                                      'class': 'form-control',
                                                      'data-parsley-required': "false"}))
    medical_practitioner_certify=forms.CharField(
                                                 widget=forms.TextInput(
                                                     attrs={'placeholder': _(''),
                                                            'class': 'form-control',
                                                            'data-parsley-required': "false"}))

    medical_practitioner_name = forms.CharField(label='Name of Medical Practitioner',
                                                widget=forms.TextInput(
                                                    attrs={'placeholder': _(''),
                                                           'class': 'form-control',
                                                           'data-parsley-required': "false"}))

    medical_practitioner_date = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': _('Select date'),
                   'class': 'form-control',
                   'data-parsley-notfuturedate': "dd-M-yy",
                   'id': 'datepicker',
                   'data-parsley-group': 'primary'}))

class IndividualCarePlanForm(forms.Form):
    child_name = forms.CharField(label='CHILD NAME',
                                 widget=forms.TextInput(
                                     attrs={'placeholder': _(''),
                                            'class': 'form-control',
                                            'data-parsley-required': "false"}))
    admission_no = forms.CharField(label='ADMISSION NO.' ,
                                   widget=forms.TextInput(
                                       attrs={'placeholder': _(''),
                                              'class': 'form-control',
                                              'data-parsley-required': "false"}))
    needs_of_the_child = forms.CharField(label='NEEDS OF THE CHILD',
                                         widget=forms.TextInput(
                                             attrs={'placeholder': _(''),
                                                    'class': 'form-control',
                                                    'data-parsley-required': "false"}))
    family_child_risks = forms.CharField(label='FAMILY / CHILD RISKS',
                                         widget=forms.TextInput(
                                             attrs={'placeholder': _(''),
                                                    'class': 'form-control',
                                                    'data-parsley-required': "false"}))
    family_resources = forms.CharField(label='FAMILY RESOURCES',
                                       widget=forms.TextInput(
                                           attrs={'placeholder': _(''),
                                                  'class': 'form-control',
                                                  'data-parsley-required': "false"}))
    starting_date = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': _('Select date'),
                   'class': 'form-control',
                   'data-parsley-notfuturedate': "dd-M-yy",
                   'id': 'datepicker',
                   'data-parsley-group': 'primary'}))
    ending_date = forms.DateField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': _('Select date'),
                   'class': 'form-control',
                   'data-parsley-notfuturedate': "dd-M-yy",
                   'id': 'datepicker',
                   'data-parsley-group': 'primary'}))
    officers_comment = forms.CharField(label="Officer’s Comment",
                                       widget=forms.TextInput(
                                           attrs={'placeholder': _(''),
                                                  'class': 'form-control',
                                                  'data-parsley-required': "false"}))
    goal = forms.CharField(label="Officer’s Comment",
                                       widget=forms.TextInput(
                                           attrs={'placeholder': _(''),
                                                  'class': 'form-control',
                                                  'data-parsley-required': "false"}))
    sub_goal_action_plan = forms.ChoiceField(label='SUB-GOAL/ACTION PLAN',
                                             choices=SUB_GOAL,
                                             widget=forms.Select)
    sub_goal_action_plan_1 = forms.CharField(label='SUB-GOAL/ACTION PLAN 1-1',
                                             widget=forms.TextInput(
                                                 attrs={'placeholder': _(''),
                                                        'class': 'form-control',
                                                        'data-parsley-required': "false"}))
    sub_goal_action_plan_2 = forms.CharField(label='SUB-GOAL/ACTION PLAN 1-2',
                                             widget=forms.TextInput(
                                                 attrs={'placeholder': _(''),
                                                        'class': 'form-control',
                                                        'data-parsley-required': "false"}))
    sub_goal_action_plan_3 = forms.CharField(label='SUB-GOAL/ACTION PLAN 2-1',
                                             widget=forms.TextInput(
                                                 attrs={'placeholder': _(''),
                                                        'class': 'form-control',
                                                        'data-parsley-required': "false"}))
    sub_goal_action_plan_4 = forms.CharField(label='SUB-GOAL/ACTION PLAN 2-2',
                                             widget=forms.TextInput(
                                                 attrs={'placeholder': _(''),
                                                        'class': 'form-control',
                                                        'data-parsley-required': "false"}))
    sub_goal_action_plan_5 = forms.CharField(label='SUB-GOAL/ACTION PLAN 3-1',
                                             widget=forms.TextInput(
                                                 attrs={'placeholder': _(''),
                                                        'class': 'form-control',
                                                        'data-parsley-required': "false"}))
    sub_goal_action_plan_6 = forms.CharField(label='SUB-GOAL/ACTION PLAN 3-2',
                                             widget=forms.TextInput(
                                                 attrs={'placeholder': _(''),
                                                        'class': 'form-control',
                                                        'data-parsley-required': "false"}))

    counsellors_recommendations = forms.CharField(label='COUNSELLORS RECOMMENDATIONS',
                                                  widget=forms.TextInput(
                                                      attrs={'placeholder': _(''),
                                                             'class': 'form-control',
                                                             'data-parsley-required': "false"}))
    family_conferencing_result = forms.CharField(label='FAMILY CONFERENCING RESULT')
    family_conferencing_date = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': _('Select date'),
                   'class': 'form-control',
                   'data-parsley-notfuturedate': "dd-M-yy",
                   'id': 'datepicker',
                   'data-parsley-group': 'primary'}))
    family_conferencing_venue = forms.CharField(label='Venue')
    family_conferencing_participants = forms.CharField(label='Participants',
                                                       widget=forms.TextInput(
                                                           attrs={'placeholder': _(''),
                                                                  'class': 'form-control',
                                                                  'data-parsley-required': "false"}))
    family_conferencing_result = forms.CharField(label='Result',
                                                 widget=forms.TextInput(
                                                     attrs={'placeholder': _(''),
                                                            'class': 'form-control',
                                                            'data-parsley-required': "false"}))




class LeaveOfAbsenceForm(forms.Form):
    name = forms.CharField(label='Name')
    admission_number = forms.CharField(label='Admission Number')
    dormitory = forms.CharField(label='Dormitory')
    class_name = forms.CharField(label='Class')
    guardian_name = forms.CharField(label='Name and Relationship of Guardian')
    guardian_relationship = forms.ChoiceField(
        choices=list_relationship,
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control'}))
    guardian_address = forms.CharField(label='Address of Guardian')
    guardian_contact_measures = forms.CharField(label='Measures to Contact Guardian (nearest phone etc.)')
    leave_period = forms.CharField(label='Period of Leave of Absence')
    leave_conditions = forms.CharField(label='Conditions to Grant Leave of Absence')
    child_health_conditions = forms.CharField(label='Mental and Physical Health Conditions of the child')
    risk_of_escape = forms.CharField(label='Risk of Escape')
    sco_spo_information = forms.CharField(label='Information from SCO / SPO')
    relationship_with_guardian = forms.ChoiceField(
        choices=list_relationship,
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control'}))
    collecting_sending_guardians = forms.CharField(label='Guardians who Collect/Send Back')
    good_behavior_at_rs = forms.CharField(label='Good Behavior Maintained at the RS')
    rule_violations = forms.CharField(label='Rule Violation Committed so far')
    previous_leave_problem = forms.CharField(label='Problem with Previous Leave')
    others = forms.CharField(label='Others')
    personal_officer_opinion = forms.CharField(label='Opinion of Personal Officer')
    school_committee_decision = forms.CharField(label='Decision by the School Committee')






