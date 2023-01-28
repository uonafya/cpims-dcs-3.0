"""Forms for authentication module."""
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .models import AppUser

import unicodedata
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives

UserModel = get_user_model()


def _unicode_ci_compare(s1, s2):
    """
    Perform case-insensitive comparison of two identifiers, using the
    recommended algorithm from Unicode Technical Report 36, section
    2.11.2(B)(2).
    """
    return (
        unicodedata.normalize("NFKC", s1).casefold()
        == unicodedata.normalize("NFKC", s2).casefold()
    )


class RegistrationForm(forms.Form):
    """Registration form."""

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('First name'),
               'class': 'form-control',
               'autofocus': 'true'}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Last name'),
               'class': 'form-control',
               'autofocus': 'true'}))
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Username'),
               'class': 'form-control',
               'autofocus': 'true'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': _('Password'),
               'class': 'form-control',
               'autofocus': 'true'}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': _('Re-enter password'),
               'class': 'form-control',
               'autofocus': 'true'}))
    phone_no = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Phone number'),
               'class': 'form-control',
               'autofocus': 'true'}))
    national_id = forms.IntegerField(widget=forms.TextInput(
        attrs={'placeholder': _('National id number'),
               'class': 'form-control',
               'autofocus': 'true'}))
    list_geolocation_id = forms.IntegerField(widget=forms.TextInput(
        attrs={'placeholder': _('Geo-location'),
               'class': 'form-control',
               'autofocus': 'true'}))
    staff_no = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Staff number'),
               'class': 'form-control',
               'autofocus': 'true'}))

    def clean_username(self):
        """Method to clean username."""
        try:
            AppUser.objects.get(username__iexact=self.cleaned_data['username'])
        except AppUser.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_(
            "The username already exists. Please try another one."))

    def clean(self):
        """Method to compare passwords."""
        form_obj = self.cleaned_data
        if 'password1' in form_obj and 'password2' in form_obj:
            if form_obj['password1'] != form_obj['password2']:
                raise forms.ValidationError(
                    _("The two password fields did not match."))
        return self.cleaned_data


class LoginForm(forms.Form):
    """Login form for the application."""

    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Username'),
               'class': 'form-control input-lg',
               'data-parsley-required': "true",
               'data-parsley-error-message': "Please enter your username.",
               'autofocus': 'true'}),
        error_messages={'required': 'Please enter your username.',
                        'invalid': 'Please enter a valid username.'})
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': _('Password'),
               'class': 'form-control input-lg',
               'data-parsley-required': "true",
               'data-placement': "after",
               'data-toggle': "password",
               'data-parsley-error-message': "Please enter your password.",
               'autofocus': 'true'}),
        error_messages={'required': 'Please enter your password.',
                        'invalid': 'Please enter a valid password.'},)

    def clean_username(self):
        """Method to clean username."""
        username = self.cleaned_data['username']
        if not username:
            raise forms.ValidationError("Please enter your username.")
        return username

    def clean_password(self):
        """Method to clean password."""
        password = self.cleaned_data['password']
        if not password:
            raise forms.ValidationError("Please enter your password.")
        return password


