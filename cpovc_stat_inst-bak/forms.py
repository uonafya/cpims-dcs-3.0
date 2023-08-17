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
    ("", "Select"),
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
    ("", "Select"),
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
    ("", "Select"),
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
    ("", "Select"),
    ("New_admission", "New admission"),
    ("readmission_after_escape", "readmission after escape"),
    ("readmission_on_relapse", "readmission on relapse"),
    ("transfer_in", "transfer in"),
)
SI_INSTITUTION = (
    ("", "Select"),
    ("Remand", "Remand Homes"),
    ("Rehabilitation", "Rehabilitation Centres"),
    ("Rescue", "Rescue Centres"),
)

NEEDS_RISK_ASSESSMENT = (
    (
        "1",
        "Has no parent or guardian, or has been abandoned by his parent or guardian, or is destitute.",
    ),
    ("2", "Found begging or receiving alms and parents or guardians cannot be traced."),
    ("3", "The parent has been imprisoned and there are no alternative care options."),
    (
        "4",
        "Whose parent or guardian does not, or is unable or unfit to exercise proper care and guardianship and there is no alternative care option",
    ),
    (
        "5",
        "Who is prevented from receiving education and there are no proper interventions in place",
    ),
    (
        "6",
        "Who, being a female is subjected or is likely to be subjected tofemale circumcision or early  marriage or customs and practices prejudicial to the childs life, education, and health",
    ),
    (
        "7",
        "Who is being kept in any premises which, in the opinion of a medical officer, are overcrowded,  unsanitary or dangerous;",
    ),
    ("8", "Who is exposed to domestic violence"),
    (
        "9",
        "Who is pregnant and living within the same household as the perpetrator who committed the offence",
    ),
    ("10", "Whose parent is terminally ill with no access to alternative care"),
    ("11", "Who is disabled and is being unlawfully confined or ill_treated"),
    (
        "12",
        "Who has been sexually abused or is likely to be exposed to sexual abuse and exploitation including prostitution and pornography",
    ),
    (
        "13",
        "Who is engaged in any work likely to harm his health, education, mental or moral development",
    ),
    (
        "14",
        "Who is displaced as a consequence of war, civil disturbances or natural disasters",
    ),
)

NEED_RISK_SCALE = (
    ("Area_1", "Area 1 _ Prior or Current Offences/Dispositions"),
    ("Area_2", "Area 2 _ Family Circumstances/Parenting"),
    ("Area_3", "Area 3 _ Education/Employment"),
    ("Area_4", "Area 4 _ Peer Relations"),
    ("Area_5", "Area 5 _ Substance Abuse"),
    ("Area_6", "Area 6 _ Leisure/Recreation"),
    ("Area_7", "Area 7 _ Street Experience"),
    ("Area_8", "Area 8 _ Personality/Behaviour"),
    ("Area_9", "Area 9 _ Attitudes/Orientation"),
)

RELATIVE_CHOICES = [
    ("relative", "Relative"),
    ("friend", "Friend"),
]

