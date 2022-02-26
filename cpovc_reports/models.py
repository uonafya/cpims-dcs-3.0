# import uuid
from django.db import models
from django.utils import timezone
from cpovc_registry.models import RegOrgUnit, RegPersonsTypes, RegPerson
from cpovc_forms.models import OVCCaseRecord, OVCPlacement


class RPTCaseLoad(models.Model):
    """Model for Case Load Report."""

    case = models.ForeignKey(OVCCaseRecord)
    case_serial = models.CharField(max_length=40, null=False)
    case_reporter_id = models.CharField(max_length=4)
    case_reporter = models.CharField(max_length=250)
    case_perpetrator_id = models.CharField(max_length=4, null=True)
    case_perpetrator = models.CharField(max_length=250, null=True)
    case_category_id = models.CharField(max_length=4)
    case_category = models.CharField(max_length=250)
    date_of_event = models.DateField(default=timezone.now)
    place_of_event_id = models.CharField(max_length=4)
    place_of_event = models.CharField(max_length=250)
    sex_id = models.CharField(max_length=4)
    sex = models.CharField(max_length=10)
    dob = models.DateField(default=timezone.now, null=True)
    county_id = models.IntegerField(default=0)
    county = models.CharField(max_length=250, null=True)
    sub_county_id = models.IntegerField(default=0)
    sub_county = models.CharField(max_length=250, null=True)
    org_unit = models.ForeignKey(RegOrgUnit)
    org_unit_name = models.CharField(max_length=250, null=True)
    case_status = models.IntegerField(null=False)
    intervention_id = models.CharField(max_length=4, null=True)
    intervention = models.CharField(max_length=250, null=True)
    case_year = models.IntegerField(default=0)
    case_month = models.IntegerField(default=0)
    case_quota = models.IntegerField(default=0)
    case_count = models.IntegerField(default=1)
    age_range = models.CharField(max_length=20, null=True, blank=True)
    knbs_age_range = models.CharField(max_length=20, null=True, blank=True)
    age = models.IntegerField(default=0, null=True)
    case_date = models.DateField(null=True, default=timezone.now)
    system_date = models.DateField(null=True, default=timezone.now)
    is_void = models.BooleanField(default=False)

    class Meta:
        """Override table details."""

        db_table = 'rpt_case_load'
        verbose_name = 'Protection Case data'
        verbose_name_plural = 'Protection Cases data'

    def __unicode__(self):
        """To be returned by admin actions."""
        return self.case_serial


class SIPopulation(OVCPlacement):
    class Meta:
        proxy = True
        verbose_name = 'SI Population'
        verbose_name_plural = 'SI Populations'


class CCIPopulation(OVCPlacement):
    class Meta:
        proxy = True
        verbose_name = 'CCI Population'
        verbose_name_plural = 'CCI Populations'


class SystemUsage(RegPersonsTypes):
    class Meta:
        proxy = True
        verbose_name = 'System Usage'
        verbose_name_plural = 'System Usages'


class RPTIPopulation(models.Model):
    """Model for Institution Population."""

    case = models.ForeignKey(OVCCaseRecord)
    case_serial = models.CharField(max_length=40, null=False)
    person = models.ForeignKey(RegPerson)
    admission_number = models.CharField(max_length=40, null=False)
    org_unit = models.ForeignKey(RegOrgUnit)
    org_unit_name = models.CharField(max_length=250, null=True)
    org_unit_type_id = models.CharField(max_length=4, null=True)
    org_unit_type = models.CharField(max_length=250, null=True)
    sex_id = models.CharField(max_length=4)
    sex = models.CharField(max_length=10)
    dob = models.DateField(default=timezone.now, null=True)
    age = models.IntegerField(default=0, null=True)
    age_now = models.IntegerField(default=0, null=True)
    age_range = models.CharField(max_length=20, null=True, blank=True)
    knbs_age_range = models.CharField(max_length=20, null=True, blank=True)
    admission_date = models.DateField(default=timezone.now)
    admission_type_id = models.CharField(max_length=4)
    admission_type = models.CharField(max_length=250)
    admission_reason_id = models.CharField(max_length=4)
    admission_reason = models.CharField(max_length=250)
    case_status_id = models.IntegerField(null=False, default=1)
    case_status = models.CharField(max_length=20, null=False)
    case_category_id = models.CharField(max_length=4)
    case_category = models.CharField(max_length=250)
    sub_category_id = models.CharField(max_length=4)
    sub_category = models.CharField(max_length=250)
    discharge_date = models.DateField(null=True, default=timezone.now)
    discharge_type_id = models.CharField(max_length=4, null=True)
    discharge_type = models.CharField(max_length=250, null=True)
    county_id = models.IntegerField(default=0)
    county = models.CharField(max_length=250, null=True)
    sub_county_id = models.IntegerField(default=0)
    sub_county = models.CharField(max_length=250, null=True)
    system_date = models.DateField(null=True, default=timezone.now)
    system_timestamp = models.DateTimeField(null=True, default=timezone.now)
    is_void = models.BooleanField(default=False)

    class Meta:
        """Override table details."""

        db_table = 'rpt_inst_population'
        verbose_name = 'Population Report'
        verbose_name_plural = 'Population Reports'

    def __unicode__(self):
        """To be returned by admin actions."""
        return self.case_serial
