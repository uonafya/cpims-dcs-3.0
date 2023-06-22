from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import RadioSelect

from cpovc_main.functions import get_list, get_org_units_list
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


ENTRY_CHOICES = (
    ("", "Select"),
    ("identified", "Was identified"),
    ("referred", "Was referred"),
    ("own_will", "Came of own will"),
)

YES_NO_CHOICES = (("AYES", "Yes"), ("ANNO", "No"))


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