REASON_FOR_REFERRAL = (
    ("By court order", "By court order"),
    ("Supervision", "Supervision"),
    ("Others", "Others"),
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
    institution_type = forms.ChoiceField(
        choices=SI_INSTITUTION,
        required=False,
        widget=forms.Select(
            attrs={
                "placeholder": _("Institution to be Admitted"),
                "class": "form-control",
                "id": "institution_type",
            }
        ),
    )
    institution_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Name of the Institution"),
                "class": "form-control",
                "id": "institution_name",
            }
        ),
    )
    child_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Name of the child"),
                "class": "form-control",
                "id": "child_name",
            }
        ),
    )
    nickname = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Child Nickname"),
                "class": "form-control",
                "id": "nickname",
            }
        ),
    )
    sex = forms.ChoiceField(
        choices=(("M", "Male"), ("F", "Female")),
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "id": "gender"}),
    )
    age = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Age"),
                "class": "form-control",
                "id": "age",
                "data_parsley_required": "true",
                "data_parsley_group": "group0",
            }
        )
    )
    date_of_admission = forms.DateField(
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Date Of Admission"),
                "class": "form-control",
                "id": "admission_date",
                "data_parsley_required": "true",
                "data_parsley_group": "group0",
            }
        )
    )
    admission_no = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Admission number"),
                "class": "form-control",
                "id": "admission_no",
                "data_parsley_required": "false",
                "data_parsley_group": "group0",
            }
        )
    )
    current_year_of_school = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Year of school"),
                "class": "form-control",
                "id": "current_year_of_school",
                "data_parsley_required": "true",
                "data_parsley_group": "group0",
            }
        ),
    )
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
        choices=CHILD_CATEGORY,
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "id": "child_category",
            }
        ),
    )
    abused_child_desc = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Abuse child description"),
                "class": "form-control",
                "id": "abused_child_desc",
            }
        ),
    )
    referral_source_others = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "placeholder": _("Specify other referral sources"),
                "class": "form-control",
                "id": "referral_source_others",
                "row": "1",
            }
        ),
    )
    referrer_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Referrer Name"),
                "class": "form-control",
                "id": "referrer_name",
            }
        ),
    )
    referrer_address = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Referrer address"),
                "class": "form-control",
                "id": "referrer_address",
            }
        ),
    )
    referrer_phone = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Referrer name"),
                "class": "form-control",
                "id": "referrer_phone",
            }
        ),
    )
    not_contact_child = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        required=False,
        widget=forms.RadioSelect(
            attrs={
                "placeholder": _("Not to contact child"),
                "id": "not_contact_child",
            }
        ),
    )

    name_not_contact_child = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Person not to contact child"),
                "class": "form-control",
                "id": "name_not_contact_child",
            }
        ),
    )
    relationship_to_child_not_contact_child = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Realtion not to contact child"),
                "class": "form-control",
                "id": "relationship_to_child_not_contact_child",
            }
        ),
    )
    consent_form_signed = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        required=False,
        widget=forms.RadioSelect(
            attrs={
                "class": "radio-inline",
                "id": "consent_form_signed",
            }
        ),
    )
    commital_court_order = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        required=False,
        widget=forms.RadioSelect(
            attrs={
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
    
class SICaseReferral(forms.Form):
    reason_for_referral = forms.MultipleChoiceField(
        choices=REASON_FOR_REFERRAL,
        widget=forms.CheckboxSelectMultiple(
            attrs={'data-parsley-required': 'true'}))
    file_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('File Name'),
               'class': 'form-control',
               'readonly': 'true',
               'id': 'file_name'}))
    
class RemandHomeEscape(forms.Form):
    admission_no = forms.CharField(max_length=100)
    id_no = forms.CharField(max_length=100)
    court_file_no = forms.CharField(max_length=100)
    police_file_no = forms.CharField(max_length=100)
    ethnic_group = forms.CharField(max_length=100)
    address_of_remandhome = forms.CharField(max_length=100)
    clan = forms.CharField(max_length=100)
    county = forms.CharField(max_length=100)
    location = forms.CharField(max_length=100)
    village = forms.CharField(max_length=100)
    mode_of_escape = forms.CharField(max_length=100)
    gvt_clothing_taken = forms.CharField(max_length=250)
    circumstances_of_escape = forms.CharField(max_length=250)
    officer_incharge = forms.CharField(max_length=250)
    ward = forms.CharField(max_length=250)
    sublocation = forms.CharField(max_length=250)
    sub_chief = forms.CharField(max_length=250)
    criminal_case_no = forms.CharField(max_length=250)
    steps_taken_torecapture = forms.CharField(max_length=250)
    description_of_escape = forms.CharField(max_length=250)
    escape_under_supervision_of = forms.CharField(max_length=250)
    station = forms.CharField(max_length=250)
    date_of_order= forms.CharField(
        required=False,
        widget=forms.DateInput(
            attrs={'placeholder': _('Select date'),
                   'class': 'form-control',
                   'id': 'datepicker'},

                   ))
    date_of_escape = forms.CharField(
        required=False,
        widget=forms.DateInput(
            attrs={'placeholder': _('Select date'),
                   'class': 'form-control',
                   'id': 'datepicker'},

                   ))
    date__ = forms.CharField(
        required=False,
        widget=forms.DateInput(
            attrs={'placeholder': _('Select date'),
                   'class': 'form-control',
                   'id': 'datepicker'},

                   ))
   
