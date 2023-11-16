from django import forms
from django.utils.translation import gettext_lazy as _

from cpovc_main.models import ListQuestions
from cpovc_main.functions import get_list


class SIForm(forms.Form):
    """All statutory Institution Forms from the DB."""

    def __init__(self, form_id, *args, **kwargs):
        """Get all forms data from the DB."""
        self.form_id = form_id
        super(SIForm, self).__init__(*args, **kwargs)

        form_elements = self.get_form_data(self.form_id)

        for form_el in form_elements:
            choices = ()
            f_id = form_elements[form_el]['id']
            f_label = form_elements[form_el]['label']
            field_id = form_elements[form_el]['field_id']
            type_id = form_elements[form_el]['type_id']
            set_id = form_elements[form_el]['set_id']
            is_required = form_elements[form_el]['is_required']
            ftype_id = form_elements[form_el]['form_type_id']
            fid = int(ftype_id) if ftype_id else 0
            err_id = "#%s_error" % f_id
            if field_id:
                if type_id == 'FMSL':
                    choices = get_list(field_id, 'Please Select')
                else:
                    choices = get_list(field_id)
            if type_id == 'FMSL':
                f_data = forms.ChoiceField(
                    choices=choices,
                    label=f_label,
                    required=is_required,
                    widget=forms.Select(
                        attrs={'class': 'form-control', 'id': f_id}))
            elif type_id == 'FMRD':
                f_data = forms.ChoiceField(
                    choices=choices,
                    label=f_label,
                    required=is_required,
                    widget=forms.RadioSelect(
                        attrs={'id': f_id,
                               'data-parsley-errors-container': err_id}))
            elif type_id == 'FMTA':
                rows = 5 if fid else 2
                f_data = forms.CharField(
                    required=is_required,
                    label=f_label,
                    widget=forms.Textarea(
                        attrs={'placeholder': '',
                               'class': 'form-control', 'rows': '%s' % rows}))
            elif type_id == 'FMCB':
                f_data = forms.MultipleChoiceField(
                    choices=choices,
                    label=f_label,
                    required=is_required,
                    widget=forms.CheckboxSelectMultiple(
                        attrs={'data-parsley-errors-container': err_id}))
            elif type_id == 'FMFL':
                f_data = forms.FileField(
                    label=f_label,
                    required=is_required,
                    widget=forms.FileInput(
                        attrs={'class': 'form-control',
                               'accept': 'image/*,video/*'}))
            else:
                if set_id == 3:
                    date_class = 'other_date' if fid else 'event_date'
                    f_data = forms.DateField(
                        required=is_required,
                        label=f_label,
                        widget=forms.TextInput(
                            attrs={'placeholder': '',
                                   'class': 'form-control %s' % date_class,
                                   'id': f_id}))
                elif set_id == 2:
                    f_data = forms.IntegerField(
                        required=is_required,
                        label=f_label,
                        widget=forms.NumberInput(
                            attrs={'placeholder': '',
                                   'class': 'form-control',
                                   'id': f_id}))
                else:
                    if type_id == 'FMRO':
                        f_data = forms.CharField(
                            required=is_required,
                            label=f_label,
                            widget=forms.TextInput(
                                attrs={'placeholder': '',
                                       'readonly': 'readonly',
                                       'class': 'form-control', 'id': f_id}))
                    else:
                        f_data = forms.CharField(
                            required=is_required,
                            label=f_label,
                            widget=forms.TextInput(
                                attrs={'placeholder': '',
                                       'class': 'form-control', 'id': f_id}))

            self.fields[f_id] = f_data

    event_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date'),
               'class': 'form-control', 'id': 'event_date',
               'data-parsley-required': "true"
               }))

    def get_form_data(self, form_id):
        try:
            fms = {}
            forms = ListQuestions.objects.filter(
                form__form_guid=form_id, is_void=False)
            for fm in forms:
                fd = {'id': fm.question_code,
                      'label': fm.question_text,
                      'type_id': fm.answer_type_id,
                      'field_id': fm.answer_field_id,
                      'form_type_id': fm.form_type_id,
                      'set_id': fm.answer_set_id,
                      'is_required': fm.question_required}
                fms[fm] = fd
        except Exception:
            return {}
        else:
            return fms
