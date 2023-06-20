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

YES_NO_CHOICES = (
    ("yes", "Yes"),
    ("no", "No"),
)

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
RELIGION= (("Christian", "Christian"),
            ("Muslim", "Muslim"),
            ("Hindu", "Hindu"))
REASON_FOR_ADMISSION=(("School/education access", "School/education access"),
                                                               ("Poverty/family vulnerability", "Poverty/family vulnerability"),
                                                               ("Abuse or neglect at home", "Abuse or neglect at home"),
                                                               ("Child abandoned", "Child abandoned"),
                                                               ("Child on the street", "Child on the street"),
                                                               ("HIV & AIDS or other chronic illness", "HIV & AIDS or other chronic illness"),
                                                               ("Special needs (disability)", "Special needs (disability)"),
                                                               ("Child victim of human trafficking", "Child victim of human trafficking"),
                                                               ("Orphan", "Orphan"),
                                                               ("Child lost and found", "Child lost and found"),
                                                               ("Separated/unaccompanied", "Separated/unaccompanied"),
                                                               ("Child of imprisoned parent", "Child of imprisoned parent"),
                                                               ("Other", "Other"))
ALTERNATIVE_CARE=(
    ("Kinship Care", "Kinship Care"),
    ("Foster Care", "Foster Care"),
    ("Temporary Shelter", "Temporary Shelter"),
    ("CCI", "CCI"),
    ("SCI", "SCI"),
    ("Supported child-headed household", "Supported child-headed household"),
    ("Supported Independent Living", "Supported Independent Living"),
    ("Guardianship", "Guardianship"),
    ("Kafaalah", "Kafaalah"),
    ("Other", "Other")
                  )

YES_NO_NA_CHOICES=(
    ("Yes", "Yes"),
    ("No", "No"),
    ("unsure", "Unsure"),
    ("N/A", "N/A")
)
OTHER_FORMS_OF_ADMISSION=(
    ("Self-referral", "Self-referral"),
    ("Abandoned at CCI", "Abandoned at CCI")
)
EXHIBITED_BEHAVIOR=(
        ("self_harm", "Self harm"),
        ("history_of_abuse", "Known history of abuse"),
        ("inappropriate_sexual_behavior", "Inappropriate sexual behaviour"),
        ("substance_abuse", "Drug and/or substance abuse"),
        ("potential_abuse_symptoms", "Displays potential symptoms of abuse"),
        ("emotional_distress", "Displays signs of emotional distress"),
        ("risk_behavior", "Exhibits risk"),
        ("change_in_behavior", "Any unexplained recent change in behavior")
)
LEVEL=(
    ("high", "High"),
    ("medium", "Medium"),
    ("low", "Low"))
AGE_DYNAMICS=(
    ("older", "Much older"),
    ("younger", "Much younger"),
    ("same", "Same age")
)
QUALITY=(
   ("positive", "Positive"),
   ("negative", "Negative")
)

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
    relationship_to_child_not_contact_child = forms.CharField(max_length=100)
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