class SICertificateofExit(forms.Form):
    admission_no = forms.CharField(max_length=100)
    date_of_admission= forms.CharField(
        required=False,
        widget=forms.DateInput(
            attrs={'placeholder': _('Select date'),
                   'class': 'form-control',
                   'id': 'datepicker'},

                   ))
    expiry_date = forms.CharField(
        required=False,
        widget=forms.DateInput(
            attrs={'placeholder': _('Select date'),
                   'class': 'form-control',
                   'id': 'datepicker'},

                   ))
    date_of_committal_order = forms.CharField(
        required=False,
        widget=forms.DateInput(
            attrs={'placeholder': _('Select date'),
                   'class': 'form-control',
                   'id': 'datepicker'},

                   ))
    date_of_exit = forms.CharField(
        required=False,
        widget=forms.DateInput(
            attrs={'placeholder': _('Select date'),
                   'class': 'form-control',
                   'id': 'datepicker'},

                   ))
    date_of_follow_up = forms.CharField(
        required=False,
        widget=forms.DateInput(
            attrs={'placeholder': _('Select date'),
                   'class': 'form-control',
                   'id': 'datepicker'},

                   ))
    reason_for_exit = forms.CharField(max_length=250)
    name_of_person_followingup = forms.CharField(max_length=100)
    name_of_organization= forms.CharField(max_length=100)
    relationship_to_child= forms.CharField(max_length=100)
    address= forms.CharField(max_length=100)
    telephone= forms.CharField(max_length=100)
    name= forms.CharField(max_length=100)
    designation= forms.CharField(max_length=100)

class SIRecordofVisits(forms.Form):
    admission_no = forms.CharField(max_length=100)
    name_of_visitor = forms.CharField(max_length=250)
    age = forms.IntegerField()
    sex = forms.ChoiceField(
        choices=(("M", "Male"), ("F", "Female")),
        required=False,
        widget=forms.Select(attrs={"class": "form-control", "id": "gender"}),
    )
    date_of_visit= forms.CharField(
        required=False,
        widget=forms.DateInput(
            attrs={'placeholder': _('Select date'),
                   'class': 'form-control',
                   'id': 'datepicker'},

                   ))
    relationship_to_child= forms.CharField(max_length=100)
    address= forms.CharField(max_length=100)
    telephone= forms.CharField(max_length=100)
    id_no= forms.CharField(max_length=100)
    type_of_communication= forms.CharField(max_length=100)
    description = forms.CharField(max_length=250)
    name_of_staff= forms.CharField(max_length=100)

