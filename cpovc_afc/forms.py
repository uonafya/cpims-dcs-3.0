from django import forms
from django.forms.widgets import RadioSelect

from django.utils.translation import gettext_lazy as _

from cpovc_main.functions import get_list, get_lists
immunization_list = get_list('immunization_status_id', 'Please Select')

person_type_list = get_list('person_type_id', 'Please Select Type')
school_level_list = get_list('school_level_id', 'Please Select Level')
admission_list = get_list('school_type_id', 'Please Select one')
disability_list = get_list('disability_type_id', 'Please Select one')
severity_list = get_list('severity_level_id', 'Please Select one')
admission_type_list = get_list('admission_type_id', 'Please Select')
admission_reason_list = get_list('care_admission_reason_id')
domain_list = get_list('afc_domain_id', 'Please Select')
list_sex_id = get_list('sex_id')
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


class RadioCustomRenderer(RadioSelect):
    """Custom radio button renderer class."""

    def render(self):
        """Renderer override method."""
        pass


class AltCareForm(forms.Form):
    """AFC form."""

    has_consent = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'has_consent',
                   'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#has_consent_error"}))

    care_option = forms.ChoiceField(
        choices=care_option_list,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control', 'id': 'care_option',
                   'data-parsley-required': "true"}))

    care_sub_option = forms.ChoiceField(
        choices=(('', 'Please Select'), ),
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control', 'id': 'care_sub_option',
                   'data-parsley-required': "false"}))

    case_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Care initiation Date'),
               'class': 'form-control',
               'id': 'case_date',
               'data-parsley-required': "true"
               }))

    event_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date'),
               'class': 'form-control',
               'id': 'event_date',
               'data-parsley-required': "true"
               }))

    AFC_FM_msc = forms.MultipleChoiceField(
        choices=admission_reason_list,
        widget=forms.CheckboxSelectMultiple(
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#id_qf1A1"}))

    qf3A1_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qf3A1_rdo',
                   'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf3A1_rdo_error"}))

    qf3A2_sdd = forms.ChoiceField(
        choices=consent_forms_list,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control', 'id': 'care_option',
                   'data-parsley-required': "true"}))

    qf3B1_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qf3B1_rdo',
                   'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf3B1_rdo_error"}))


class AFCForm1A(forms.Form):
    """AFC Form 1A."""

    event_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date'),
               'class': 'form-control',
               'id': 'event_date',
               'data-parsley-required': "true"
               }))

    qf1A1_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'has_bcert',
                   'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf1A1_rdo_error"}))

    qf1A2 = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': _(''),
               'class': 'form-control', 'id': 'qf1A2',
               'data-parsley-required': "false"}))

    qf1A3 = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': _(''),
               'class': 'form-control', 'id': 'qf1A3',
               'data-parsley-required': "false"}))

    qf1A4 = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': _(''),
               'class': 'form-control', 'id': 'qf1A4',
               'data-parsley-required': "false"}))

    qf1A5 = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': _(''),
               'class': 'form-control', 'id': 'qf1A5',
               'data-parsley-required': "false"}))

    qf1A6 = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': _(''),
               'class': 'form-control', 'id': 'qf1A6',
               'data-parsley-required': "false"}))

    qf1A7 = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': _(''),
               'class': 'form-control', 'id': 'qf1A7',
               'data-parsley-required': "false"}))

    qf1A8 = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': _(''),
               'class': 'form-control', 'id': 'qf1A8',
               'data-parsley-required': "false"}))

    qf1A10_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'has_disability',
                   'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf1A2_rdo_error"}))

    qf1A11_sdd = forms.ChoiceField(
        choices=disability_list,
        initial='0',
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'disability_type'}))

    qf1A12_sdd = forms.ChoiceField(
        choices=severity_list,
        initial='0',
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'disability_severity'}))

    qf1A13 = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': _(''),
               'class': 'form-control', 'id': 'qf1A13',
               'data-parsley-required': "false"}))

    qf1A14_sdd = forms.ChoiceField(
        choices=list_other_adms,
        initial='0',
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'qf1A14_sdd'}))

    qf1A15_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf1A15_rdo_error"}))

    qf1A16 = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': _(''),
               'class': 'form-control',
               'data-parsley-required': "false"}))

    qf1A17 = forms.DateField(required=False, widget=forms.TextInput(
        attrs={'placeholder': _(''),
               'class': 'form-control event_date',
               'data-parsley-required': "false"}))

    qf1A18 = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': _(''),
               'class': 'form-control',
               'data-parsley-required': "false"}))

    qf1A19 = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': _(''),
               'class': 'form-control',
               'data-parsley-required': "false"}))

    qf1A20_sdd = forms.ChoiceField(
        choices=list_other_vulnerability,
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control'}))

    qf1A21 = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': _(''),
               'class': 'form-control',
               'data-parsley-required': "false"}))

    qf1A21A_sdd = forms.ChoiceField(
        choices=list_relationship,
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control'}))

    qf1A22_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf1A22_rdo_error"}))

    qf1A23_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf1A23_rdo_error"}))

    qf1A24_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf1A24_rdo_error"}))

    qf1A25_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'false',
                   'data-parsley-errors-container': "#qf1A25_rdo_error"}))

    qf1A25A = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': _(''),
               'class': 'form-control',
               'data-parsley-required': "false"}))

    qf1A25B = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': _(''),
               'class': 'form-control',
               'data-parsley-required': "false"}))

    qf1A26_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'false',
                   'data-parsley-errors-container': "#qf1A26_rdo_error"}))

    qf1A27_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'false',
                   'data-parsley-errors-container': "#qf1A27_rdo_error"}))

    qf1A27A = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': _(''),
               'class': 'form-control',
               'data-parsley-required': "false"}))

    qf1A28_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf1A28_rdo_error"}))


