from django import forms
from django.forms.widgets import RadioSelect
from django.utils.translation import gettext_lazy as _

from cpovc_main.functions import get_list


YESNO_CHOICES = get_list('yesno_id')
activity_list = get_list('ctip_activity_id')
means_list = get_list('ctip_means_id')
purpose_list = get_list('ctip_purpose_id')
form_b1_list = get_list('ctip_form_b1')
form_b2_list = get_list('ctip_form_b2')
form_b3_list = get_list('ctip_form_b3')
form_b4_list = get_list('ctip_form_b4')
form_d10_list = get_list('ctip_form_d10')
form_d21_list = get_list('ctip_form_d21')
form_labour_list = get_list('ctip_labour')
form_transport_list = get_list('ctip_transport')
form_companion_list = get_list('ctip_companion')
form_doc_type_list = get_list('ctip_docs_type')
form_no_exploit_list = get_list('ctip_no_exploit_reason')
form_freedom_list = get_list('ctip_freedom')
form_exploit_cond_list = get_list('ctip_exploit_condition')
ctip_YESNO = get_list('ctip_yesno_otdk')
trafficking_type = get_list('ctip_trafficking_type')
form_criteria = get_list('ctip_support_criteria')
form_situation_list = get_list('ctip_situation')
form_referral_list = get_list('ctip_referral_type')


class RadioCustomRenderer(RadioSelect):
    """Custom radio button renderer class."""

    def render(self):
        """Renderer override method."""
        pass


class CTIPForm(forms.Form):
    """Counter Trafficking form."""

    is_trafficking = forms.ChoiceField(
        choices=YESNO_CHOICES,
        initial='AYES',
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'occurence_nationality',
                   'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#trafficking_error"}))

    ctip_activity = forms.MultipleChoiceField(
        choices=activity_list,
        widget=forms.CheckboxSelectMultiple(
            attrs={'id': 'ctip_activity',
                   'data-parsley-errors-container': "#activity_error"}))

    ctip_means = forms.MultipleChoiceField(
        choices=means_list,
        widget=forms.CheckboxSelectMultiple(
            attrs={'data-parsley-required': 'false',
                   'id': 'ctip_means'}))

    ctip_purpose = forms.MultipleChoiceField(
        choices=purpose_list,
        widget=forms.CheckboxSelectMultiple(
            attrs={'data-parsley-required': 'false',
                   'id': 'ctip_purpose',
                   'data-parsley-errors-container': "#purpose_error"}))


class CTIPFormA(forms.Form):
    """Counter Trafficking form A."""

    has_consent = forms.ChoiceField(
        choices=YESNO_CHOICES,
        initial='AYES',
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'has_consent',
                   'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#trafficking_error"}))

    consent_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Consent Date'),
               'class': 'form-control',
               'id': 'consent_date',
               'data-parsley-required': "true"
               }))


class CTIPFormB(forms.Form):
    """Counter Trafficking form B."""

    qfB1 = forms.MultipleChoiceField(
        choices=form_b1_list,
        widget=forms.CheckboxSelectMultiple(
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#id_qfB1"}))

    qfB1_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Note'),
               'class': 'form-control',
               'id': 'qfB1_txt',
               'rows': '3'}))

    qfB2 = forms.MultipleChoiceField(
        choices=form_b2_list,
        widget=forms.CheckboxSelectMultiple(
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#id_qfB2"}))

    qfB2_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Note'),
               'class': 'form-control',
               'id': 'qfB2_txt',
               'rows': '3'}))

    qfB3 = forms.MultipleChoiceField(
        choices=form_b3_list,
        widget=forms.CheckboxSelectMultiple(
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#id_qfB3"}))

    qfB3_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Note'),
               'class': 'form-control',
               'id': 'qfB3_txt',
               'rows': '3'}))

    qfB4 = forms.MultipleChoiceField(
        choices=form_b4_list,
        widget=forms.CheckboxSelectMultiple(
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#id_qfB4"}))

    qfB4_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Note'),
               'class': 'form-control',
               'id': 'qfB4_txt',
               'rows': '3'}))

    event_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Event Date'),
               'class': 'form-control',
               'id': 'event_date',
               'data-parsley-required': "true"
               }))

    qfB5 = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'qfB5', 'data-parsley-required': "true"
               }))


