from django.db import models
import uuid
from django.db import models
from django.utils import timezone

from cpovc_auth.models import AppUser

from cpovc_registry.models import RegPerson, RegOrgUnit
from cpovc_forms.models import OVCCaseRecord, OVCPlacement

YES_NO_CHOICES = (("AYES", "Yes"), ("ANNO", "No"),)


class CCIMain(models.Model):
    si_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    case = models.ForeignKey(
        OVCCaseRecord, on_delete=models.CASCADE, null=True)
    person = models.ForeignKey(RegPerson, on_delete=models.CASCADE)
    org_unit = models.ForeignKey(
        RegOrgUnit, on_delete=models.CASCADE, null=True)
    placement = models.ForeignKey(
        OVCPlacement, on_delete=models.CASCADE, null=True)
    org_type = models.CharField(max_length=5, null=True, blank=True)
    case_status = models.BooleanField(null=True, default=None)
    case_stage = models.IntegerField(default=0)
    case_date = models.DateField()
    case_number = models.CharField(max_length=12, blank=True)
    created_by = models.ForeignKey(
        AppUser, blank=True, on_delete=models.CASCADE)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_modified = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)

    def _get_cases(self):
        _cases = CCIMain.objects.all().count()
        if self.case_number:
            return _cases
        else:
            return _cases + 1

    def _case_serial(self):
        """Calculate age in years only."""
        fy = self.case_date.strftime('%Y')
        fm = int(self.case_date.strftime('%m'))
        if fm > 6:
            fy = int(fy) + 1
        cs = '%s/%s' % (self.case_number, fy)
        return cs

    case_serial = property(_case_serial)

    def save(self, *args, **kwargs):
        # This is to save the Unique code.
        if self.pk is None and not self.case_number:
            self.case_number = self.case_number
        elif self.pk and not self.case_number:
            case_num = self._get_cases()
            self.case_number = case_num

        # Call the original save method
        super(CCIMain, self).save(*args, **kwargs)

    class Meta:
        db_table = 'ovc_cci_registration'
        verbose_name = 'CCI Care'
        verbose_name_plural = 'CCI Cares'

    def __str__(self):
        """To be returned by admin actions."""
        return '%s - %s' % (str(self.case_number), str(self.case))


class CCIEvents(models.Model):
    event_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    care = models.ForeignKey(CCIMain, on_delete=models.CASCADE)
    event_count = models.IntegerField(default=1)
    event_date = models.DateField()
    form_id = models.CharField(max_length=10, blank=True)
    person = models.ForeignKey(RegPerson, on_delete=models.CASCADE)
    related_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(
        AppUser, blank=True, on_delete=models.CASCADE)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_modified = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)

    class Meta:
        db_table = 'ovc_cci_event'
        verbose_name = 'CCI Event'
        verbose_name_plural = 'CCI Events'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (str(self.case))


class CCIForms(models.Model):
    form_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    event = models.ForeignKey(CCIEvents, on_delete=models.CASCADE)
    question_id = models.CharField(max_length=50)
    item_value = models.CharField(max_length=10)
    item_detail = models.TextField(null=True, blank=True)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_modified = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)

    class Meta:
        db_table = 'ovc_cci_form'
        verbose_name = 'CCI Form data'
        verbose_name_plural = 'CCII Forms data'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (str(self.question_id))