class AFCForm1B(forms.Form):
    """AFC Form 1B."""

    event_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date'),
               'class': 'form-control',
               'id': 'event_date',
               'data-parsley-required': "true"
               }))

    qf1B1A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf1B1A_rdo_error"}))

    qf1B1B = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Details'),
               'class': 'form-control', 'rows': '2'}))

    qf1B2A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf1B2A_rdo_error"}))

    qf1B2B = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Details'),
               'class': 'form-control', 'rows': '2'}))

    qf1B2C_rdo = forms.ChoiceField(
        choices=list_frequency,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf1B2C_rdo_error"}))

    qf1B3A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf1B3A_rdo_error"}))

    qf1B3B = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Details'),
               'class': 'form-control', 'rows': '2'}))

    qf1B4A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf1B4A_rdo_error"}))

    qf1B4B = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Details'),
               'class': 'form-control', 'rows': '2'}))

    qf1B5A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf1B5A_rdo_error"}))

    qf1B5B = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Details'),
               'class': 'form-control', 'rows': '2'}))

    qf1B6A_sdd = forms.ChoiceField(
        choices=immunization_list,
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': "true",
                   'id': 'immunization'}))

    qf1B6B = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('If not fully, reason'),
               'class': 'form-control', 'rows': '2'}))

    qf1B7A_rdo = forms.ChoiceField(
        choices=YESNO_UK_CHOICES,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf1B7A_rdo_error"}))

    qf1B7B = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Details'),
               'class': 'form-control', 'rows': '2'}))

    qf1B8 = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Details'),
               'class': 'form-control', 'rows': '2'}))

    # School details

    qf1B9A_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf1B9A_rdo_error"}))

    qf1B9B = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('If yes, name'),
               'class': 'form-control', 'rows': '2'}))

    school_level = forms.ChoiceField(
        choices=school_level_list,
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': "true",
                   'id': 'school_level'}))

    school_name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Start typing then select',
               'id': 'school_name'}))

    school = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'readonly': 'readonly',
               'data-parsley-required': "true",
               'id': 'school_id'}))

    admission_type = forms.ChoiceField(
        choices=admission_list,
        initial='0',
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'admission_type'}))

    school_class = forms.ChoiceField(
        choices=(),
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'school_class'}))

    qf1B10_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf1B10_rdo_error"}))

    qf1B11_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf1B11_rdo_error"}))

    qf1B12_rdo = forms.ChoiceField(
        choices=list_education_perf,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf1B12_rdo_error"}))

    qf1B13 = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Other details'),
               'class': 'form-control', 'rows': '2'}))

    # PSS

    qf1B14A = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Details'),
               'class': 'form-control', 'rows': '2'}))

    qf1B14B = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Details'),
               'class': 'form-control', 'rows': '2'}))

    qf1B14C = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Details'),
               'class': 'form-control', 'rows': '2'}))

    qf1B15 = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Details'),
               'class': 'form-control', 'rows': '2'}))

    qf1B16 = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Details'),
               'class': 'form-control', 'rows': '2'}))

    qf1B17 = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Details'),
               'class': 'form-control', 'rows': '2'}))

    qf1B18A_rdo = forms.ChoiceField(
        choices=list_range_level_rdo,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf1B18A_rdo_error"}))

    qf1B18B = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Describe'),
               'class': 'form-control', 'rows': '2'}))

    qf1B19A_rdo = forms.ChoiceField(
        choices=list_range_level_rdo,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf1B19A_rdo_error"}))

    qf1B19B = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Describe'),
               'class': 'form-control', 'rows': '2'}))

    qf1B20_msc = forms.MultipleChoiceField(
        choices=list_child_exhibits,
        required=False,
        widget=forms.CheckboxSelectMultiple(
            attrs={'data-parsley-required': 'false'}))

    qf1B21 = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Describe'),
               'class': 'form-control', 'rows': '2'}))

    qf1B22_rdo = forms.ChoiceField(
        choices=list_range_level_rdo,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'false',
                   'data-parsley-errors-container': "#qf1B22_rdo_error"}))

    qf1B23 = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Describe'),
               'class': 'form-control', 'rows': '2'}))

    qf1B24 = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Describe'),
               'class': 'form-control', 'rows': '2'}))

    qf1B25 = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Describe'),
               'class': 'form-control', 'rows': '2'}))

    qf1B26 = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Describe'),
               'class': 'form-control', 'rows': '2'}))

    # Child perspective
    qf1B27A_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf1B27A_rdo_error"}))

    qf1B28A_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf1B28A_rdo_error"}))

    qf1B28B = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('If yes, explain'),
               'class': 'form-control', 'rows': '2'}))

    # Assessment conclusions

    qf1B30 = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Details'),
               'class': 'form-control', 'rows': '2'}))

    qf1B31 = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Details'),
               'class': 'form-control', 'rows': '2'}))

    qf1B32 = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Details'),
               'class': 'form-control', 'rows': '2'}))

    qf1B33 = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Details'),
               'class': 'form-control', 'rows': '2'}))


