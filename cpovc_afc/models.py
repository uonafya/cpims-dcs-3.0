import uuid
from django.db import models
from django.utils import timezone

from cpovc_registry.models import RegPerson, RegOrgUnit
from cpovc_forms.models import OVCCaseRecord
from cpovc_auth.models import AppUser


class AFCMain(models.Model):
    care_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    case = models.ForeignKey(OVCCaseRecord, on_delete=models.CASCADE)
    case_number = models.CharField(max_length=12, blank=True)
    care_type = models.CharField(max_length=5, null=True, blank=True)
    care_sub_type = models.CharField(max_length=5, null=True, blank=True)
    person = models.ForeignKey(RegPerson, on_delete=models.CASCADE)
    school_level = models.CharField(max_length=4, null=True)
    immunization_status = models.CharField(max_length=4, null=True)
    org_unit = models.ForeignKey(RegOrgUnit, on_delete=models.CASCADE)
    case_status = models.BooleanField(null=True, default=None)
    case_stage = models.IntegerField(default=0)
    case_date = models.DateField()
    created_by = models.ForeignKey(
        AppUser, blank=True, on_delete=models.CASCADE)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_modified = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)

    def _get_cases(self):
        _cases = AFCMain.objects.all().count()
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
        super(AFCMain, self).save(*args, **kwargs)

    class Meta:
        db_table = 'ovc_afc_main'
        verbose_name = 'Alternative Care'
        verbose_name_plural = 'Alternative Cares'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s - %s' % (str(self.case_number), str(self.case))


class AFCEvents(models.Model):
    event_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    case = models.ForeignKey(OVCCaseRecord, on_delete=models.CASCADE)
    care = models.ForeignKey(AFCMain, on_delete=models.CASCADE)
    event_count = models.IntegerField(default=1)
    event_date = models.DateField()
    form_id = models.CharField(max_length=3, blank=True)
    person = models.ForeignKey(RegPerson, on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        AppUser, blank=True, on_delete=models.CASCADE)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_modified = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)

    class Meta:
        db_table = 'ovc_afc_event'
        verbose_name = 'AFC Event'
        verbose_name_plural = 'AFC Events'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (str(self.case))


class AFCForms(models.Model):
    form_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    event = models.ForeignKey(AFCEvents, on_delete=models.CASCADE)
    question_id = models.CharField(max_length=12)
    item_value = models.CharField(max_length=5)
    item_detail = models.TextField(null=True, blank=True)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_modified = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)

    class Meta:
        db_table = 'ovc_afc_form'
        verbose_name = 'AFC Form data'
        verbose_name_plural = 'AFC Forms data'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (str(self.event))


class AFCInfo(models.Model):
    info_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    care = models.ForeignKey(AFCMain, on_delete=models.CASCADE)
    person = models.ForeignKey(RegPerson, on_delete=models.CASCADE)
    item_id = models.CharField(max_length=12)
    item_value = models.CharField(max_length=10)
    item_detail = models.TextField(null=True, blank=True)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_modified = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)

    class Meta:
        db_table = 'ovc_afc_info'
        verbose_name = 'AFC Form Info'
        verbose_name_plural = 'AFC Forms Infos'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (str(self.care))


class AFCQuestions(models.Model):
    """List of questions used by forms."""

    question_text = models.TextField(null=True, blank=True)
    question_code = models.CharField(max_length=50)
    form_id = models.CharField(max_length=4, null=True, blank=True)
    answer_type_id = models.CharField(max_length=4, null=True, blank=True)
    answer_set_id = models.IntegerField(db_index=True, null=True)
    the_order = models.IntegerField(db_index=True, null=True)
    timestamp_created = models.DateTimeField(auto_now=True, null=True)
    timestamp_updated = models.DateTimeField(auto_now=True, null=True)
    is_void = models.BooleanField(default=False)

    class Meta:
        """Override some params."""

        db_table = 'ovc_afc_questions'
        verbose_name = 'AFC Question'
        verbose_name_plural = 'AFC Questions'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (str(self.question_code))
