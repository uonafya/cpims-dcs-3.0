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

REASON_FOR_REFERRAL = (
    ("By court order", "By court order"),
    ("Supervision", "Supervision"),
    ("Others", "Others"),
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
    
class SIRemandHomeEscape(forms.Form):
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
   