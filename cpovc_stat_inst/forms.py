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

YES_NO_CHOICES = (('AYES', 'Yes'), ('ANNO', 'No'))


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
    ('1', 'Has no parent or guardian, or has been abandoned by his parent or guardian, or is destitute.'),
    ('2', 'Found begging or receiving alms and parents or guardians cannot be traced.'),
    ('3', 'The parent has been imprisoned and there are no alternative care options.'),
    ('4', 'Whose parent or guardian does not, or is unable or unfit to exercise proper care and guardianship and there is no alternative care option'),
    ('5', 'Who is prevented from receiving education and there are no proper interventions in place'),
    ('6', 'Who, being a female is subjected or is likely to be subjected tofemale circumcision or early  marriage or customs and practices prejudicial to the childs life, education, and health'),
    ('7', 'Who is being kept in any premises which, in the opinion of a medical officer, are overcrowded,  unsanitary or dangerous;'),
    ('8', 'Who is exposed to domestic violence'),
    ('9', 'Who is pregnant and living within the same household as the perpetrator who committed the offence'),
    ('10', 'Whose parent is terminally ill with no access to alternative care'),
    ('11', 'Who is disabled and is being unlawfully confined or ill-treated'),
    ('12', 'Who has been sexually abused or is likely to be exposed to sexual abuse and exploitation including prostitution and pornography'),
    ('13', 'Who is engaged in any work likely to harm his health, education, mental or moral development'),
    ('14', 'Who is displaced as a consequence of war, civil disturbances or natural disasters')
)

NEED_RISK_SCALE = (
    ('Area-1', 'Area 1 - Prior or Current Offences/Dispositions'),
    ('Area-2', 'Area 2 - Family Circumstances/Parenting'),
    ('Area-3', 'Area 3 - Education/Employment'),
    ('Area-4', 'Area 4 - Peer Relations'),
    ('Area-5', 'Area 5 - Substance Abuse'),
    ('Area-6', 'Area 6 - Leisure/Recreation'),
    ('Area-7', 'Area 7 - Street Experience'),
    ('Area-8', 'Area 8 - Personality/Behaviour'),
    ('Area-9', 'Area 9 - Attitudes/Orientation'),
)


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
        ),)
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
                "data-parsley-required": "true",
                "data-parsley-group": "group0",
            }
        )
    )
    date_of_admission = forms.DateField(
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Date Of Admission"),
                "class": "form-control",
                "id": "admission_date",
                "data-parsley-required": "true",
                "data-parsley-group": "group0",
            }
        )
    )
    current_year_of_school = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Year of sschool"),
                "class": "form-control",
                "id": "current_year_of_school",
                "data-parsley-required": "true",
                "data-parsley-group": "group0",
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
                'row': "1"
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
                "class": "form-control",
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
        )
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
        )
        
    )

    workforce_id = forms.IntegerField(
        required=False, widget=forms.TextInput(
            attrs={'placeholder': _('Workforce ID'),
                   'class': 'form-control',
                   'id': 'workforce_id'}))
    audit_date = forms.DateField(
        required=False, widget=forms.DateInput(
            attrs={'class': 'form-control',
                   'data-parsley-required': 'true',
                   'id': 'audit_date'}))





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
                "data-parsley-required": "true",
                "data-parsley-group": "group0",
            }
        )
    )
    workforce_id = forms.IntegerField(
        required=False, widget=forms.TextInput(
            attrs={'placeholder': _('Workforce ID'),
                   'class': 'form-control',
                   'id': 'workforce_id'}))
    audit_date = forms.DateField(
        required=False, widget=forms.DateInput(
            attrs={'class': 'form-control',
                   'data-parsley-required': 'true',
                   'id': 'audit_date'}))
    


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
    needrisk_list = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'hidden',
               'id': 'needrisk_list'}))


class SIVacancyApp(forms.Form):
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

class SIVacancyConfirm(forms.Form):
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