from enum import Enum, auto
import uuid
from django.db import models
from django.utils import timezone
from cpovc_forms.models import OVCCaseRecord
from cpovc_registry.models import ( RegOrgUnit, AppUser)

# Create your models here.

class ApprovalStatus(Enum):
    NEUTRAL = auto()  # stored as 1 in the DB
    TRUE = auto()  # stored as 2 in the DB
    FALSE = auto()  # stored as 3 in the DB
# CRS Staging
class OVCBasicCRSMobile(models.Model):
    # Make case_id primary key
    case_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1)
    case_serial = models.CharField(max_length=50, default='XXXX')
    case_reporter = models.CharField(max_length=5)
    reporter_telephone = models.CharField(max_length=15, null=True)
    reporter_county = models.CharField(max_length=3, null=True)
    reporter_sub_county = models.CharField(max_length=3, null=True)
    reporter_ward = models.CharField(max_length=100, null=True)
    reporter_village = models.CharField(max_length=100, null=True)
    case_date = models.DateField(default=timezone.now)
    perpetrator = models.CharField(max_length=5, null=True)
    county = models.CharField(max_length=3)
    constituency = models.CharField(max_length=3)
    organization_unit = models.CharField(max_length=100)
    case_landmark = models.CharField(max_length=50, null=True)
    hh_economic_status = models.CharField(max_length=5)
    family_status = models.CharField(max_length=5)
    mental_condition = models.CharField(max_length=5)
    physical_condition = models.CharField(max_length=5)
    other_condition = models.CharField(max_length=5)
    risk_level = models.CharField(max_length=5)
    referral = models.CharField(max_length=5, default='ANNO')
    referral_detail = models.CharField(max_length=200, null=True)
    summon = models.CharField(max_length=5, default='ANNO')
    case_narration = models.TextField(null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True)
    account = models.ForeignKey(AppUser, on_delete=models.CASCADE, default=1)
    case_params = models.TextField(null=True)
    status = models.IntegerField(default=0)
    case_comments = models.TextField(null=True)
    case_record = models.ForeignKey(
        OVCCaseRecord, blank=True, null=True, on_delete=models.CASCADE)
    case_org_unit = models.ForeignKey(
        RegOrgUnit, blank=True, null=True, on_delete=models.CASCADE)
    timestamp_created = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    is_accepted = models.IntegerField(
        choices=[(status.value, status.name) for status in ApprovalStatus],
        default=ApprovalStatus.NEUTRAL.value
    )

    class Meta:
        db_table = 'ovc_basic_case_record_mobile'
        verbose_name = 'Basic Case Record Staging'
        verbose_name_plural = 'Basic Case Records Staging'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.case_serial)


class OVCBasicCategoryMobile(models.Model):
    # Make case_id primary key
    category_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    case_category = models.CharField(max_length=5)
    case_sub_category = models.CharField(max_length=5, null=True)
    case_date_event = models.DateField(default=timezone.now)
    case_nature = models.CharField(max_length=5)
    case_place_of_event = models.CharField(max_length=5)
    case = models.ForeignKey(OVCBasicCRSMobile, on_delete=models.CASCADE)
    is_void = models.BooleanField(default=False)

    class Meta:
        db_table = 'ovc_basic_category_mobile'
        verbose_name = 'Basic Category'
        verbose_name_plural = 'Basic Category'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s' % (self.case_category)


class OVCBasicPersonMobile(models.Model):
    # Make case_id primary key
    person_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    relationship = models.CharField(max_length=5, null=True)
    person_type = models.CharField(
        max_length=5, choices=(
            ('PTRD', 'Reporter'), ('PTPD', 'Perpetrator'),
            ('PTCH', 'Child'), ('PTCG', 'Guardian')))
    first_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    other_names = models.CharField(max_length=50, null=True)
    dob = models.DateField(null=True)
    sex = models.CharField(max_length=5, null=True)
    case = models.ForeignKey(OVCBasicCRSMobile, on_delete=models.CASCADE)
    is_void = models.BooleanField(default=False)

    class Meta:
        db_table = 'ovc_basic_person_mobile'
        verbose_name = 'Basic Person'
        verbose_name_plural = 'Basic Persons'

    def __unicode__(self):
        """To be returned by admin actions."""
        return '%s - %s %s' % (
            self.get_person_type_display(), self.first_name, self.surname)