class SIFamilyConference(forms.Form):
    name_of_participant = forms.CharField(max_length=100,
        widget=forms.TextInput(
            attrs={'placeholder': _('Name of Participant'),
                   'class': 'form-control',
                   'id': 'name_of_participant'}
        ) )
    relationship_to_child= forms.CharField(max_length=100,
         widget=forms.TextInput(
            attrs={'placeholder': _('Relationship with the child'),
                   'class': 'form-control',
                   'id': 'relationship_child'}
        ) 
                                           )
    address= forms.CharField(max_length=100,
            widget=forms.TextInput(
            attrs={'placeholder': _('Address'),
                   'class': 'form-control',
                   'id': 'address'}
        ) 
                             )
    telephone= forms.CharField(max_length=100, widget=forms.TextInput(
            attrs={'placeholder': _('Telephone'),
                   'class': 'form-control',
                   'id': 'telephone'}
        ) )
    underlying_issues = forms.CharField(max_length=250,widget=forms.TextInput(
            attrs={'placeholder': _('Underlying Issues'),
                   'class': 'form-control',
                   'id': 'underlying_issues'}
        ))
    presenting_issues = forms.CharField(max_length=250,widget=forms.TextInput(
            attrs={'placeholder': _('Presenting Issues'),
                   'class': 'form-control',
                   'id': 'presenting_issues'}
        ))
    consensus = forms.CharField(max_length=250,widget=forms.TextInput(
            attrs={'placeholder': _('Consensus'),
                   'class': 'form-control',
                   'id': 'consensus'}
        ))
    family_promise = forms.CharField(max_length=250,widget=forms.TextInput(
            attrs={'placeholder': _('Family Promise of Commitment'),
                   'class': 'form-control',
                   'id': 'family_promise'}
        ))
    child_promise = forms.CharField(max_length=250,widget=forms.TextInput(
            attrs={'placeholder': _('Childs Promise of Commitment'),
                   'class': 'form-control',
                   'id': 'child_promise'}
        ))
    child_name = forms.CharField(max_length=100,widget=forms.TextInput(
            attrs={'placeholder': _('Childs Name'),
                   'class': 'form-control',
                   'id': 'child_name'}
        ))
    family_member= forms.CharField(max_length=100,widget=forms.TextInput(
            attrs={'placeholder': _('Name of family member'),
                   'class': 'form-control',
                   'id': 'family_member'}
        ))
    significant_other= forms.CharField(max_length=100,widget=forms.TextInput(
            attrs={'placeholder': _('Significant Other'),
                   'class': 'form-control',
                   'id': 'significant_other'}
        ))
    official_handling= forms.CharField(max_length=100,widget=forms.TextInput(
            attrs={'placeholder': _('Official handling the case'),
                   'class': 'form-control',
                   'id': 'official_handling'}
        ))
    follow_up_meeting= forms.CharField(max_length=100,widget=forms.TextInput(
            attrs={'placeholder': _('Follow up meeting to be held at?'),
                   'class': 'form-control',
                   'id': 'follow_up_meeting'}
        ))
    family_contactperson= forms.CharField(max_length=100,widget=forms.TextInput(
            attrs={'placeholder': _('Family Contact Person'),
                   'class': 'form-control',
                   'id': 'family_contactperson'}
        ))
    family_contactdetails= forms.CharField(max_length=100,widget=forms.TextInput(
            attrs={'placeholder': _('Contact details '),
                   'class': 'form-control',
                   'id': 'family_contactdetails'}
        ))
    follow_up_date= forms.CharField(
        required=False,
        widget=forms.DateInput(
            attrs={'placeholder': _('Select date'),
                   'class': 'form-control',
                   'id': 'datepicker'},

                   ))
   
class SIReleaseForm(forms.Form):
    admission_no = forms.CharField(max_length=100,widget=forms.TextInput(
            attrs={'placeholder': _('Admission Number'),
                   'class': 'form-control',
                   'id': 'admission_no'}
        ))
    name = forms.CharField(max_length=100,
        widget=forms.TextInput(
            attrs={'placeholder': _('Name'),
                   'class': 'form-control',
                   'id': 'name'}
        ) )
    id_no= forms.CharField(max_length=100,
         widget=forms.TextInput(
            attrs={'placeholder': _('ID Number'),
                   'class': 'form-control',
                   'id': 'id_no'}
        ) )
    telephone= forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'placeholder': _('Telephone'),
                'class': 'form-control',
                'id': 'telephone'}
    ) )
    occupation= forms.CharField(max_length=100,
            widget=forms.TextInput(
            attrs={'placeholder': _('Occupation'),
                   'class': 'form-control',
                   'id': 'occupation'}
        ))
    residence = forms.CharField(max_length=250,widget=forms.TextInput(
            attrs={'placeholder': _('Residence'),
                   'class': 'form-control',
                   'id': 'residence'}
        ))
    relation_to_child = forms.CharField(max_length=250,widget=forms.TextInput(
            attrs={'placeholder': _('Relation to Child'),
                   'class': 'form-control',
                   'id': 'relation_to_child'}
        ))
   