class AFCForm2A(forms.Form):
    """AFC Form 2A."""

    event_date = forms.DateField(
        widget=forms.TextInput(
            attrs={'placeholder': _('Date'),
                   'class': 'form-control',
                   'id': 'event_date',
                   'data-parsley-required': "true"
                   }))

    qf2A1 = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))

    qf2A2_sdd = forms.ChoiceField(
        choices=list_marriage_type,
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': "true"}))

    qf2A3 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _('Details'),
                   'class': 'form-control', 'rows': '2'}))

    qf2A4 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _('Details'),
                   'class': 'form-control', 'rows': '2'}))

    qf2A5_sdd = forms.ChoiceField(
        choices=list_items_count,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': "true"}))

    qf2A6_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf2A6_rdo_error"}))

    qf2A7 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _('Details'),
                   'class': 'form-control', 'rows': '2'}))

    qf2A8 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _('Details'),
                   'class': 'form-control', 'rows': '2'}))

    qf2A9 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _('Details'),
                   'class': 'form-control', 'rows': '2'}))

    qf2A10 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _('Details'),
                   'class': 'form-control', 'rows': '2'}))

    qf2A11 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _('Details'),
                   'class': 'form-control', 'rows': '2'}))

    qf2A12 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _('Details'),
                   'class': 'form-control', 'rows': '2'}))

    qf2A13 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _('Details'),
                   'class': 'form-control', 'rows': '2'}))

    qf2A14_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf2A14_rdo_error"}))

    qf2A15_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf2A15_rdo_error"}))

    qf2A16A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf2A16A_rdo_error"}))

    qf2A16B = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _('If yes, who, and what type'),
                   'class': 'form-control', 'rows': '2'}))

    qf2A17A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf2A17A_rdo_error"}))

    qf2A17B = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'How many'}))

    qf2A18A1_rdo = forms.ChoiceField(
        choices=list_disability_assessment,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'false',
                   'data-parsley-errors-container': "#qf2A18A1_rdo_error"}))

    qf2A18A2_rdo = forms.ChoiceField(
        choices=list_disability_assessment,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'false',
                   'data-parsley-errors-container': "#qf2A18A2_rdo_error"}))

    qf2A18A3_rdo = forms.ChoiceField(
        choices=list_disability_assessment,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'false',
                   'data-parsley-errors-container': "#qf2A18A3_rdo_error"}))

    qf2A18A4_rdo = forms.ChoiceField(
        choices=list_disability_assessment,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'false',
                   'data-parsley-errors-container': "#qf2A18A4_rdo_error"}))

    qf2A18A5_rdo = forms.ChoiceField(
        choices=list_disability_assessment,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'false',
                   'data-parsley-errors-container': "#qf2A18A5_rdo_error"}))

    qf2A18A6_rdo = forms.ChoiceField(
        choices=list_disability_assessment,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'false',
                   'data-parsley-errors-container': "#qf2A18A6_rdo_error"}))

    qf2A18A7_rdo = forms.ChoiceField(
        choices=list_disability_handling,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'false',
                   'data-parsley-errors-container': "#qf2A18A7_rdo_error"}))

    qf2A18A8_msc = forms.MultipleChoiceField(
        required=False,
        choices=list_special_support,
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': ''}))

    qf2A18B = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _('Other, details'),
                   'class': 'form-control', 'rows': '2'}))

    qf2A19A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf2A19A_rdo_error"}))

    qf2A19B = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _('Explain'),
                   'class': 'form-control', 'rows': '2'}))

    qf2A20_msc = forms.MultipleChoiceField(
        choices=list_community_services,
        required=False,
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': ''}))

    qf2A21_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf2A21_rdo_error"}))

    qf2A22_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf2A22_rdo_error"}))

    qf2A23A = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))

    qf2A23B = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))

    qf2A23C = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))

    qf2A23D = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))

    qf2A24_sdd = forms.ChoiceField(
        choices=list_school_category,
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control'}))

    qf2A25A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf2A25A_rdo_error"}))

    qf2A25B = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("If no, describe child's unmet needs"),
                   'class': 'form-control', 'rows': '2'}))

    qf2A26A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf2A26A_rdo_error"}))

    qf2A26B_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'false',
                   'data-parsley-errors-container': "#qf2A26B_rdo_error"}))

    qf2A27_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf2A27_rdo_error"}))

    qf2A28 = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={'placeholder': _("Economic activity"),
                   'data-parsley-required': 'true',
                   'class': 'form-control', 'rows': '2'}))

    qf2A29_sdd = forms.ChoiceField(
        choices=list_employment_type,
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control', 'data-parsley-required': 'true'}))

    qf2A30_sdd = forms.ChoiceField(
        choices=list_income_range,
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control', 'data-parsley-required': 'true'}))

    qf2A31A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf2A31A_rdo_error",
                   'data-parsley-required': 'true'}))

    qf2A31B = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("If yes, by whom"),
                   'class': 'form-control', 'rows': '2'}))

    qf2A32 = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={'placeholder': _("Assets"),
                   'data-parsley-required': 'true',
                   'class': 'form-control', 'rows': '2'}))

    qf2A33A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf2A33A_rdo_error"}))

    qf2A33B = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Please describe"),
                   'class': 'form-control', 'rows': '2'}))

    qf2A34_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf2A34_rdo_error"}))

    qf2A35A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf2A35A_rdo_error"}))

    qf2A35B = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Please describe"),
                   'class': 'form-control', 'rows': '2'}))

    qf2A36_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf2A36_rdo_error"}))

    qf2A37 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Please describe"),
                   'class': 'form-control', 'rows': '2'}))

    qf2A38A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf2A38A_rdo_error"}))

    qf2A38B_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf2A38B_rdo_error"}))

    qf2A39_sdd = forms.ChoiceField(
        choices=list_attachment_assessment,
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control', 'data-parsley-required': 'true'}))

    qf2A39A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf2A39A_rdo_error"}))

    qf2A39B = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Describe"),
                   'class': 'form-control', 'rows': '2'}))

    qf2A40A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf2A40A_rdo_error"}))

    qf2A40B = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Describe"),
                   'class': 'form-control', 'rows': '2'}))

    qf2A41A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf2A41A_rdo_error"}))

    qf2A41B = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Describe both +ve and -ve events"),
                   'class': 'form-control', 'rows': '2'}))

    qf2A42 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Describe"),
                   'class': 'form-control', 'rows': '2'}))

    qf2A43_rdo = forms.ChoiceField(
        choices=list_ratings,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf2A43A_rdo_error"}))

    qf2A44_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf2A44_rdo_error"}))

    qf2A45_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf2A45_rdo_error"}))

    qf2A46 = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={'placeholder': _("Describe"),
                   'data-parsley-required': 'true',
                   'class': 'form-control', 'rows': '2'}))

    qf2A47_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf2A47_rdo_error"}))

    qf2A48 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Describe"),
                   'class': 'form-control', 'rows': '2'}))

    qf2A49A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf2A49A_rdo_error"}))

    qf2A49B = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Describe"),
                   'class': 'form-control', 'rows': '2'}))

    qf2A50 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Describe"),
                   'class': 'form-control', 'rows': '2'}))

    qf2A51_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf2A51_rdo_error"}))

    qf2A52_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf2A52_rdo_error"}))

    qf2A53_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf2A53_rdo_error"}))

    qf2A54A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf2A54A_rdo_error"}))

    qf2A54B = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Examples"),
                   'class': 'form-control', 'rows': '2'}))

    qf2A55_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf2A55_rdo_error"}))

    qf2A56 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Describe"),
                   'class': 'form-control', 'rows': '2'}))

    qf2A57 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Describe"),
                   'class': 'form-control', 'rows': '2'}))

    qf2A58 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Describe"),
                   'class': 'form-control', 'rows': '2'}))

    qf2A59_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf2A59_rdo_error"}))

    qf2A60_rdo = forms.ChoiceField(
        choices=YESNO_UN_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf2A60_rdo_error"}))

    qf2A61 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Describe"),
                   'class': 'form-control', 'rows': '3'}))

    qf2A62 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Describe"),
                   'class': 'form-control', 'rows': '3'}))

    qf2A63 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Describe"),
                   'class': 'form-control', 'rows': '3'}))

    qf2A64_sdd = forms.ChoiceField(
        choices=list_range_level,
        required=True,
        widget=forms.Select(
            attrs={'data-parsley-required': 'true',
                   'class': 'form-control'}))

    qf2A65_sdd = forms.ChoiceField(
        choices=list_family_types,
        required=True,
        widget=forms.Select(
            attrs={'data-parsley-required': 'true',
                   'class': 'form-control'}))


