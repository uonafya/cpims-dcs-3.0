import uuid
from django.db import models
from django.utils import timezone

from cpovc_auth.models import AppUser

from cpovc_registry.models import RegPerson, RegOrgUnit
from cpovc_forms.models import OVCCaseRecord, OVCPlacement

YES_NO_CHOICES = (("AYES", "Yes"), ("ANNO", "No"),)


class SIMain(models.Model):
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
        _cases = SIMain.objects.all().count()
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
        super(SIMain, self).save(*args, **kwargs)

    class Meta:
        db_table = 'ovc_si_registration'
        verbose_name = 'Statutory Institutions Care'
        verbose_name_plural = 'Statutory Institutions Cares'

    def __str__(self):
        """To be returned by admin actions."""
        return '%s - %s' % (str(self.case_number), str(self.case))


class SIEvents(models.Model):
    event_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    care = models.ForeignKey(SIMain, on_delete=models.CASCADE)
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
        db_table = 'ovc_si_event'
        verbose_name = 'SI Event'
        verbose_name_plural = 'SI Events'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (str(self.case))


class SIForms(models.Model):
    form_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    event = models.ForeignKey(SIEvents, on_delete=models.CASCADE)
    question_id = models.CharField(max_length=50)
    item_value = models.CharField(max_length=10)
    item_detail = models.TextField(null=True, blank=True)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_modified = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)

    class Meta:
        db_table = 'ovc_si_form'
        verbose_name = 'SI Form data'
        verbose_name_plural = 'SI Forms data'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (str(self.question_id))


class SI_VacancyApp(models.Model):
    vacancy = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    event = models.ForeignKey(
        SIEvents, on_delete=models.CASCADE, null=True, blank=True)
    case = models.ForeignKey(
        OVCCaseRecord, on_delete=models.CASCADE, null=True)
    person = models.ForeignKey(RegPerson, on_delete=models.CASCADE)
    ref_no = models.CharField(max_length=100)
    date_of_application = models.DateField(null=True, blank=True)
    crc_no = models.CharField(max_length=100, null=True, blank=True)
    pnc_no = models.CharField(max_length=100)
    court_number = models.CharField(max_length=100)
    judge_name = models.CharField(max_length=100)
    child_held_at = models.CharField(max_length=100)
    date_of_next_mention = models.DateField()
    requesting_officer = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    sub_county_children_officer = models.CharField(max_length=100)
    application_status = models.BooleanField(default=False)
    date_of_approved = models.DateField(null=True, blank=True)
    approved_by = models.ForeignKey(
        AppUser, on_delete=models.CASCADE, null=True, related_name='approver')
    institution = models.ForeignKey(
        RegOrgUnit, on_delete=models.CASCADE, null=True)
    months_approved = models.IntegerField(default=0, null=True)
    magistrate_court = models.CharField(max_length=100, null=True, blank=True)
    holding_place = models.CharField(max_length=100, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    is_void = models.BooleanField(default=False)
    created_by = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.now)

    class Meta:
        db_table = "si_vacancy"
        verbose_name = "SI Vacancy Application"
        verbose_name_plural = "SI Vacancy Applications"


class SI_Document(models.Model):
    doc_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    person = models.ForeignKey(RegPerson, on_delete=models.CASCADE)
    form_id = models.CharField(max_length=10, null=True)
    document_type = models.CharField(max_length=10)
    document = models.FileField(upload_to='si_docs/')
    is_void = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        AppUser, on_delete=models.CASCADE, null=True)
    created_at = models.DateField(default=timezone.now)

    class Meta:
        db_table = 'si_document'
        verbose_name = "SI Document"
        verbose_name_plural = "SI Documents"


class SIFormsAudit(models.Model):
    audit_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    event = models.ForeignKey(SIEvents, on_delete=models.CASCADE)
    person = models.ForeignKey(RegPerson, on_delete=models.CASCADE)
    form_id = models.CharField(max_length=20)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, null=True)
    trans_type = models.CharField(max_length=10)
    trans_metadata = models.TextField()
    trans_timestamp = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)

    class Meta:
        db_table = 'ovc_si_audit'
        verbose_name = 'SI Form Audit'
        verbose_name_plural = 'SI Forms Audit'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (str(self.form_id))
