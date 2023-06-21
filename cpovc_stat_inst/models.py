import uuid
from django.db import models
from django.utils import timezone

# Create your models here.
from cpovc_registry.models import RegPerson
from cpovc_forms.models import OVCCaseRecord

YES_NO_CHOICES = (
    ("yes", "Yes"),
    ("no", "No"),
)


class SIAdmission(models.Model):
    si_id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    person_id = models.ForeignKey(RegPerson, on_delete=models.CASCADE)
    institution_type = models.CharField(max_length=100, null=False, blank=False)
    date_of_admission = models.DateField(null=True, blank=True)
    current_year_of_school = models.CharField(max_length=50, null=True, blank=True)
    type_of_entry = models.CharField(max_length=100, null=True, blank=True)
    referral_source = models.CharField(max_length=100, null=True, blank=True)
    child_category = models.CharField(max_length=100, null=True, blank=True)
    abused_child_desc = models.CharField(max_length=100, null=True, blank=True)
    referral_source_others = models.TextField(null=True, blank=True)
    referrer_name = models.CharField(max_length=100, null=True, blank=True)
    referrer_address = models.CharField(max_length=100, null=True, blank=True)
    referrer_phone = models.CharField(max_length=100, null=True, blank=True)
    not_contact_child = models.CharField(
        max_length=3, choices=YES_NO_CHOICES, null=True, blank=True
    )
    name_not_contact_child = models.CharField(max_length=100, null=True, blank=True)
    relationship_to_child_not_contact_child = models.CharField(
        max_length=100, null=True, blank=True
    )
    consent_form_signed = models.CharField(
        max_length=3, choices=YES_NO_CHOICES, null=True, blank=True
    )
    commital_court_order = models.CharField(
        max_length=3, choices=YES_NO_CHOICES, null=True, blank=True
    )
    school_name = models.CharField(max_length=100, null=True, blank=True)
    health_status = models.TextField(null=True, blank=True)
    special_needs = models.TextField(null=True, blank=True)
    workforce_id = models.IntegerField(null=True, blank=True)
    audit_date = models.DateField(null=True, blank=True)

    def _get_cases(self):
        _cases = SIAdmission.objects.all().count()
        if self.case_number:
            return _cases
        else:
            return _cases + 1

    def save(self, *args, **kwargs):
        # This is to save the Unique code.
        if self.pk is None and not self.case_number:
            self.case_number = self.case_number
        elif self.pk and not self.case_number:
            case_num = self._get_cases()
            self.case_number = case_num

        # Call the original save method
        super(SIAdmission, self).save(*args, **kwargs)

    class Meta:
        db_table = "ovc_si_main"
        verbose_name = "Statutory Institutions"
        verbose_name_plural = "Statutory Institutions"
        app_label = "Statutory Institutions"

    def __unicode__(self):
        """To be returned by admin actions."""
        return "%s" % (str(self.case))