class SIChildProfile(forms.Form):
    record_date= forms.CharField(
        required=False,
        widget=forms.DateInput(
            attrs={'placeholder': _('Select date'),
                   'class': 'form-control',
                   'id': 'datepicker'},

                   ))
    name_of_institution = forms.CharField(max_length=100,widget=forms.TextInput(
            attrs={'placeholder': _('Name of Institution'),
                   'class': 'form-control',
                   'id': 'name_of_institution'}
        ))
    scco_addressed = forms.CharField(max_length=100,widget=forms.TextInput(
            attrs={'placeholder': _('SCCO Addressed'),
                   'class': 'form-control',
                   'id': 'scco_addressed'}
        ))
    old_released_to = forms.CharField(max_length=100,
        widget=forms.TextInput(
            attrs={'placeholder': _('Old address to be released to'),
                   'class': 'form-control',
                   'id': 'old_released_to'}
        ) )
    new_released_to = forms.CharField(max_length=100,
        widget=forms.TextInput(
            attrs={'placeholder': _('New address to be released to'),
                   'class': 'form-control',
                   'id': 'new_released_to'}
        ) )
    guardian_job = forms.CharField(max_length=100,
        widget=forms.TextInput(
            attrs={'placeholder': _('Job of guardian'),
                   'class': 'form-control',
                   'id': 'guardian_job'}
        ) )
    relation_guardian= forms.CharField(max_length=100,
         widget=forms.TextInput(
            attrs={'placeholder': _('Relation with the guardian'),
                   'class': 'form-control',
                   'id': 'relation_guardian'}
        ) )
    expiration_date= forms.CharField(
        required=False,
        widget=forms.DateInput(
            attrs={'placeholder': _('Select date'),
                   'class': 'form-control',
                   'id': 'datepicker'},

                   ))
    reason_forchange= forms.CharField(max_length=250, widget=forms.TextInput(
        attrs={'placeholder': _('Reason for change'),
                'class': 'form-control',
                'id': 'reason_forchange'}
    ) )
    life_planning= forms.CharField(max_length=100,
            widget=forms.TextInput(
            attrs={'placeholder': _('Life planning (interest and aptitude)'),
                   'class': 'form-control',
                   'id': 'life_planning'}
        ))
    mental_state = forms.CharField(max_length=250,widget=forms.TextInput(
            attrs={'placeholder': _('Mental and Physical states'),
                   'class': 'form-control',
                   'id': 'mental_state'}
        ))
    other_changes = forms.CharField(max_length=250,widget=forms.TextInput(
            attrs={'placeholder': _('Other Changes'),
                   'class': 'form-control',
                   'id': 'other_changes'}
        ))
   

    health_status = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "placeholder": _("Health Situation"),
                "class": "form-control",
                "id": "health_status",
                "rows": "2",
            }
        ),
    )

    special_needs = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "placeholder": _("Special needs"),
                "class": "form-control",
                "id": "special_needs",
                "rows": "2",
            }
        ),
    )

    workforce_id = forms.IntegerField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Workforce ID"),
                "class": "form-control",
                "id": "workforce_id",
            }
        ),
    )
    audit_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "data_parsley_required": "true",
                "id": "audit_date",
            }
        ),
    )


class SINeedRiskAssessment(forms.Form):
    needrisk_assess = forms.MultipleChoiceField(
        choices=NEEDS_RISK_ASSESSMENT,
        # required=False,
        widget=forms.CheckboxSelectMultiple(
            # attrs={
            #     "class": "form-control",
            #     "id": "needrisk_assess",
            #     "row": "8"
            # }
        ),
    )
    previous_institution = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Previous Institution"),
                "class": "form-control",
                "id": "previous_institution",
            }
        ),
    )

    prev_inst_release_date = forms.DateField(
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Date Of Release"),
                "class": "form-control",
                "id": "prev_inst_release_date",
                "data_parsley_required": "true",
                "data_parsley_group": "group0",
            }
        )
    )
    workforce_id = forms.IntegerField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Workforce ID"),
                "class": "form-control",
                "id": "workforce_id",
            }
        ),
    )
    audit_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "data_parsley_required": "true",
                "id": "audit_date",
            }
        ),
    )


class SINeedRiskScale(forms.Form):
    needrisk_scale = forms.ChoiceField(
        choices=NEED_RISK_SCALE,
        # required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "id": "needrisk_scale",
            }
        ),
    )
    needrisk_description = forms.ChoiceField(
        choices=NEED_RISK_SCALE,
        # required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "id": "needrisk_description",
            }
        ),
    )
    needrisk_comment = forms.CharField(
        # choices=NEED_RISK_SCALE,
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "id": "needrisk_comment",
                "row": "2",
            }
        ),
    )
    needrisk_list = forms.CharField(
        widget=forms.TextInput(attrs={"type": "hidden", "id": "needrisk_list"})
    )