class AFCForm4A(forms.Form):
    """AFC Form 4A."""

    event_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date'),
               'class': 'form-control',
               'id': 'event_date',
               'data-parsley-required': "true"
               }))

    qf4A1_sdd = forms.ChoiceField(
        choices=domain_list,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control', 'id': 'qf4A1',
                   'data-parsley-required': "true"}))

    qf4A2_sdd = forms.ChoiceField(
        choices=(),
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control', 'id': 'qf4A2',
                   'data-parsley-required': "true"}))

    qf4A3_sdd = forms.ChoiceField(
        choices=(),
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control', 'id': 'qf4A3',
                   'data-parsley-required': "true"}))

    qf4A4_sdd = forms.ChoiceField(
        choices=(),
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control', 'id': 'qf4A4',
                   'data-parsley-required': "true"}))

    qf4A5 = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Date'),
               'class': 'form-control other_date',
               'data-parsley-required': "true"
               }))

    qf4A6_sdd = forms.ChoiceField(
        choices=list_case_plan_responsible,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control', 'id': 'qf4A6',
                   'data-parsley-required': "true"}))

    qf4A7_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qf4A1_rdo',
                   'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf4A7_rdo_error"}))

    qf4A8 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Explain"),
                   'class': 'form-control', 'rows': '2'}))

    qf4A9 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Explain"),
                   'class': 'form-control', 'rows': '2'}))


class AFCForm5A(forms.Form):
    """AFC Form 5A."""

    def __init__(self, care_type, *args, **kwargs):
        """Override method especially for dynamic lookup data."""
        self.care_type = care_type
        super(AFCForm5A, self).__init__(*args, **kwargs)

        if self.care_type == 'IL':
            adm_reason_list = get_list('sil_placement_reason_id')
        else:
            adm_reason_list = get_list('care_admission_reason_id')

        qf5A17 = forms.MultipleChoiceField(
            required=True,
            choices=adm_reason_list,
            widget=forms.CheckboxSelectMultiple(
                attrs={'data-parsley-required': 'true',
                       'data-parsley-errors-container': "#qf5A17_error"}))

        self.fields['qf5A17_msc'] = qf5A17

    event_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date'),
               'class': 'form-control',
               'id': 'event_date',
               'data-parsley-required': "true"
               }))

    qf5A1 = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': _(''),
                   'class': 'form-control',
                   'data-parsley-required': "false"
                   }))

    qf5A2 = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': _(''),
                   'class': 'form-control',
                   'data-parsley-required': "false"
                   }))

    qf5A3_sdd = forms.ChoiceField(
        choices=(),
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control'}))

    qf5A3_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qf5A1_rdo',
                   'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf5A3_rdo_error"}))

    qf5A4_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qf5A1_rdo',
                   'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf5A4_rdo_error"}))

    qf5A5_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf5A5_rdo_error"}))

    qf5A6 = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control other_date',
                   'data-parsley-required': "false"
                   }))

    qf5A7 = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control other_date',
                   'data-parsley-required': "false"
                   }))

    qf5A8A = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))

    qf5A8B = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))

    qf5A8C = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))

    qf5A8D = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))

    qf5A9A = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))

    qf5A9B = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))

    qf5A9C = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))

    qf5A9D = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))

    qf5A10A = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))

    qf5A10B = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))

    qf5A10C = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))

    qf5A10D = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))

    qf5A11A = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))

    qf5A11B = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))

    qf5A11C = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))

    qf5A11D = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))

    qf5A12A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf5A12A_rdo_error"}))

    qf5A12B = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))

    qf5A12C = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))

    qf5A13_sdd = forms.ChoiceField(
        choices=care_option_list,
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control'}))

    qf5A14_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'class': 'form-control',
                   'data-parsley-errors-container': "#qf5A14_rdo_error"}))

    qf5A15A = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))

    qf5A15B_sdd = forms.ChoiceField(
        choices=list_sex_other_id,
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control'}))

    qf5A15C = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))

    qf5A16 = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))