class CTIPFormC(forms.Form):
    """Counter Trafficking form C."""

    qfC1_txt = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'qfC1_txt',
               'data-parsley-required': "true"
               }))

    qfC2_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        initial='AYES',
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfC2',
                   'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#trafficking_error"}))

    qfC3_txt = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'qfC3_txt',
               'data-parsley-required': "true"
               }))

    qfC4_txt = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'qfC4_txt',
               'data-parsley-required': "true"
               }))

    qfC5_txt = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'qfC5_txt',
               'data-parsley-required': "true"
               }))

    qfC6_txt = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'qfC6_txt',
               'data-parsley-required': "true"
               }))

    qfC7_txt = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Notes'),
               'class': 'form-control',
               'id': 'qfC7_txt', 'data-parsley-required': "true",
               'rows': '3'}))

    qfC8_txt = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Notes'),
               'class': 'form-control',
               'id': 'qfC8_txt', 'data-parsley-required': "true",
               'rows': '3'}))

    qfC9_txt = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Notes'),
               'class': 'form-control',
               'id': 'qfC9_txt', 'data-parsley-required': "true",
               'rows': '3'}))

    qfC10_txt = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Notes'),
               'class': 'form-control',
               'id': 'qfC10_txt', 'data-parsley-required': "true",
               'rows': '3'}))

    qfC11_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Notes'),
               'class': 'form-control',
               'id': 'qfC11_txt',
               'rows': '3'}))

    event_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Event Date'),
               'class': 'form-control',
               'id': 'event_date',
               'data-parsley-required': "true"
               }))


