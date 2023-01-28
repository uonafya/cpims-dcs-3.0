import uuid
from django.db import models
from django.utils import timezone

from cpovc_registry.models import RegPerson
from cpovc_forms.models import OVCCaseRecord


class CTIPMain(models.Model):
    case = models.ForeignKey(OVCCaseRecord, on_delete=models.CASCADE)
    case_number = models.CharField(max_length=12, blank=True)
    case_date = models.DateField()
    country = models.CharField(max_length=2, blank=True)
    person = models.ForeignKey(RegPerson, on_delete=models.CASCADE)
    case_status = models.BooleanField(null=True, default=None)
    case_stage = models.IntegerField(default=0)
    has_consent = models.BooleanField(default=False)
    consent_date = models.DateField(null=True, blank=True)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)

    def _get_cases(self):
        _cases = CTIPMain.objects.all().count()
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
        super(CTIPMain, self).save(*args, **kwargs)

    class Meta:
        db_table = 'ovc_ctip_main'
        verbose_name = 'Trafficked Person'
        verbose_name_plural = 'Trafficked Persons'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (str(self.case))


class CTIPEvents(models.Model):
    event_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    case = models.ForeignKey(OVCCaseRecord, on_delete=models.CASCADE)
    event_count = models.IntegerField(default=1)
    event_date = models.DateField()
    form_id = models.CharField(max_length=1, blank=True)
    person = models.ForeignKey(RegPerson, on_delete=models.CASCADE)
    interviewer = models.CharField(max_length=100, blank=True)
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)

    class Meta:
        db_table = 'ovc_ctip_event'
        verbose_name = 'Trafficking Event'
        verbose_name_plural = 'Trafficking Events'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (str(self.case))


class CTIPForms(models.Model):
    form_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    event = models.ForeignKey(CTIPEvents, on_delete=models.CASCADE)
    question_id = models.CharField(max_length=12)
    item_value = models.CharField(max_length=5)
    item_detail = models.TextField(null=True, blank=True)
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)

    class Meta:
        db_table = 'ovc_ctip_form'
        verbose_name = 'Trafficking Form data'
        verbose_name_plural = 'Trafficking Forms data'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (str(self.event))