class AFCForm6A(forms.Form):
    """AFC Form 6A."""

    event_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date'),
               'class': 'form-control',
               'id': 'event_date',
               'data-parsley-required': "true"
               }))

    qf6A1 = forms.CharField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control', 'min': '1',
                   'data-parsley-required': "true"}))

    qf6A2 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Details"),
                   'class': 'form-control', 'rows': '2'}))

    qf6A3 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Details"),
                   'class': 'form-control', 'rows': '2'}))

    qf6A4 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Details"),
                   'class': 'form-control', 'rows': '2'}))

    qf6A5 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Details"),
                   'class': 'form-control', 'rows': '2'}))

    qf6A6 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Details"),
                   'class': 'form-control', 'rows': '2'}))

    qf6A7 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Details"),
                   'class': 'form-control', 'rows': '2'}))

    qf6A8 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Details"),
                   'class': 'form-control', 'rows': '2'}))

    qf6A9 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Details"),
                   'class': 'form-control', 'rows': '2'}))

    qf6A10 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Details"),
                   'class': 'form-control', 'rows': '2'}))

    qf6A11 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Details"),
                   'class': 'form-control', 'rows': '2'}))

    qf6A12 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Details"),
                   'class': 'form-control', 'rows': '2'}))

    qf6A13 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Details"),
                   'class': 'form-control', 'rows': '2'}))

    qf6A14 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Details"),
                   'class': 'form-control', 'rows': '2'}))
    qf6A15 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Details"),
                   'class': 'form-control', 'rows': '2'}))

    qf6A16 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Details"),
                   'class': 'form-control', 'rows': '2'}))

    qf6A17 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Details"),
                   'class': 'form-control', 'rows': '2'}))

    qf6A18 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Details"),
                   'class': 'form-control', 'rows': '2'}))

    qf6A19 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Details"),
                   'class': 'form-control', 'rows': '2'}))

    qf6A20 = forms.DateField(
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': _('Date'),
                   'data-parsley-required': "true",
                   'class': 'form-control other_date'}))


class AFCForm7A(forms.Form):
    """AFC Form 7A."""

    event_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date'),
               'class': 'form-control',
               'id': 'event_date',
               'data-parsley-required': "true"
               }))

    qf7A11_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A11_rdo_error"}))

    qf7A12_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A12_rdo_error"}))

    qf7A13_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A13_rdo_error"}))

    qf7A14_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A14_rdo_error"}))

    qf7A15_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A15_rdo_error"}))

    qf7A16_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A16_rdo_error"}))

    qf7A17_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A17_rdo_error"}))

    qf7A21_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A21_rdo_error"}))

    qf7A22_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A22_rdo_error"}))

    qf7A23_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A23_rdo_error"}))

    qf7A24_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A24_rdo_error"}))

    qf7A31_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A31_rdo_error"}))

    qf7A32_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A32_rdo_error"}))

    qf7A33_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A33_rdo_error"}))

    qf7A34_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A34_rdo_error"}))

    qf7A35_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A35_rdo_error"}))

    qf7A36_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A36_rdo_error"}))

    qf7A37_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A37_rdo_error"}))

    qf7A38_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A38_rdo_error"}))

    qf7A41_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A41_rdo_error"}))

    qf7A42_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A42_rdo_error"}))

    qf7A43_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A43_rdo_error"}))

    qf7A44_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A44_rdo_error"}))

    qf7A45_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A45_rdo_error"}))

    qf7A46_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A46_rdo_error"}))

    qf7A51_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A51_rdo_error"}))

    qf7A52_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A52_rdo_error"}))

    qf7A53_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A53_rdo_error"}))

    qf7A54_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A54_rdo_error"}))

    qf7A55_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A55_rdo_error"}))

    qf7A61_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A61_rdo_error"}))

    qf7A62_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A62_rdo_error"}))

    qf7A63_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A63_rdo_error"}))

    qf7A64_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A64_rdo_error"}))

    qf7A65_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A65_rdo_error"}))

    qf7A71_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A71_rdo_error"}))

    qf7A72_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A72_rdo_error"}))

    qf7A81_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A81_rdo_error"}))

    qf7A82_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A82_rdo_error"}))

    qf7A83_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A83_rdo_error"}))

    qf7A84_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A84_rdo_error"}))

    qf7A91_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A91_rdo_error"}))

    qf7A92_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A92_rdo_error"}))

    qf7A93_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A93_rdo_error"}))

    qf7A94_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A94_rdo_error"}))

    qf7A95_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A95_rdo_error"}))

    qf7A101_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A101_rdo_error"}))

    qf7A102_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A102_rdo_error"}))

    qf7A103_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A103_rdo_error"}))

    qf7A104_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A104_rdo_error"}))

    qf7A105_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A105_rdo_error"}))

    qf7A111_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A111_rdo_error"}))

    qf7A112_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A112_rdo_error"}))

    qf7A113_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A113_rdo_error"}))

    qf7A114_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A114_rdo_error"}))

    qf7A115_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A115_rdo_error"}))

    qf7A116_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A116_rdo_error"}))

    qf7A117_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A117_rdo_error"}))

    qf7A121_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A121_rdo_error"}))

    qf7A122_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A122_rdo_error"}))

    qf7A123_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A123_rdo_error"}))

    qf7A124_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A124_rdo_error"}))

    qf7A125_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A125_rdo_error"}))

    qf7A126_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A126_rdo_error"}))

    qf7A127_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf7A127_rdo_error"}))


