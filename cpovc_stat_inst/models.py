from django.db import models
import uuid
from django.utils import timezone

from cpovc_auth.models import AppUser

# Create your models here.
from cpovc_registry.models import RegPerson

YES_NO_CHOICES = (
    ("yes", "Yes"),
    ("no", "No"),
)


class SI_Admission(models.Model):
    si = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    person = models.ForeignKey(RegPerson, on_delete=models.CASCADE)
    institution_type = models.CharField(max_length=100, null=False, blank=False)  # from list general institution type id
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
    is_void = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        AppUser, on_delete=models.CASCADE, null=True)
    created_at = models.DateField(default=timezone.now)

    class Meta:
        managed = True
        db_table = "ovc_si_main"
        verbose_name = "Statutory Institutions"
        verbose_name_plural = "Statutory Institutions"
        app_label = "Statutory Institutions"
    
class SI_NeedRiskAssessment(models.Model):
    needs = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    person = models.ForeignKey(RegPerson, on_delete=models.CASCADE)
    needrisk_assess = models.CharField(max_length=100)
    previous_institution = models.CharField(max_length=100, blank=True)
    prev_inst_release_date = models.DateField(null=True, blank=True)
    is_void = models.BooleanField(default=False)
    created_by = models.ForeignKey(AppUser, on_delete=models.CASCADE, null=True)
    created_at = models.DateField(default=timezone.now)


    class Meta:
        db_table = "si_needriskassessment"
        verbose_name = "SINeedRiskAssessment"
        verbose_name_plural = "SINeedRiskAssessments"
        app_label = "SINeedRiskAssessment"


class SI_NeedRiskScale(models.Model):
    riskscale = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    person = models.ForeignKey(RegPerson, on_delete=models.CASCADE)
    needrisk_scale = models.CharField(max_length=100)
    needrisk_description = models.CharField(max_length=100)
    needrisk_comment = models.TextField(blank=True)
    is_void = models.BooleanField(default=False)
    created_by = models.ForeignKey(AppUser, on_delete=models.CASCADE, null=True)
    created_at = models.DateField(default=timezone.now)

    class Meta:
        db_table = "si_needriskscale"
        verbose_name = "SINeedRiskScale"
        verbose_name_plural = "SINeedRiskScales"
        app_label = "SINeedRiskScale"


class SI_VacancyApp(models.Model):
    vacancy = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    person = models.ForeignKey(RegPerson, on_delete=models.CASCADE)
    ref_no = models.CharField(max_length=100)
    date_of_application = models.DateField(null=True, blank=True)
    crc_no = models.CharField(max_length=100)
    pnc_no = models.CharField(max_length=100)
    court_number = models.CharField(max_length=100)
    judge_name = models.CharField(max_length=100)
    child_held_at = models.CharField(max_length=100)
    date_of_next_mention = models.DateField()
    requesting_officer = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    sub_county_children_officer = models.CharField(max_length=100)
    application_status = models.BooleanField(default=False)
    date_of_approved = models.DateField()
    months_approved = models.CharField(max_length=100)
    magistrate_court = models.CharField(max_length=100)
    cci_placed = models.CharField(max_length=100)
    is_void = models.BooleanField(default=False)
    created_by = models.ForeignKey(AppUser, on_delete=models.CASCADE, null=True)
    created_at = models.DateField(default=timezone.now)

    class Meta:
        db_table = "si_vacancy"
        verbose_name = "SIVacancyApp"
        verbose_name_plural = "SIVacancyApps"
        app_label = "SIVacancyApp"



class SI_SocialInquiry(models.Model):
    inquiry = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    person = models.ForeignKey(RegPerson, on_delete=models.CASCADE)
    # Child's Details
    school_attended = models.CharField(max_length=100)
    class_name = models.CharField(max_length=100)
    year = models.IntegerField()
    headmaster_teacher_name = models.CharField(max_length=100)
    hobbies = models.CharField(max_length=100)
    types_of_friends = models.CharField(max_length=100)
    mental_physical_condition = models.CharField(max_length=100)
    person_type = models.CharField(max_length=100)

    # Person Details
    name = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    sub_county = models.CharField(max_length=100)
    ward = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    sub_location = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    telephone = models.CharField(max_length=100)
    contact_address = models.CharField(max_length=100)

    # Child's Close Relative
    has_close_relative = models.CharField(max_length=100, blank=True, null=True)
    relative_name = models.CharField(max_length=100)
    child_relative_county = models.CharField(max_length=100)
    child_relative_sub_county = models.CharField(max_length=100)
    child_relative_location = models.CharField(max_length=100)
    child_relative_village = models.CharField(max_length=100)
    child_relative_contact_address = models.CharField(max_length=100)
    relative_telephone = models.CharField(max_length=100)

    # Guardian Details
    guardian_county = models.CharField(max_length=100)
    guardian_location = models.CharField(max_length=100)
    guardian_village = models.CharField(max_length=100)
    guardian_contact_address = models.CharField(max_length=100)

    # Other Details
    chief_name = models.CharField(max_length=100)
    assistant_chief_name = models.CharField(max_length=100)
    neighbours = models.CharField(max_length=100)
    nearest_church_mosque = models.CharField(max_length=100)
    religious_leader_name = models.CharField(max_length=100)
    nearest_school = models.CharField(max_length=100)
    nearest_market_shop = models.CharField(max_length=100)
    nearest_matatu_stage = models.CharField(max_length=100)
    nearest_police_station = models.CharField(max_length=100)

    # Father Details
    father_alive = models.CharField(max_length=100, blank=True, null=True)
    father_name = models.CharField(max_length=100)
    father_age = models.IntegerField()
    father_education_level = models.CharField(max_length=100)
    father_occupation = models.CharField(max_length=100)
    father_address = models.CharField(max_length=100)
    father_telephone = models.CharField(max_length=100)
    father_id_number = models.CharField(max_length=100)
    father_estate_name = models.CharField(max_length=100)
    father_road_name = models.CharField(max_length=100)

    # Mother Details
    mother_alive = models.CharField(max_length=100, blank=True, null=True)
    mother_name = models.CharField(max_length=100)
    mother_age = models.IntegerField()
    mother_education_level = models.CharField(max_length=100)
    mother_occupation = models.CharField(max_length=100)
    mother_address = models.CharField(max_length=100)
    mother_telephone = models.CharField(max_length=100)
    mother_id_number = models.CharField(max_length=100)
    is_void = models.BooleanField(default=False)
    created_by = models.ForeignKey(AppUser, on_delete=models.CASCADE, null=True)
    created_at = models.DateField(default=timezone.now)

    class Meta:
        db_table = 'si_social_inquiry'
        verbose_name = "SIVacancyApp"
        verbose_name_plural = "SIVacancyApps"
        app_label = "SIVacancyApp"