class RolesForm(forms.Form):
    """For generating Roles forms - with predefined groups."""

    acm = 'Access Manager'
    rgm = 'Registry Manager'
    scm = 'System Configuration'
    std = 'Standard logged in'
    swm = 'National child services'
    fa_lg = '<i class="fa fa-info-circle fa-lg"></i>'
    acm_text = ('<a href="#" id="id_ACM" data-toggle="tooltip" title="%s - '
                'This role allows allocation of roles (both restricted and '
                'non-restricted roles) to any user">%s</a>') % (acm, fa_lg)
    rgm_text = ('<a href="#" id="id_RGM" data-toggle="tooltip" title="%s - '
                'This role allows high level administration, de-duplication '
                'and corrections to the national registries (org units, '
                'workforce/users and beneficiaries">%s</a>') % (rgm, fa_lg)
    scm_text = ('<a href="#" id="id_SCM" data-toggle="tooltip" title="%s - '
                'This role allows managing the content of configurable drop '
                'down lists in the system, and maintaining system geographic '
                'data">%s</a>') % (scm, fa_lg)
    std_text = ('<a href="#" id="id_STD" data-toggle="tooltip" title="%s - '
                'This role is allocated by default to all logged in users / '
                'workforce members">%s</a>') % (std, fa_lg)
    ncs_text = ('<a href="#" id="id_SWM" data-toggle="tooltip" title="%s - '
                'This role allows viewing of sensitive individual beneficiary '
                'registry records and forms data throughout the entire '
                'country">%s</a>') % (swm, fa_lg)
    user_id = forms.CharField(widget=forms.HiddenInput)
    group_SCM = forms.BooleanField(label=_('%s %s' % (scm, scm_text)))
    group_RGM = forms.BooleanField(label=_('%s %s' % (rgm, rgm_text)))
    group_ACM = forms.BooleanField(label=_('%s %s' % (acm, acm_text)))
    group_SWM = forms.BooleanField(label=_('%s %s' % (swm, ncs_text)))
    group_STD = forms.BooleanField(label=_('%s %s' % (std, std_text)))
    reset_password = forms.BooleanField()

    ACTIVATE_CHOICES = (('activate', 'Activate (May log into CPIMS)',),
                        ('deactivate', 'Deactivate (May not log into CPIMS)',))
    activate_choice = forms.ChoiceField(
        widget=forms.RadioSelect, choices=ACTIVATE_CHOICES)


class RolesOrgUnits(forms.Form):
    """Form elements for the Roles Org units part."""

    org_unit_id = forms.CharField(widget=forms.HiddenInput)
    org_unit_name = forms.CharField(widget=forms.HiddenInput)
    org_unit_primary = forms.CharField(widget=forms.HiddenInput)
    group_RGU = forms.BooleanField()
    group_DUU = forms.BooleanField()
    group_DSU = forms.BooleanField()
    group_DEC = forms.BooleanField()


class RolesGeoArea(forms.Form):
    """Form elements for the Geo Area part."""

    sub_county = forms.CharField(widget=forms.HiddenInput)
    area_id = forms.CharField(widget=forms.HiddenInput)
    area_welfare = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class': 'area_check'}))


class PasswordResetForm(forms.Form):

    email_msg = "There was error processing your request. Contact Admin."
    error_messages = {
        'not_registered': email_msg,
    }

    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if not AppUser.objects.filter(
                reg_person__email__iexact=email, is_active=True).exists():
            raise forms.ValidationError(
                self.error_messages['not_registered'],
                code='not_registered',
            )
        return email

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(
            subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(
                html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")

        email_message.send()

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.
        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        # email_field_name = UserModel.get_email_field_name()
        email_field_name = 'email'
        '''
        active_users = UserModel._default_manager.filter(
            **{
                "%s__iexact" % email_field_name: email,
                "is_active": True,
            }
        )
        '''
        print('users details', email, email_field_name)
        active_users = UserModel._default_manager.filter(
            reg_person__email__iexact=email, is_active=True)

        for user in active_users:
            setattr(user, email_field_name, email)

        return (
            u
            for u in active_users
            if u.has_usable_password()
            and _unicode_ci_compare(email, getattr(u, email_field_name))
        )

    def save(
        self,
        domain_override=None,
        subject_template_name="registration/password_reset_subject.txt",
        email_template_name="registration/password_reset_email.html",
        use_https=True,
        token_generator=default_token_generator,
        from_email=None,
        request=None,
        html_email_template_name=None,
        extra_email_context=None,
    ):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override

        # email_field_name = UserModel.get_email_field_name()
        email_field_name = 'email'
        for user in self.get_users(email):
            print('user found', user)
            user_email = getattr(user, email_field_name)
            context = {
                "email": user_email,
                "domain": domain,
                "site_name": site_name,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                "token": token_generator.make_token(user),
                "protocol": "https" if use_https else "http",
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name,
                email_template_name,
                context,
                from_email,
                user_email,
                html_email_template_name=html_email_template_name,
            )