class CTIPFormD(forms.Form):
    """Counter Trafficking form D."""

    # Registration data

    qfDR1_txt = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'qfDR1_txt'}))

    qfDR2_txt = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'qfDR2_txt'}))

    qfDR3_txt = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'qfDR3_txt'}))

    qfDR4_txt = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'qfDR4_txt'}))

    qfDR5_txt = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'qfDR5_txt'}))

    qfDR6_txt = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'qfDR6_txt'}))

    qfDR7_txt = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'qfDR7_txt'}))

    qfDR8_txt = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'qfDR8_txt'}))

    qfDR9_txt = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'qfDR9_txt'}))

    qfDR10_txt = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'qfDR10_txt'}))

    qfDR11_txt = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'qfDR11_txt'}))

    qfDR12_txt = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'qfDR12_txt'}))

    qfDR13_txt = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'qfDR13_txt'}))

    qfDR14_txt = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'qfDR14_txt'}))

    # Case data

    qfDC1_rdo = forms.MultipleChoiceField(
        choices=form_referral_list,
        required=False,
        widget=forms.RadioSelect(
            attrs={'id': 'qfDC1_rdo'}))

    qfDC2_txt = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'qfDC2_txt'}))

    qfDC3_txt = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'qfDC3_txt'}))

    qfDC4_txt = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'qfDC4_txt'}))

    qfDC5_txt = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'qfDC5_txt'}))

    qfDC6_txt = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'qfDC6_txt'}))

    qfDC7_txt = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'qfDC7_txt'}))

    qfDC8_txt = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'qfDC8_txt'}))

    qfDC9_txt = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'qfDC9_txt'}))

    qfDC10_txt = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'qfDC10_txt'}))

    qfDC11_txt = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'qfDC11_txt'}))

    qfDC12_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Details'),
               'class': 'form-control',
               'id': 'qfDC12_txt',
               'rows': '3'}))

    # Recruitment

    qfD10 = forms.MultipleChoiceField(
        choices=form_d10_list,
        widget=forms.CheckboxSelectMultiple(
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#id_qfD10"}))

    qfD11_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Other details'),
               'class': 'form-control',
               'id': 'qfD11_txt',
               'rows': '3'}))

    qfD20 = forms.MultipleChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfD20', 'data-parsley-required': 'true'}))

    qfD21 = forms.MultipleChoiceField(
        choices=form_d21_list,
        widget=forms.CheckboxSelectMultiple(
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#id_qfD21"}))

    qfD21_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Other details'),
               'class': 'form-control',
               'id': 'qfD21_txt',
               'rows': '3'}))

    qfD30 = forms.MultipleChoiceField(
        choices=form_labour_list,
        required=False,
        widget=forms.CheckboxSelectMultiple(
            attrs={'data-parsley-errors-container': "#id_qfD30"}))

    qfD31_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Other details'),
               'class': 'form-control',
               'id': 'qfD31_txt',
               'rows': '3'}))

    qfD32_txt = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': _('Specify'),
               'class': 'form-control'
               }))

    qfD40_rdo = forms.MultipleChoiceField(
        choices=YESNO_CHOICES,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfD40_rdo'}))

    qfD41_txt = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': _('Specify'),
               'class': 'form-control'
               }))

    qfD42_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Other benefits'),
               'class': 'form-control',
               'id': 'qfD31_txt',
               'rows': '3'}))

    qfD50_txt = forms.DateField(required=False, widget=forms.TextInput(
        attrs={'placeholder': _('Month/Year 1st date'),
               'class': 'form-control',
               'id': 'qfD50_txt'
               }))

    qfD60_rdo = forms.MultipleChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfD60_rdo', 'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#id_qfD60_error"}))

    qfD70_txt = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Specify'),
               'class': 'form-control', 'data-parsley-required': 'true'
               }))

    qfD80_txt = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Specify'),
               'class': 'form-control', 'data-parsley-required': 'true'
               }))

    qfD90 = forms.MultipleChoiceField(
        choices=form_transport_list,
        widget=forms.CheckboxSelectMultiple(
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#id_qfD90"}))

    qfD91_txt = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Name'),
               'class': 'form-control',
               'data-parsley-required': 'true',
               'id': 'qfD91_txt',
               }))

    qfD100_rdo = forms.MultipleChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfD100_rdo', 'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qfD100_rdo_error"}))

    qfD101 = forms.MultipleChoiceField(
        choices=form_companion_list,
        widget=forms.CheckboxSelectMultiple(
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#id_qfD101"}))

    qfD102_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Other'),
               'class': 'form-control',
               'id': 'qfD102_txt',
               'rows': '3'}))

    qfD110_rdo = forms.MultipleChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfD110_rdo', 'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qfD110_rdo_error"}))

    qfD111_rdo = forms.MultipleChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfD111_rdo', 'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qfD111_rdo_error"}))

    qfD112_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Where and how?'),
               'class': 'form-control',
               'id': 'qfD112_txt',
               'rows': '3'}))

    qfD113_rdo = forms.MultipleChoiceField(
        choices=form_doc_type_list,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfD113_rdo', 'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qfD113_rdo_error"}))

    qfD120_rdo = forms.MultipleChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfD120_rdo', 'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qfD120_rdo_error"}))

    qfD121_txt = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Chronological order'),
               'class': 'form-control',
               'id': 'qfD121_txt', 'data-parsley-required': 'true',
               'rows': '3'}))

    qfD122_rdo = forms.MultipleChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfD122_rdo', 'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qfD122_rdo_error"}))

    qfD123 = forms.MultipleChoiceField(
        choices=form_labour_list,
        required=False,
        widget=forms.CheckboxSelectMultiple(
            attrs={'data-parsley-errors-container': "#id_qfD123"}))

    qfD123_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Other'),
               'class': 'form-control',
               'id': 'qfD123_txt',
               'rows': '3'}))

    # Exploitation phase
    qfD130 = forms.MultipleChoiceField(
        choices=form_labour_list,
        widget=forms.CheckboxSelectMultiple(
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#id_qfD130"}))

    qfD131_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Other'),
               'class': 'form-control',
               'id': 'qfD131_txt',
               'rows': '3'}))

    qfD140_txt = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': _('How soon'),
               'class': 'form-control',
               'id': 'qfD140_txt',
               }))

    qfD141_txt = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': _('Age'),
               'class': 'form-control',
               'id': 'qfD141_txt',
               }))

    qfD142_rdo = forms.MultipleChoiceField(
        choices=YESNO_CHOICES,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfD142_rdo'}))

    qfD143_txt = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': _('How long?'),
               'class': 'form-control',
               'id': 'qfD143_txt',
               }))

    qfD144_rdo = forms.MultipleChoiceField(
        choices=YESNO_CHOICES,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfD144_rdo'}))

    qfD150_rdo = forms.MultipleChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfD150_rdo', 'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qfD150_rdo_error"}))

    qfD160_rdo = forms.MultipleChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfD160_rdo', 'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qfD160_rdo_error"}))

    qfD161_rdo = forms.MultipleChoiceField(
        choices=form_no_exploit_list,
        widget=forms.RadioSelect(
            attrs={'id': 'qfD161_rdo', 'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qfD161_rdo_error"}))

    qfD162_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Other'),
               'class': 'form-control',
               'id': 'qfD162_txt',
               'rows': '3'}))

    qfD170_rdo = forms.MultipleChoiceField(
        choices=form_freedom_list,
        widget=forms.RadioSelect(
            attrs={'id': 'qfD170_rdo', 'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qfD170_rdo_error"}))

    qfD180_rdo = forms.MultipleChoiceField(
        choices=form_exploit_cond_list,
        widget=forms.RadioSelect(
            attrs={'id': 'qfD180_rdo', 'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qfD180_rdo_error"}))

    # Corroborative Materials
    qfD190A_rdo = forms.MultipleChoiceField(
        choices=ctip_YESNO,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfD190A_rdo'}))

    qfD190B_rdo = forms.MultipleChoiceField(
        choices=ctip_YESNO,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfD190B_rdo'}))

    qfD190C_rdo = forms.MultipleChoiceField(
        choices=ctip_YESNO,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfD190C_rdo'}))

    qfD190D_rdo = forms.MultipleChoiceField(
        choices=ctip_YESNO,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfD190D_rdo'}))

    qfD190E_rdo = forms.MultipleChoiceField(
        choices=ctip_YESNO,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfD190E_rdo'}))

    qfD190F_rdo = forms.MultipleChoiceField(
        choices=ctip_YESNO,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfD190F_rdo'}))

    qfD190G_rdo = forms.MultipleChoiceField(
        choices=ctip_YESNO,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfD190G_rdo'}))

    qfD190H_rdo = forms.MultipleChoiceField(
        choices=ctip_YESNO,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfD190H_rdo'}))

    qfD190H_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Details'),
               'class': 'form-control',
               'id': 'qfD190H_txt',
               'rows': '2'}))

    # Decision making
    qfD200_rdo = forms.MultipleChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfD200_rdo', 'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qfD200_rdo_error"}))

    qfD201_txt = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Other'),
               'class': 'form-control',
               'id': 'qfD201_txt', 'data-parsley-required': 'true',
               'rows': '3'}))

    qfD210_txt = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('By whom?'),
               'class': 'form-control',
               'id': 'qfD210_txt', 'data-parsley-required': 'true'
               }))

    qfD220_rdo = forms.MultipleChoiceField(
        choices=trafficking_type,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfD220_rdo', 'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qfD220_rdo_error"}))

    qfD230_rdo = forms.MultipleChoiceField(
        choices=YESNO_CHOICES,
        required=False,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfD230_rdo'}))

    qfD231_rdo = forms.MultipleChoiceField(
        choices=form_criteria,
        required=False,
        widget=forms.RadioSelect(
            attrs={'id': 'qfD231_rdo'}))

    qfD232_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Other'),
               'class': 'form-control',
               'id': 'qfD232_txt',
               'rows': '3'}))

    qfD240_rdo = forms.MultipleChoiceField(
        choices=YESNO_CHOICES,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfD240_rdo', 'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qfD240_rdo_error"}))

    qfD241 = forms.MultipleChoiceField(
        choices=form_situation_list,
        widget=forms.CheckboxSelectMultiple(
            attrs={'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#id_qfD241"}))

    qfD250_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Other'),
               'class': 'form-control',
               'id': 'qfD250_txt',
               'rows': '3'}))

    event_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Event Date'),
               'class': 'form-control',
               'id': 'event_date',
               'data-parsley-required': "true"
               }))


class CTIPFormE(forms.Form):
    """Counter Trafficking form D."""

    qfE1_txt = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={'placeholder': _('Explain'),
                   'class': 'form-control',
                   'data-parsley-required': "true",
                   'id': 'qfE1_txt',
                   'rows': '3'}))

    qfE1b_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Intervention'),
               'class': 'form-control',
               'id': 'qfE1b_txt',
               'rows': '3'}))

    qfE2_txt = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Explain'),
               'class': 'form-control',
               'data-parsley-required': "true",
               'id': 'qfE2_txt',
               'rows': '3'}))

    qfE2b_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Intervention'),
               'class': 'form-control',
               'id': 'qfE2b_txt',
               'rows': '3'}))

    qfE3_txt = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Explain'),
               'class': 'form-control',
               'data-parsley-required': "true",
               'id': 'qfE3_txt',
               'rows': '3'}))

    qfE3b_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Intervention'),
               'class': 'form-control',
               'id': 'qfE3b_txt',
               'rows': '3'}))

    qfE4_txt = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Explain'),
               'class': 'form-control',
               'data-parsley-required': "true",
               'id': 'qfE4_txt',
               'rows': '3'}))

    qfE4b_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Intervention'),
               'class': 'form-control',
               'id': 'qfE4b_txt',
               'rows': '3'}))

    qfE5_txt = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Explain'),
               'class': 'form-control',
               'data-parsley-required': "true",
               'id': 'qfE5_txt',
               'rows': '3'}))

    qfE5b_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Intervention'),
               'class': 'form-control',
               'id': 'qfE5b_txt',
               'rows': '3'}))

    qfE6_txt = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Explain'),
               'class': 'form-control',
               'data-parsley-required': "true",
               'id': 'qfE6_txt',
               'rows': '3'}))

    qfE6b_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Intervention'),
               'class': 'form-control',
               'id': 'qfE6b_txt',
               'rows': '3'}))

    qfE7_txt = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Explain'),
               'class': 'form-control',
               'data-parsley-required': "true",
               'id': 'qfE7_txt',
               'rows': '3'}))

    qfE7b_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Intervention'),
               'class': 'form-control',
               'id': 'qfE7b_txt',
               'rows': '3'}))

    qfE8_txt = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Explain'),
               'class': 'form-control',
               'data-parsley-required': "true",
               'id': 'qfE8_txt',
               'rows': '3'}))

    qfE8b_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Intervention'),
               'class': 'form-control',
               'id': 'qfE8b_txt',
               'rows': '3'}))

    qfE9_txt = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Explain'),
               'class': 'form-control',
               'data-parsley-required': "true",
               'id': 'qfE9_txt',
               'rows': '3'}))

    qfE9b_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Intervention'),
               'class': 'form-control',
               'id': 'qfE9b_txt',
               'rows': '3'}))

    qfE10_txt = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Explain'),
               'class': 'form-control',
               'data-parsley-required': "true",
               'id': 'qfE10_txt',
               'rows': '3'}))

    qfE10b_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Intervention'),
               'class': 'form-control',
               'id': 'qfE10b_txt',
               'rows': '3'}))

    qfE11_txt = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Explain'),
               'class': 'form-control',
               'data-parsley-required': "true",
               'id': 'qfE11_txt',
               'rows': '3'}))

    qfE11b_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Intervention'),
               'class': 'form-control',
               'id': 'qfE11b_txt',
               'rows': '3'}))

    qfE12_txt = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Explain'),
               'class': 'form-control',
               'data-parsley-required': "true",
               'id': 'qfE12_txt',
               'rows': '3'}))

    qfE12b_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Intervention'),
               'class': 'form-control',
               'id': 'qfE12b_txt',
               'rows': '3'}))

    qfE13_txt = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Explain'),
               'class': 'form-control',
               'data-parsley-required': "true",
               'id': 'qfE13_txt',
               'rows': '3'}))

    qfE13b_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Intervention'),
               'class': 'form-control',
               'id': 'qfE13b_txt',
               'rows': '3'}))

    event_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Event Date'),
               'class': 'form-control',
               'id': 'event_date',
               'data-parsley-required': "true"
               }))