class SIVacancyApp(forms.Form):
    ref_no = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "id": "ref_no"}),
    )
    date_of_application = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "data_parsley_required": "true",
                "id": "date_of_application",
            }
        ),
    )

    crc_no = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "id": "crc_no"}),
    )
    pnc_no = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "id": "pnc_no"}),
    )

    court_number = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "id": "court_number"}),
    )
    judge_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "id": "judge_name"}),
    )
    child_held_at = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "id": "child_held_at"}),
    )
    date_of_next_mention = forms.DateField(
        widget=forms.DateInput(
            attrs={"class": "form-control", "id": "date_of_next_mention"}
        ),
    )
    requesting_officer = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "requesting_officer"}
        ),
    )
    designation = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "id": "designation"}),
    )
    sub_county_children_officer = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "sub_county_children_officer"}
        ),
    )


class SIVacancyConfirm(forms.Form):
    institution_applied = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "institution_applied"}
        ),
    )
    magistrate_court = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "magistrate_court"}
        ),
    )
    case_no = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "id": "case_no"}),
    )
    months = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control", "id": "months"}),
    )
    ref_no = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "id": "ref_no"}),
    )
    date_of_enrollment = forms.DateField(
        widget=forms.DateInput(
            attrs={"class": "form-control", "id": "date_of_enrollment"}
        ),
    )