class AFCForm8A(forms.Form):
    """AFC Form 8A."""

    event_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date'),
               'class': 'form-control',
               'id': 'event_date',
               'data-parsley-required': "true"
               }))

    qf8A11_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A11_rdo_error"}))

    qf8A12_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A12_rdo_error"}))

    qf8A13_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A13_rdo_error"}))

    qf8A14_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A14_rdo_error"}))

    qf8A15_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A15_rdo_error"}))

    qf8A16_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A16_rdo_error"}))

    qf8A17_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A17_rdo_error"}))

    qf8A21_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A21_rdo_error"}))

    qf8A22_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A22_rdo_error"}))

    qf8A23_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A23_rdo_error"}))

    qf8A24_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A24_rdo_error"}))

    qf8A31_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A31_rdo_error"}))

    qf8A32_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A32_rdo_error"}))

    qf8A33_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A33_rdo_error"}))

    qf8A34_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A34_rdo_error"}))

    qf8A35_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A35_rdo_error"}))

    qf8A36_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A36_rdo_error"}))

    qf8A41_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A41_rdo_error"}))

    qf8A42_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A42_rdo_error"}))

    qf8A43_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A43_rdo_error"}))

    qf8A44_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A44_rdo_error"}))

    qf8A45_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A45_rdo_error"}))

    qf8A51_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A51_rdo_error"}))

    qf8A52_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A52_rdo_error"}))

    qf8A53_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A53_rdo_error"}))

    qf8A54_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A54_rdo_error"}))

    qf8A55_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A55_rdo_error"}))

    qf8A61_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A61_rdo_error"}))

    qf8A62_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A62_rdo_error"}))

    qf8A63_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A63_rdo_error"}))

    qf8A64_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A64_rdo_error"}))

    qf8A71_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A71_rdo_error"}))

    qf8A81_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A81_rdo_error"}))

    qf8A82_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A82_rdo_error"}))

    qf8A91_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A91_rdo_error"}))

    qf8A92_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A92_rdo_error"}))

    qf8A101_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A101_rdo_error"}))

    qf8A102_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A102_rdo_error"}))

    qf8A111_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A111_rdo_error"}))

    qf8A112_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A112_rdo_error"}))

    qf8A113_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A113_rdo_error"}))

    qf8A114_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A114_rdo_error"}))

    qf8A121_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A121_rdo_error"}))

    qf8A122_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A122_rdo_error"}))

    qf8A123_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A123_rdo_error"}))

    qf8A124_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A124_rdo_error"}))

    qf8A125_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A125_rdo_error"}))

    qf8A126_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A126_rdo_error"}))

    qf8A127_rdo = forms.ChoiceField(
        choices=YESNONA_choices,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf8A127_rdo_error"}))


class AFCForm9A(forms.Form):
    """AFC Form 9A."""

    event_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date'),
               'class': 'form-control',
               'id': 'event_date',
               'data-parsley-required': "true"
               }))

    qf9AA_sdd = forms.ChoiceField(
        choices=list_closure_reasons,
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': "true"}))

    qf9AB1_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': "true",
                   'data-parsley-errors-container': "#qf9AB1_rdo_error"}))

    qf9AC1_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': "true",
                   'data-parsley-errors-container': "#qf9AC1_rdo_error"}))

    qf9AB2_rdo = forms.ChoiceField(
        choices=list_satisfied_level,
        required=False,
        widget=forms.RadioSelect(
            attrs={'data-parsley-errors-container': "#qf9AB2_rdo_error"}))

    qf9AC2_rdo = forms.ChoiceField(
        choices=list_satisfied_level,
        required=False,
        widget=forms.RadioSelect(
            attrs={'data-parsley-errors-container': "#qf9AC2_rdo_error"}))

    qf9A1A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': "true",
                   'data-parsley-errors-container': "#qf9A1A_rdo_error"}))

    qf9A1B = forms.DateField(required=False, widget=forms.TextInput(
        attrs={'placeholder': _('Date'),
               'class': 'form-control event_date'
               }))

    qf9A2A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': "true",
                   'data-parsley-errors-container': "#qf9A2A_rdo_error"}))

    qf9A2B = forms.DateField(required=False, widget=forms.TextInput(
        attrs={'placeholder': _('Date'),
               'class': 'form-control event_date'
               }))

    qf9A3A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': "true",
                   'data-parsley-errors-container': "#qf9A3A_rdo_error"}))

    qf9A3B = forms.DateField(required=False, widget=forms.TextInput(
        attrs={'placeholder': _('Date'),
               'class': 'form-control event_date'
               }))

    qf9A4A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': "true",
                   'data-parsley-errors-container': "#qf9A4A_rdo_error"}))

    qf9A4B = forms.DateField(required=False, widget=forms.TextInput(
        attrs={'placeholder': _('Date'),
               'class': 'form-control event_date'
               }))

    qf9A5A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': "true",
                   'data-parsley-errors-container': "#qf9A5A_rdo_error"}))

    qf9A5B = forms.DateField(required=False, widget=forms.TextInput(
        attrs={'placeholder': _('Date'),
               'class': 'form-control event_date'
               }))
    qf9A6A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-required': "true",
                   'data-parsley-errors-container': "#qf9A6A_rdo_error"}))

    qf9A6B = forms.DateField(required=False, widget=forms.TextInput(
        attrs={'placeholder': _('Date'),
               'class': 'form-control event_date'
               }))