class CTIPFormF(forms.Form):
    """Counter Trafficking form C."""

    qfF1_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfF1_rdo', 'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qfF1_rdo_error"}))

    qfF1_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Explain'),
               'class': 'form-control',
               'id': 'qfF1_txt',
               'rows': '3'}))

    qfF2_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfF2_rdo', 'data-parsley-required': 'true',
                   'data-parsley-errors-container': "#qfF2_rdo_error"}))

    qfF2_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Explain'),
               'class': 'form-control',
               'id': 'qfF2_txt',
               'rows': '3'}))

    qfF3_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfF3_rdo', 'data-parsley-required': "true",
                   'data-parsley-errors-container': "#qfF3_rdo_error"}))

    qfF3_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Explain'),
               'class': 'form-control',
               'id': 'qfF3_txt',
               'rows': '3'}))

    qfF4_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfF4_rdo', 'data-parsley-required': "true",
                   'data-parsley-errors-container': "#qfF4_rdo_error"}))

    qfF4_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Explain'),
               'class': 'form-control',
               'id': 'qfF4_txt',
               'rows': '3'}))

    qfF5_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfF5_rdo', 'data-parsley-required': "true",
                   'data-parsley-errors-container': "#qfF5_rdo_error"}))

    qfF5_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Explain'),
               'class': 'form-control',
               'id': 'qfF5_txt',
               'rows': '3'}))

    qfF6_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfF6_rdo', 'data-parsley-required': "true",
                   'data-parsley-errors-container': "#qfF6_rdo_error"}))

    qfF6_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Explain'),
               'class': 'form-control',
               'id': 'qfF6_txt',
               'rows': '3'}))

    qfF7_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfF7_rdo', 'data-parsley-required': "true",
                   'data-parsley-errors-container': "#qfF7_rdo_error"}))

    qfF7_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Explain'),
               'class': 'form-control',
               'id': 'qfF7_txt',
               'rows': '3'}))

    qfF8_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfF8_rdo', 'data-parsley-required': "true",
                   'data-parsley-errors-container': "#qfF8_rdo_error"}))

    qfF8_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Explain'),
               'class': 'form-control',
               'id': 'qfF8_txt',
               'rows': '3'}))

    qfF9_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfF9_rdo', 'data-parsley-required': "true",
                   'data-parsley-errors-container': "#qfF9_rdo_error"}))

    qfF9_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Explain'),
               'class': 'form-control',
               'id': 'qfF9_txt',
               'rows': '3'}))

    qfF10_rdo = forms.ChoiceField(
        choices=YESNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            # renderer=RadioCustomRenderer,
            attrs={'id': 'qfF10_rdo', 'data-parsley-required': "true",
                   'data-parsley-errors-container': "#qfF10_rdo_error"}))

    qfF10_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Explain'),
               'class': 'form-control',
               'id': 'qfF10_txt',
               'rows': '3'}))

    event_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Event Date'),
               'class': 'form-control',
               'id': 'event_date',
               'data-parsley-required': "true"
               }))


class CTIPFormG(forms.Form):
    """Counter Trafficking form C."""

    qfC11_txt = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': _('Note'),
               'class': 'form-control',
               'id': 'qfB4_txt',
               'rows': '3'}))

    event_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Event Date'),
               'class': 'form-control',
               'id': 'event_date',
               'data-parsley-required': "true"
               }))