class SISocialInquiry(forms.Form):
    # Child's Details
    school_attended = forms.CharField(
        label="Name of School attended",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "school_attended"}
        ),
    )
    class_name = forms.CharField(
        label="Class",
        widget=forms.TextInput(attrs={"class": "form-control", "id": "class_name"}),
    )
    year = forms.IntegerField(
        label="Year",
        widget=forms.NumberInput(attrs={"class": "form-control", "id": "year"}),
    )
    headmaster_teacher_name = forms.CharField(
        label="Name of H/Master/teacher",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "headmaster_teacher_name"}
        ),
    )
    hobbies = forms.CharField(
        label="Hobbies",
        widget=forms.TextInput(attrs={"class": "form-control", "id": "hobbies"}),
    )
    types_of_friends = forms.CharField(
        label="Types of friends",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "types_of_friends"}
        ),
    )
    mental_physical_condition = forms.CharField(
        label="Mental/Physical condition",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "mental_physical_condition"}
        ),
    )
    person_type = forms.ChoiceField(
        choices=RELATIVE_CHOICES,
        label="Any other Person option",
        widget=forms.Select(attrs={"class": "form-control", "id": "person_type"}),
    )

    # Person Details
    name = forms.CharField(
        label="Name",
        widget=forms.TextInput(attrs={"class": "form-control", "id": "person_name"}),
    )
    county = forms.CharField(
        label="County",
        widget=forms.TextInput(attrs={"class": "form-control", "id": "person_county"}),
    )
    sub_county = forms.CharField(
        label="Sub_county",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "person_sub_county"}
        ),
    )
    ward = forms.CharField(
        label="Ward",
        widget=forms.TextInput(attrs={"class": "form-control", "id": "person_ward"}),
    )
    location = forms.CharField(
        label="Location",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "person_location"}
        ),
    )
    sub_location = forms.CharField(
        label="Sub_location",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "person_sub_location"}
        ),
    )
    village = forms.CharField(
        label="Village",
        widget=forms.TextInput(attrs={"class": "form-control", "id": "person_village"}),
    )
    telephone = forms.CharField(
        label="Telephone",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "person_telephone"}
        ),
    )
    contact_address = forms.CharField(
        label="Contact Address",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "person_contact_address"}
        ),
    )

    # Child's Close Relative
    has_close_relative = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        required=False,
        widget=forms.RadioSelect(
            attrs={
                "id": "has_close_relative",
                "class": "radio-inline"
            }
        ),
    )
    relative_name = forms.CharField(
        label="County",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "child_relative_county"}
        ),
    )
    child_relative_county = forms.CharField(
        label="County",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "child_relative_county"}
        ),
    )
    child_relative_sub_county = forms.CharField(
        label="Sub_county",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "child_relative_sub_county"}
        ),
    )
    child_relative_location = forms.CharField(
        label="Location",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "child_relative_location"}
        ),
    )
    child_relative_village = forms.CharField(
        label="Village",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "child_relative_village"}
        ),
    )
    child_relative_contact_address = forms.CharField(
        label="Contact Address",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "child_relative_contact_address"}
        ),
    )
    relative_telephone = forms.CharField(
        label="Telephone",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "relative_telephone"}
        ),
    )

    # Guardian Details
    guardian_county = forms.CharField(
        label="County",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "guardian_county"}
        ),
    )
    guardian_location = forms.CharField(
        label="Location",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "guardian_location"}
        ),
    )
    guardian_village = forms.CharField(
        label="Village",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "guardian_village"}
        ),
    )
    guardian_contact_address = forms.CharField(
        label="Contact Address",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "guardian_contact_address"}
        ),
    )

    # Other Details
    chief_name = forms.CharField(
        label="Name of Chief",
        widget=forms.TextInput(attrs={"class": "form-control", "id": "chief_name"}),
    )
    assistant_chief_name = forms.CharField(
        label="Name of Assistant Chief/Village elder",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "assistant_chief_name"}
        ),
    )
    neighbours = forms.CharField(
        label="Name of any Neighbours",
        widget=forms.TextInput(attrs={"class": "form-control", "id": "neighbours"}),
    )
    nearest_church_mosque = forms.CharField(
        label="Nearest Church/Mosque",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "nearest_church_mosque"}
        ),
    )
    religious_leader_name = forms.CharField(
        label="Name of Religious Leader",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "religious_leader_name"}
        ),
    )
    nearest_school = forms.CharField(
        label="Nearest School",
        widget=forms.TextInput(attrs={"class": "form-control", "id": "nearest_school"}),
    )
    nearest_market_shop = forms.CharField(
        label="Nearest Market/shop",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "nearest_market_shop"}
        ),
    )
    nearest_matatu_stage = forms.CharField(
        label="Nearest Matatu Stage",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "nearest_matatu_stage"}
        ),
    )
    nearest_police_station = forms.CharField(
        label="Nearest Police Station",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "nearest_police_station"}
        ),
    )

    # Father Details
    father_alive = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        required=False,
        widget=forms.RadioSelect(
            attrs={
                "id": "father_alive",
                "class": "radio-inline"
            }
        ),
    )
    father_name = forms.CharField(
        label="Name of Father",
        widget=forms.TextInput(attrs={"class": "form-control", "id": "father_name"}),
    )
    father_age = forms.IntegerField(
        label="Age",
        widget=forms.NumberInput(attrs={"class": "form-control", "id": "father_age"}),
    )
    father_education_level = forms.CharField(
        label="Level of Education",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "father_education_level"}
        ),
    )
    father_occupation = forms.CharField(
        label="Occupation",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "father_occupation"}
        ),
    )
    father_address = forms.CharField(
        label="Address",
        widget=forms.TextInput(attrs={"class": "form-control", "id": "father_address"}),
    )
    father_telephone = forms.CharField(
        label="Tel",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "father_telephone"}
        ),
    )
    father_id_number = forms.CharField(
        label="ID No",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "father_id_number"}
        ),
    )
    father_estate_name = forms.CharField(
        label="Name of Estate",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "father_estate_name"}
        ),
    )
    father_road_name = forms.CharField(
        label="Name of Road",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "father_road_name"}
        ),
    )

    # Mother Details
    mother_alive = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        required=False,
        widget=forms.RadioSelect(
            attrs={
                "id": "mother_alive",
                "class": "radio-inline"
            }
        ),
    )
    mother_name = forms.CharField(
        label="Name of Mother",
        widget=forms.TextInput(attrs={"class": "form-control", "id": "mother_name"}),
    )
    mother_age = forms.IntegerField(
        label="Age",
        widget=forms.NumberInput(attrs={"class": "form-control", "id": "mother_age"}),
    )
    mother_education_level = forms.CharField(
        label="Level of Education",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "mother_education_level"}
        ),
    )
    mother_occupation = forms.CharField(
        label="Occupation",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "mother_occupation"}
        ),
    )
    mother_address = forms.CharField(
        label="Address",
        widget=forms.TextInput(attrs={"class": "form-control", "id": "mother_address"}),
    )
    mother_telephone = forms.CharField(
        label="Tel",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "mother_telephone"}
        ),
    )
    mother_id_number = forms.CharField(
        label="ID No",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "mother_id_number"}
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