class AFCForm10A(forms.Form):
    """AFC Form 10A."""

    event_date = forms.DateField(
        widget=forms.TextInput(
            attrs={'placeholder': _('Date'),
                   'class': 'form-control',
                   'id': 'event_date',
                   'data-parsley-required': "true"
                   }))

    qf10A1A_sdd = forms.ChoiceField(
        choices=list_case_transfer_ids,
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': "true"}))

    qf10A1B = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Describe"),
                   'class': 'form-control', 'rows': '3'}))

    qf10A2 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Describe"),
                   'class': 'form-control', 'rows': '3'}))

    qf10A3 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Describe"),
                   'class': 'form-control', 'rows': '3'}))

    qf10A4 = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))

    qf10A5 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Describe"),
                   'class': 'form-control', 'rows': '3'}))

    qf10A6 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Describe"),
                   'class': 'form-control', 'rows': '3'}))

    qf10A7 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Details"),
                   'class': 'form-control', 'rows': '3'}))

    qf10A8 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Details"),
                   'class': 'form-control', 'rows': '3'}))

    qf10A9 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Describe"),
                   'class': 'form-control', 'rows': '3'}))

    qf10A10 = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))


class AFCForm12A(forms.Form):
    """AFC Form 12A."""

    event_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date'),
               'class': 'form-control',
               'id': 'event_date',
               'data-parsley-required': "true"
               }))

    qf12A1_sdd = forms.ChoiceField(
        choices=list_referral_reasons,
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': "true"}))

    qf12A2 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Details"),
                   'class': 'form-control', 'rows': '3'}))

    qf12A3 = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))

    qf12A4_msc = forms.MultipleChoiceField(
        choices=list_referral_documents,
        widget=forms.CheckboxSelectMultiple(
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#id_qf12A4"}))


class AFCForm14A(forms.Form):
    """AFC Form 14A."""

    event_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date'),
               'class': 'form-control',
               'id': 'event_date',
               'data-parsley-required': "true"
               }))

    qf14A1A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qf9A1_rdo',
                   'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf14A1A_rdo_error"}))

    qf14A1B_rdo = forms.ChoiceField(
        choices=disability_degree,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf14A1B_rdo_error",
                   'class': 'form-check-inline'}))

    qf14A1C_rdo = forms.ChoiceField(
        choices=disability_degree,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf14A1C_rdo_error",
                   'class': 'form-check-inline'}))

    qf14A2A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qf9A1_rdo',
                   'data-parsley-required': 'true',
                   'class': 'form-check-inline',
                   'data-parsley-errors-container': "#qf14A2A_rdo_error"}))

    qf14A2B_rdo = forms.ChoiceField(
        choices=disability_degree,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf14A2B_rdo_error",
                   'class': 'form-check-inline'}))

    qf14A2C_rdo = forms.ChoiceField(
        choices=disability_degree,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf14A2C_rdo_error",
                   'class': 'form-check-inline'}))

    qf14A3A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qf14A3A_rdo',
                   'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf14A3A_rdo_error"}))

    qf14A3B_rdo = forms.ChoiceField(
        choices=disability_degree,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf14A3B_rdo_error",
                   'class': 'form-check-inline'}))

    qf14A3C_rdo = forms.ChoiceField(
        choices=disability_degree,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf14A3C_rdo_error",
                   'class': 'form-check-inline'}))

    qf14A4A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qf14A4A_rdo',
                   'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf14A4A_rdo_error"}))

    qf14A4B_rdo = forms.ChoiceField(
        choices=disability_degree,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf14A4B_rdo_error",
                   'class': 'form-check-inline'}))

    qf14A4C_rdo = forms.ChoiceField(
        choices=disability_degree,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf14A4C_rdo_error",
                   'class': 'form-check-inline'}))

    qf14A5A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qf14A5A_rdo',
                   'data-parsley-required': 'true',
                   'class': 'form-check-inline',
                   'data-parsley-errors-container': "#qf14A5A_rdo_error"}))

    qf14A5B_rdo = forms.ChoiceField(
        choices=disability_degree,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf14A5B_rdo_error",
                   'class': 'form-check-inline'}))

    qf14A5C_rdo = forms.ChoiceField(
        choices=disability_degree,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf14A5C_rdo_error",
                   'class': 'form-check-inline'}))

    qf14A6A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qf14A6A_rdo',
                   'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf14A6A_rdo_error"}))

    qf14A6B_rdo = forms.ChoiceField(
        choices=disability_degree,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf14A6B_rdo_error",
                   'class': 'form-check-inline'}))

    qf14A6C_rdo = forms.ChoiceField(
        choices=disability_degree,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf14A6C_rdo_error",
                   'class': 'form-check-inline'}))

    qf14A7A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qf14A7A_rdo',
                   'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf14A7A_rdo_error"}))

    qf14A7B_rdo = forms.ChoiceField(
        choices=disability_degree,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf14A7B_rdo_error",
                   'class': 'form-check-inline'}))

    qf14A7C_rdo = forms.ChoiceField(
        choices=disability_degree,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf14A7C_rdo_error",
                   'class': 'form-check-inline'}))

    qf14A8A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qf14A8A_rdo',
                   'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf14A8A_rdo_error"}))

    qf14A8B_rdo = forms.ChoiceField(
        choices=disability_degree,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf14A8B_rdo_error",
                   'class': 'form-check-inline'}))

    qf14A8C_rdo = forms.ChoiceField(
        choices=disability_degree,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf14A8C_rdo_error",
                   'class': 'form-check-inline'}))

    qf14A9A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qf14A9A_rdo',
                   'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf14A9A_rdo_error"}))

    qf14A9B_rdo = forms.ChoiceField(
        choices=disability_degree,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'data-parsley-errors-container': "#qf14A9B_rdo_error",
                   'class': 'form-check-inline'}))

    qf14A9C_rdo = forms.ChoiceField(
        choices=disability_degree,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'class': 'form-check-inline',
                   'data-parsley-errors-container': "#qf14A9C_rdo_error"}))

    qf14A10A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qf14A10A_rdo',
                   'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf14A10A_rdo_error"}))

    qf14A10B_rdo = forms.ChoiceField(
        choices=disability_degree,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'class': 'form-check-inline',
                   'data-parsley-errors-container': "#qf14A10B_rdo_error"}))

    qf14A10C_rdo = forms.ChoiceField(
        choices=disability_degree,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'class': 'form-check-inline',
                   'data-parsley-errors-container': "#qf14A10C_rdo_error"}))

    qf14A11A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qf14A11A_rdo',
                   'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf14A11A_rdo_error"}))

    qf14A11B_rdo = forms.ChoiceField(
        choices=disability_degree,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'class': 'form-check-inline',
                   'data-parsley-errors-container': "#qf14A11B_rdo_error"}))

    qf14A11C_rdo = forms.ChoiceField(
        choices=disability_degree,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'class': 'form-check-inline',
                   'data-parsley-errors-container': "#qf14A11C_rdo_error"}))

    qf14A12A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qf14A12A_rdo',
                   'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf14A12A_rdo_error"}))

    qf14A12B_rdo = forms.ChoiceField(
        choices=disability_degree,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'class': 'form-check-inline',
                   'data-parsley-errors-container': "#qf14A12B_rdo_error"}))

    qf14A12C_rdo = forms.ChoiceField(
        choices=disability_degree,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'class': 'form-check-inline',
                   'data-parsley-errors-container': "#qf14A12C_rdo_error"}))

    qf14A13A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qf14A13A_rdo',
                   'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf14A13A_rdo_error"}))

    qf14A13B_rdo = forms.ChoiceField(
        choices=disability_degree,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'class': 'form-check-inline',
                   'data-parsley-errors-container': "#qf14A13B_rdo_error"}))

    qf14A14A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qf14A14A_rdo',
                   'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf14A14A_rdo_error"}))

    qf14A14B_rdo = forms.ChoiceField(
        choices=disability_degree,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'class': 'form-check-inline',
                   'data-parsley-errors-container': "#qf14A14B_rdo_error"}))

    qf14A15A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qf14A15A_rdo',
                   'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf14A15A_rdo_error"}))

    qf14A15B_rdo = forms.ChoiceField(
        choices=disability_degree,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'class': 'form-check-inline',
                   'data-parsley-errors-container': "#qf14A15B_rdo_error"}))

    qf14A16A_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qf14A16A_rdo',
                   'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf14A16A_rdo_error"}))

    qf14A16B_rdo = forms.ChoiceField(
        choices=disability_degree,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'class': 'form-check-inline',
                   'data-parsley-errors-container': "#qf14A16B_rdo_error"}))

    qf14A17A = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Details"),
                   'class': 'form-control', 'rows': '3'}))

    qf14A18A = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Details"),
                   'class': 'form-control', 'rows': '3'}))

    qf14A19_rdo = forms.ChoiceField(
        choices=disability_actions,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qf14A19_rdo', 'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf14A19_rdo_error"}))

    qf14A20 = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))

    qf14A21B_rdo = forms.ChoiceField(
        choices=disability_degree,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'class': 'form-check-inline',
                   'data-parsley-errors-container': "#qf14A12B_rdo_error"}))

    qf14A21C_rdo = forms.ChoiceField(
        choices=disability_degree,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'class': 'form-check-inline',
                   'data-parsley-errors-container': "#qf14A12C_rdo_error"}))