class SIChildIdentification(forms.Form):
    case_number = forms.CharField(label="Child’s Case Number")

    current_location = forms.CharField(label="Child’s Current Location")

    assessment_started = forms.DateField(label="Date Assessment Started")

    first_name = forms.CharField(label="First name")

    middle_name = forms.CharField(label="Middle name")

    surname = forms.CharField(label="Surname")

    nickname = forms.CharField(label="Nickname or likes to be called")

    sex = forms.ChoiceField(label="Sex", choices=GENDER)

    dob_day = forms.IntegerField(label="Date of birth (DOB): DD", min_value=1, max_value=31)

    dob_month = forms.IntegerField(label="Date of birth (DOB): MM", min_value=1, max_value=12)

    dob_year = forms.IntegerField(label="Date of birth (DOB): YYYY", min_value=1900, max_value=2100)

    age_estimate = forms.IntegerField(label="Estimate of approximate age if DOB unknown")

    current_age_months = forms.IntegerField(label="Current age (Months)", min_value=0)

    current_age_years = forms.IntegerField(label="Current age (Years)", min_value=0)

    birth_registered = forms.BooleanField(label="Birth registered?", required=False)

    birth_registration_number = forms.CharField(label="Birth registration no.", required=False)

    place_of_birth_county = forms.CharField(label="Place of birth: County")

    place_of_birth_subcounty = forms.CharField(label="Place of birth: Subcounty")

    place_of_birth_village = forms.CharField(label="Place of birth: Village")

    place_of_birth_not_known = forms.BooleanField(label="Not known", required=False)
    height = forms.CharField(label="Height")

    weight = forms.CharField(label="Weight")

    complexion = forms.CharField(label="Complexion")

    ethnicity = forms.CharField(label="Ethnicity")

    religion = forms.ChoiceField(label="Religion",
                                 choices=RELIGION)

    distinguishing_features = forms.CharField(label="Distinguishing physical features (e.g., scar or birth mark)")

    languages = forms.CharField(label="Languages")

    #DIFFUCULTY SECTION
    vision_difficulty = forms.ChoiceField(label="Does the child have difficulty seeing, even if wearing glasses?",
                                          choices=DIFFICULTY)
    hearing_difficulty = forms.ChoiceField(label="Does the child have difficulty hearing, even if using a hearing aid?",
                                           choices=DIFFICULTY)
    walking_difficulty = forms.ChoiceField(label="Does the child have difficulty walking or climbing steps?",
                                           choices=DIFFICULTY)
    memory_difficulty = forms.ChoiceField(label="Does the child have difficulty remembering or concentrating?",
                                          choices=DIFFICULTY)
    self_care_difficulty = forms.ChoiceField(label="Does the child have difficulty with self-care (e.g., washing all over or dressing)?",
                                             choices=DIFFICULTY)
    communication_difficulty = forms.ChoiceField(label="Does the child have difficulty communicating (e.g., understanding or being understood by others)?",
                                                 choices=DIFFICULTY)

    #DETAILS OPF ADMISSION TO CARE
    date_of_admission = forms.DateField(label="Date of admission")
    age_at_admission = forms.IntegerField(label="Age of the child at admission")
    other_forms_of_admission = forms.MultipleChoiceField(label="Other forms of admission",
                                                        choices=OTHER_FORMS_OF_ADMISSION,
                                                        widget=forms.CheckboxSelectMultiple)
    admission_order_issued = forms.ChoiceField(label="Was Admission Order issued?",
                                               choices=YES_NO_NA_CHOICES)
    committal_order_number = forms.CharField(label="Committal Order #", required=False)
    date_of_committal = forms.DateField(label="Date of committal", required=False)
    referring_person_name = forms.CharField(label="Name of referring person", required=False)
    referring_person_title = forms.CharField(label="Title of referring person", required=False)
    referring_person_relationship = forms.CharField(label="Relationship to the child", required=False)
    referring_person_contact = forms.CharField(label="Contact of referring person", required=False)
    referring_person_location = forms.CharField(label="Location of referring person", required=False)
    current_care_provider_name_address = forms.CharField(label="Name and address of current care provider", required=False)
    current_care_provider_phone = forms.CharField(label="Phone number of current care provider", required=False)
    current_care_provider_registration_status = forms.CharField(label="Registration status of current care provider",
                                                                required=False)
    alternative_care_placement_type = forms.MultipleChoiceField(label="Current Alternative Care Placement Type",
                                                                choices=ALTERNATIVE_CARE,
                                                                widget=forms.CheckboxSelectMultiple,
                                                                required=False)
    reasons_for_admission = forms.MultipleChoiceField(label="Reasons for admission",
                                                      choices=REASON_FOR_ADMISSION,
                                                      widget=forms.CheckboxSelectMultiple,
                                                      required=False)
    # New fields
    cci_types_names = forms.CharField(label="Types and/or names of CCIs",
                                      widget=forms.Textarea,
                                      required=False)

    child_not_in_institution_vulnerability_type = forms.CharField(label="Type of vulnerability if child not in any institution",
                                                                  required=False)

    street_connected_child_location = forms.CharField(label="Location of street connected child",
                                                      required=False)

    child_at_risk_of_separation_location = forms.CharField(label="Location of child at risk of separation",
                                                           required=False)

    other_vulnerability_type = forms.CharField(label="Other vulnerability type",
                                               widget=forms.Textarea,
                                               required=False)

    living_before_admission_names = forms.CharField(label="Name(s) of person(s) child was living with before admission",
                                                    widget=forms.Textarea,
                                                    required=False)

    living_before_admission_phone = forms.CharField(label="Phone number(s) of person(s) child was living with before admission",
                                                    required=False)

    living_before_admission_relationships = forms.CharField(label="Relationship(s) to child of person(s) child was living with before admission",
                                                            widget=forms.Textarea,
                                                            required=False)

    living_before_admission_in_cci = forms.BooleanField(label="Was this placement in a CCI?", required=False)

    living_before_admission_county = forms.CharField(label="County", required=False)

    living_before_admission_subcounty = forms.CharField(label="Subcounty", required=False)

    living_before_admission_location = forms.CharField(label="Location", required=False)

    living_before_admission_sublocation = forms.CharField(label="Sub-location", required=False)

    living_before_admission_village_estate = forms.CharField(label="Village/estate", required=False)

    living_before_admission_landmark = forms.CharField(label="Landmark (e.g. school/church/mosque/market)",
                                                       required=False)
    sibling_with_child_now = forms.BooleanField(label="Are there other sibling(s) living with the child now in this form of care?",
                                                required=False)
    sibling_with_child_now_names = forms.CharField(label="Name(s) of sibling(s) living with the child now",
                                                   widget=forms.Textarea,
                                                   required=False)
    sibling_in_care_elsewhere = forms.BooleanField(label="Are there other sibling(s) admitted into care elsewhere?",
                                                   required=False)
    sibling_in_care_elsewhere_details = forms.CharField(label="Details of sibling(s) admitted into care elsewhere",
                                                        widget=forms.Textarea,
                                                        required=False)
    #STATUS OF FAMILILY
    name = forms.CharField(label="Name")
    other_names = forms.CharField(label="Other Names")
    last_known_location = forms.CharField(label="Last Known Location")
    phone_number = forms.CharField(label="Phone No.")
    alive_choices = [
        ('Y', 'Yes'),
        ('N', 'No'),
        ('Unknown', 'Unknown')
    ]
    alive = forms.ChoiceField(label="Alive (Y/N/Unknown)", choices=alive_choices)
    mother = forms.CharField(label="Mother")
    father = forms.CharField(label="Father")
    living_together = forms.BooleanField(label="Are mother and father living together?", required=False)
    mother_current_residence_county = forms.CharField(label="Mother's current residence county", required=False)
    mother_current_residence_subcounty = forms.CharField(label="Mother's current residence subcounty", required=False)
    mother_current_residence_location = forms.CharField(label="Mother's current residence location", required=False)
    mother_current_residence_sublocation = forms.CharField(label="Mother's current residence sub-location", required=False)
    mother_current_residence_village_estate = forms.CharField(label="Mother's current residence village/estate", required=False)
    father_current_residence_county = forms.CharField(label="Father's current residence county", required=False)
    father_current_residence_subcounty = forms.CharField(label="Father's current residence subcounty", required=False)
    father_current_residence_location = forms.CharField(label="Father's current residence location", required=False)
    father_current_residence_sublocation = forms.CharField(label="Father's current residence sub-location", required=False)
    father_current_residence_village_estate = forms.CharField(label="Father's current residence village/estate", required=False)
    sibling_names = forms.CharField(label="Name(s) of other siblings currently living with caregiver", widget=forms.Textarea, required=False)
    sibling_nicknames = forms.CharField(label="Nickname(s) of other siblings currently living with caregiver", widget=forms.Textarea, required=False)
    sibling_last_known_locations = forms.CharField(label="Last known location(s) of other siblings currently living with caregiver", widget=forms.Textarea, required=False)
    sibling_education_employment = forms.CharField(label="Education / Employment of other siblings currently living with caregiver", widget=forms.Textarea, required=False)
    sibling_class = forms.CharField(label="Class of other siblings currently living with caregiver", widget=forms.Textarea, required=False)
    sibling_ages = forms.CharField(label="Age(s) of other siblings currently living with caregiver", widget=forms.Textarea, required=False)
    relative_names = forms.CharField(label="Name(s) of other relatives", widget=forms.Textarea, required=False)
    relative_relationships = forms.CharField(label="Relationship to the child", widget=forms.Textarea, required=False)
    relative_last_known_locations = forms.CharField(label="Last known location(s) of other relatives",
                                                    widget=forms.Textarea, required=False)
    relative_phone_numbers = forms.CharField(label="Phone No.(s) of other relatives", widget=forms.Textarea,
                                             required=False)
    is_contact_with_family = forms.BooleanField(label="Is there any contact with family?", required=False)
    contact_person = forms.CharField(label="If yes, who", required=False)
    last_visit_date = forms.CharField(
        label="If yes, does the child remember the date (or how long ago) the last visit occurred?", required=False)
    goes_home_on_school_holidays = forms.BooleanField(label="Does child go home on school holidays?", required=False)
    family_visits = forms.BooleanField(label="Does family visit?", required=False)
    family_visit_details = forms.CharField(label="If yes, who, and how often do they visit?", widget=forms.Textarea,
                                           required=False)
    expresses_caregiver_preference = forms.BooleanField(label="Does the child express a preference of caregiver?",
                                                        required=False)
    #4.CHILD WELLBEING
    # a)HEALTH AND DEVELOPMENT
    is_growing_appropriately = forms.CharField(
        label="Is the child growing appropriately for their age? Describe physical skills and needs, intellectual skills and needs, social skills and needs",
        widget=forms.Textarea,
        required=False
    )
    medical_history = forms.CharField(
        label="Any history of medical issues/hospitalization? Frequency? Explain and attach records",
        widget=forms.Textarea,
        required=False
    )
    has_current_health_condition = forms.BooleanField(label="Any current health conditions?", required=False)
    current_health_condition = forms.CharField(label="Specify", required=False)
    has_chronic_health_condition = forms.BooleanField(label="Any chronic health conditions?", required=False)
    chronic_health_condition = forms.CharField(label="Specify", required=False)
    is_on_medication = forms.BooleanField(label="Currently on any medication?", required=False)
    medication_details = forms.CharField(label="If yes, specify", required=False)
    is_fully_immunized = forms.BooleanField(label="Has the child been fully immunized?", required=False)
    immunization_reason = forms.CharField(label="If no, what is the reason?", required=False)
    has_allergy = forms.BooleanField(label="Any allergy?", required=False)
    allergy_details = forms.CharField(label="If yes, specify", required=False, widget=forms.Textarea)
    feeding_routine = forms.CharField(label="Feeding routine and special needs", required=False, widget=forms.Textarea)
    # b) EDUCATION

    previously_attended_school = forms.BooleanField(label="Previously attended any school?", required=False)
    previous_school_type = forms.ChoiceField(label="If yes, type of school",
                                             choices=[("public", "Public"), ("private", "Private")], required=False)
    previous_school_name = forms.CharField(label="Name and location of school", required=False)

    currently_attending_school = forms.BooleanField(label="Child currently attending school?", required=False)
    current_school_type = forms.ChoiceField(label="If yes, type of school",
                                            choices=[("public", "Public"), ("private", "Private")], required=False)
    current_school_name = forms.CharField(label="Name and location of school", required=False)
    education_level = forms.CharField(label="Current education level", required=False)
    school_performance = forms.CharField(label="Attendance, performance, extra-curricular activity, and behaviour",
                                         required=False, widget=forms.Textarea)
    # c)PSYCHOSOCIAL AND EMOTIONAL WELLBEING
    friends = forms.CharField(label="Who are the child’s friends?", widget=forms.Textarea, required=False)
    activities_with_friends = forms.CharField(label="What kinds of things do they do together?", widget=forms.Textarea,
                                              required=False)
    interaction_frequency = forms.CharField(label="How often do they interact?", required=False)

    peer_friendship_views = forms.CharField(label="What are the child’s views of these peer friendships?",
                                            widget=forms.Textarea, required=False)
    friendship_quality = forms.ChoiceField(label="What is the quality of these friendships?",
                                           choices=[], required=False)
    age_dynamics = forms.ChoiceField(label="Are the perceived friends much older, younger, or same age?",
                                     choices=AGE_DYNAMICS, required=False)

    caregiver_attachment_level = forms.ChoiceField(label="Level of attachment between the child and current caregiver",
                                                   choices=LEVEL,
                                                   required=False)
    caregiver_relationship = forms.CharField(label="Describe the relationship with the current caregiver",
                                             widget=forms.Textarea, required=False)

    previous_caregiver_attachment_level = forms.ChoiceField(label="Level of attachment to previous primary caregiver",
                                                            choices=LEVEL, required=False)
    previous_caregiver_relationship = forms.CharField(
        label="Describe the relationship with the previous primary caregiver", widget=forms.Textarea, required=False)

    exhibited_behaviors = forms.MultipleChoiceField(label="Does the child exhibit any of the following?", choices=EXHIBITED_BEHAVIOR, widget=forms.CheckboxSelectMultiple, required=False)
    daily_routine = forms.CharField(label="Daily routine", widget=forms.Textarea, required=False)
    degree_of_independence = forms.CharField(label="Degree of independence", widget=forms.Textarea, required=False)

    likes = forms.CharField(label="Likes", widget=forms.Textarea, required=False)
    dislikes = forms.CharField(label="Dislikes", widget=forms.Textarea, required=False)
    fears = forms.CharField(label="Fears", widget=forms.Textarea, required=False)
    skills_strengths = forms.CharField(label="Skills / strengths", widget=forms.Textarea, required=False)

     # CHILD PERSPECTIBVE ON REINTERGRATION
    preference_reunification = forms.ChoiceField(label="Does the child express a preference for reunification/placement?", choices=YES_NO_NA_CHOICES)
    concerns_reunification = forms.ChoiceField(label="Does the child express concerns about reunification/placement?", choices=YES_NO_CHOICES)
    concerns_reunification_details = forms.CharField(label="If yes, please specify", widget=forms.Textarea, required=False)

    #Assesemnt CONCLUSION AND ACTION POINTS
    strengths_resources = forms.CharField(label="Strengths and resources", widget=forms.Textarea, required=False)
    needs_concerns = forms.CharField(label="Needs or concerns", widget=forms.Textarea, required=False)
    additional_observations = forms.CharField(label="Additional observations", widget=forms.Textarea, required=False)
    things_to_achieve = forms.CharField(label="Things to be achieved", widget=forms.Textarea, required=False)

    #SIGNATURE
    caseworker_name = forms.CharField(label="Caseworker's name", required=False)
    caseworker_signature = forms.CharField(label="Caseworker's signature", required=False)
    caseworker_date = forms.DateField(label="Caseworker's date", required=False)

    case_manager_name = forms.CharField(label="Case Manager's name", required=False)
    case_manager_signature = forms.CharField(label="Case Manager's signature", required=False)
    case_manager_date = forms.DateField(label="Case Manager's date", required=False)