class AFCForm15A(forms.Form):
    """AFC Form 15A."""

    event_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date'),
               'class': 'form-control',
               'id': 'event_date',
               'data-parsley-required': "true"
               }))

    qf15A1_rdo = forms.ChoiceField(
        choices=list_satisfied_level,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qf15A1_rdo',
                   'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf15A1_rdo_error"}))

    qf15A3 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Details"),
                   'class': 'form-control', 'rows': '3'}))

    qf15A4 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Details"),
                   'class': 'form-control', 'rows': '3'}))


class AFCForm16A(forms.Form):
    """AFC Form 16A."""

    event_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date'),
               'class': 'form-control',
               'id': 'event_date',
               'data-parsley-required': "true"
               }))

    qf16A1_rdo = forms.ChoiceField(
        choices=list_feeling_level,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qf16A1_rdo',
                   'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf16A1_rdo_error"}))

    qf16A2_rdo = forms.ChoiceField(
        choices=list_satisfied_level,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qf16A2_rdo',
                   'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qf16A2_rdo_error"}))

    qf16A3 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Details"),
                   'class': 'form-control', 'rows': '3'}))

    qf16A4 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Details"),
                   'class': 'form-control', 'rows': '3'}))

    qf16A5 = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': _("Details"),
                   'class': 'form-control', 'rows': '3'}))
