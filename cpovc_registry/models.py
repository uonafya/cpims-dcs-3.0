"""CPIMS Registry models."""
import os
import uuid
from datetime import datetime, date
from difflib import SequenceMatcher
from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
# from django.contrib.postgres.indexes import GinIndex
from cpovc_auth.models import AppUser


class RegOrgUnit(models.Model):
    """Model for Organisational Units details."""

    org_unit_id_vis = models.CharField(max_length=12)
    org_unit_name = models.CharField(max_length=255, null=False)
    org_unit_type_id = models.CharField(max_length=4)
    date_operational = models.DateField(null=True, blank=True)
    date_closed = models.DateField(null=True, blank=True)
    handle_ovc = models.BooleanField(default=False)
    is_void = models.BooleanField(default=False)
    parent_org_unit_id = models.IntegerField(null=True, blank=True)
    created_by = models.ForeignKey(
        AppUser, on_delete=models.CASCADE, null=True)
    created_at = models.DateField(default=timezone.now)

    def _is_active(self):
        if self.date_closed:
            return False
        else:
            return True

    def _parent_unit(self):
        if self.parent_org_unit_id:
            _parent_unit = RegOrgUnit.objects.get(
                id=self.parent_org_unit_id)
            return _parent_unit
        else:
            return "N/A"

    is_active = property(_is_active)
    parent_unit = property(_parent_unit)

    class Meta:
        """Override table details."""

        db_table = 'reg_org_unit'
        verbose_name = 'Organisational Units Registry'
        verbose_name_plural = 'Organisational Units Registries'

    def make_void(self, date_closed=None):
        """Inline call method."""
        self.is_void = True
        if date_closed:
            self.date_closed = date_closed
        super(RegOrgUnit, self).save()

    def __str__(self):
        """To be returned by admin actions."""
        return self.org_unit_name


class RegOrgUnitContact(models.Model):
    """Model for Organisational units contact details."""

    org_unit = models.ForeignKey(RegOrgUnit, on_delete=models.CASCADE)
    contact_detail_type_id = models.CharField(max_length=20)
    contact_detail = models.CharField(max_length=255)
    is_void = models.BooleanField(default=False)

    class Meta:
        """Override table details."""

        db_table = 'reg_org_units_contact'


class RegOrgUnitExternalID(models.Model):
    """Model for Organisational units external IDs."""

    org_unit = models.ForeignKey(RegOrgUnit, on_delete=models.CASCADE)
    identifier_type_id = models.CharField(max_length=4)
    identifier_value = models.CharField(max_length=255, null=True)
    is_void = models.BooleanField(default=False)

    class Meta:
        """Override table details."""

        db_table = 'reg_org_units_external_ids'


class RegOrgUnitGeography(models.Model):
    """Model for Organisational units Geography."""

    org_unit = models.ForeignKey(RegOrgUnit, on_delete=models.CASCADE)
    area = models.ForeignKey(
        'cpovc_main.SetupGeography', on_delete=models.CASCADE)
    date_linked = models.DateField(null=True)
    date_delinked = models.DateField(null=True)
    is_void = models.BooleanField(default=False)

    class Meta:
        """Override table details."""

        db_table = 'reg_org_units_geo'

    def make_void(self, date_delinked=None):
        """Inline call method."""
        self.is_void = True
        if date_delinked:
            self.date_delinked = date_delinked
        elif not self.date_delinked:
            self.date_delinked = datetime.now().date()
        super(RegOrgUnitGeography, self).save()


class RegPerson(models.Model):
    """Model for Persons details."""

    designation = models.CharField(max_length=25, null=True)
    first_name = models.CharField(max_length=255)
    other_names = models.CharField(max_length=255, null=True, blank=True)
    surname = models.CharField(max_length=255, default=None)
    email = models.EmailField(blank=True, null=True)
    des_phone_number = models.IntegerField(null=True, blank=True, default=None)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True, default=None)
    sex_id = models.CharField(max_length=4,
                              choices=[('SMAL', 'Male'), ('SFEM', 'Female')])
    is_void = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        AppUser, on_delete=models.CASCADE, null=True)
    created_at = models.DateField(default=timezone.now)

    def _get_persons_data(self):
        _reg_persons_data = RegPerson.objects.all().order_by('-id')
        return _reg_persons_data

    def _get_full_name(self):
        return '%s %s' % (self.first_name, self.surname)

    def make_void(self):
        """Inline call method."""
        self.is_void = True
        super(RegPerson, self).save()

    def record_death(self, date_of_death=None):
        """Inline call method."""
        if date_of_death:
            self.date_of_death = date_of_death
        super(RegPerson, self).save()

    full_name = property(_get_full_name)

    def _calculate_age(self):
        """Calculate age in years, then months, then days."""
        today = date.today()
        age = 0
        if self.date_of_birth:
            dob = self.date_of_birth
            date_check = (today.month, today.day) < (dob.month, dob.day)
            yrs = today.year - dob.year - (date_check)
            age = '%d years' % (yrs)
            if yrs == 0:
                days = (today - dob).days
                mon = days / 30
                age = '%d days' % days if mon < 1 else '%d months' % mon
        return age

    age = property(_calculate_age)

    def _calculate_years(self):
        """Calculate age in years only."""
        today = date.today()
        yrs = 0
        if self.date_of_birth:
            dob = self.date_of_birth
            date_check = (today.month, today.day) < (dob.month, dob.day)
            yrs = today.year - dob.year - (date_check)
        return yrs

    years = property(_calculate_years)

    class Meta:
        """Override table details."""

        db_table = 'reg_person'
        verbose_name = 'Persons Registry'
        verbose_name_plural = 'Persons Registries'

    def __str__(self):
        """To be returned by admin actions."""
        onames = ' %s' % self.other_names if self.other_names else ''
        return '{} {} {}'.format(self.first_name, self.surname, onames,)


class RegBiometric(models.Model):
    """Model for Persons biometric details."""

    account = models.OneToOneField(AppUser, on_delete=models.CASCADE)
    left_iris = models.BinaryField()
    right_iris = models.BinaryField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        """Override table details."""

        db_table = 'reg_biometric'
        verbose_name = 'Persons Biometric'
        verbose_name_plural = 'Persons Biometrics'

    def __str__(self):
        """To be returned by admin actions."""
        return '%s' % (self.account)


class RegPersonsGuardians(models.Model):
    """Model for Persons (Child) guardians."""

    child_person = models.ForeignKey(RegPerson, on_delete=models.CASCADE,
                                     related_name='child_person')
    guardian_person = models.ForeignKey(RegPerson, on_delete=models.CASCADE,
                                        related_name='guardian_person')
    relationship = models.CharField(max_length=5)
    date_linked = models.DateField(null=True)
    date_delinked = models.DateField(null=True)
    child_headed = models.BooleanField(default=False)
    is_void = models.BooleanField(default=False)

    def make_void(self, date_delinked=None):
        """Inline call method."""
        self.is_void = True
        if date_delinked:
            self.date_delinked = date_delinked
        super(RegPersonsGuardians, self).save()

    class Meta:
        """Override table details."""

        db_table = 'reg_persons_guardians'


class RegPersonsSiblings(models.Model):
    """Model for Persons (Child) siblings."""

    child_person = models.ForeignKey(RegPerson, on_delete=models.CASCADE,
                                     related_name='child_sibling')
    sibling_person = models.ForeignKey(RegPerson, on_delete=models.CASCADE,
                                       related_name='sibling_person')
    date_linked = models.DateField(null=True)
    date_delinked = models.DateField(null=True)
    remarks = models.TextField(null=True)
    is_void = models.BooleanField(default=False)

    def make_void(self, date_delinked=None):
        """Inline call method."""
        self.is_void = True
        if date_delinked:
            self.date_delinked = date_delinked
        super(RegPersonsSiblings, self).save()

    class Meta:
        """Override table details."""

        db_table = 'reg_persons_siblings'


class RegPersonsTypes(models.Model):
    """Model for Persons types details."""

    person = models.ForeignKey(RegPerson, on_delete=models.CASCADE)
    person_type_id = models.CharField(max_length=4)
    date_began = models.DateField(null=True)
    date_ended = models.DateField(null=True, default=None)
    is_void = models.BooleanField(default=False)

    def make_void(self, person_type_change_date=None):
        """Inline call method."""
        self.is_void = True
        if person_type_change_date:
            self.date_ended = person_type_change_date
        super(RegPersonsTypes, self).save()

    class Meta:
        """Override table details."""

        db_table = 'reg_persons_types'
        verbose_name = 'Person Type (Child, Caregiver, other)'
        verbose_name_plural = 'Person Types (Child, Caregiver, other)'


class RegPersonsGeo(models.Model):
    """Model for Persons Geography."""

    from cpovc_main.models import SetupGeography
    person = models.ForeignKey(RegPerson, on_delete=models.CASCADE)
    area = models.ForeignKey(SetupGeography, on_delete=models.CASCADE)
    area_type = models.CharField(max_length=4)
    date_linked = models.DateField(null=True)
    date_delinked = models.DateField(null=True)
    is_void = models.BooleanField(default=False)

    def make_void(self, date_delinked, is_void):
        """Inline call method."""
        if date_delinked:
            self.date_delinked = date_delinked
            self.is_void = True
        super(RegPersonsGeo, self).save()

    class Meta:
        """Override table details."""

        db_table = 'reg_persons_geo'
        verbose_name = 'Person Geographical area (Ward, Sub-county)'
        verbose_name_plural = 'Person Geographical areas (Ward, Sub-county)'


class RegPersonsExternalIds(models.Model):
    """Model for Persons External IDs."""

    person = models.ForeignKey(RegPerson, on_delete=models.CASCADE)
    identifier_type_id = models.CharField(max_length=4)
    identifier = models.CharField(max_length=255)
    is_void = models.BooleanField(default=False)

    def make_void(self):
        """Inline call method."""
        self.is_void = True
        super(RegPersonsExternalIds, self).save()

    class Meta:
        """Override table details."""

        db_table = 'reg_persons_external_ids'

    def __str__(self):
        """To be returned by admin actions."""
        return '%s' % (self.identifier)


class RegPersonsContact(models.Model):
    """Model for Persons contacts."""

    person = models.ForeignKey(RegPerson, on_delete=models.CASCADE)
    contact_detail_type_id = models.CharField(max_length=4)
    contact_detail = models.CharField(max_length=255)
    is_void = models.BooleanField(default=False)

    def make_void(self):
        """Inline call method."""
        self.is_void = True
        super(RegPersonsContact, self).save()

    class Meta:
        """Override table details."""

        db_table = 'reg_persons_contact'


class RegPersonsOrgUnits(models.Model):
    """Model for Persons Organisational Units."""

    person = models.ForeignKey(RegPerson, on_delete=models.CASCADE)
    org_unit = models.ForeignKey(RegOrgUnit, on_delete=models.CASCADE)
    date_linked = models.DateField(null=True)
    date_delinked = models.DateField(null=True, blank=True)
    primary_unit = models.BooleanField(default=False)
    reg_assistant = models.BooleanField(default=False)
    is_void = models.BooleanField(default=False)

    class Meta:
        """Override table details."""

        db_table = 'reg_persons_org_units'
        verbose_name = 'Persons Organisation Unit'
        verbose_name_plural = 'Persons Organisation Units'


class RegPersonsWorkforceIds(models.Model):
    """Model for Persons Workforce IDs."""

    person = models.ForeignKey(RegPerson, on_delete=models.CASCADE)
    workforce_id = models.CharField(max_length=8, null=True)

    class Meta:
        """Override table details."""

        db_table = 'reg_persons_workforce_ids'


class RegPersonsBeneficiaryIds(models.Model):
    """Model for Persons Beneficiary IDs."""

    person = models.ForeignKey(RegPerson, on_delete=models.CASCADE)
    beneficiary_id = models.CharField(max_length=10, null=True)

    class Meta:
        """Override table details."""

        db_table = 'reg_persons_beneficiary_ids'


class RegOrgUnitsAuditTrail(models.Model):
    """Model for Organisational units Audit."""

    transaction_id = models.AutoField(primary_key=True)
    org_unit = models.ForeignKey(RegOrgUnit, on_delete=models.CASCADE)
    transaction_type_id = models.CharField(max_length=4, null=True,
                                           db_index=True)
    interface_id = models.CharField(max_length=4, null=True, db_index=True)
    timestamp_modified = models.DateTimeField(auto_now=True)
    app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(protocol='both')
    meta_data = models.TextField(null=True)

    class Meta:
        """Override table details."""

        db_table = 'reg_org_units_audit_trail'
        app_label = 'cpovc_registry'
        verbose_name = 'Org Units Audit Trail'
        verbose_name_plural = 'Org Units Audit Trails'


class RegPersonsAuditTrail(models.Model):
    """Model for Persons Audit."""

    transaction_id = models.AutoField(primary_key=True)
    person = models.ForeignKey(RegPerson, on_delete=models.CASCADE)
    transaction_type_id = models.CharField(max_length=4, null=True,
                                           db_index=True)
    interface_id = models.CharField(max_length=4, null=True, db_index=True)
    date_recorded_paper = models.DateField(null=True)
    person_recorded_paper = models.ForeignKey(
        RegPerson, on_delete=models.CASCADE,
        related_name='person_recorded_paper', null=True)
    timestamp_modified = models.DateTimeField(auto_now=True)
    app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(protocol='both')
    meta_data = models.TextField(null=True)

    class Meta:
        """Override table details."""

        db_table = 'reg_persons_audit_trail'
        app_label = 'cpovc_registry'
        verbose_name = 'Persons Audit Trail'
        verbose_name_plural = 'Persons Audit Trails'


class OVCSibling(models.Model):
    """Model for Siblings details."""

    person = models.ForeignKey(
        RegPerson, on_delete=models.CASCADE, related_name='ovc_sibling')
    cpims = models.ForeignKey(
        RegPerson, on_delete=models.CASCADE,
        related_name='ovc_cpims', null=True)
    first_name = models.CharField(max_length=50)
    other_names = models.CharField(max_length=50, default=None)
    surname = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    sex_id = models.CharField(max_length=4)
    class_level = models.CharField(max_length=4, null=True)
    remarks = models.CharField(max_length=250, null=True)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)

    class Meta:
        """Override table details."""

        db_table = 'ovc_sibling'


class OVCCheckin(models.Model):
    """Model for Siblings details."""

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(RegPerson, on_delete=models.CASCADE)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    org_unit = models.ForeignKey(
        RegOrgUnit, on_delete=models.CASCADE, null=True)
    is_ovc = models.BooleanField(default=True)
    is_void = models.BooleanField(default=False)
    timestamp_created = models.DateTimeField(default=timezone.now)

    class Meta:
        """Override table details."""

        db_table = 'ovc_checkin'


class OVCHouseHold(models.Model):
    """Model for Siblings details."""

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    index_child = models.ForeignKey(
        RegPerson, on_delete=models.CASCADE, related_name='index_child')
    members = models.TextField()
    is_void = models.BooleanField(default=False)
    timestamp_created = models.DateTimeField(default=timezone.now)

    class Meta:
        """Override table details."""

        db_table = 'reg_household'
        # indexes = [GinIndex(fields=['members'])]


class PersonsMaster(models.Model):
    """Model for Siblings details."""

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(RegPerson, on_delete=models.CASCADE, null=True)
    person_type = models.CharField(max_length=5, null=True)
    system_id = models.CharField(max_length=100, null=True)
    timestamp_created = models.DateTimeField(default=timezone.now)

    class Meta:
        """Override table details."""

        db_table = 'reg_person_master'


class RegPersonsOtherGeo(models.Model):
    """Model for Persons Other Geography."""
    # Imported here because of cyclic importation
    from cpovc_main.models import SetupLocation

    person = models.OneToOneField(RegPerson, on_delete=models.CASCADE)
    country_code = models.CharField(max_length=4, null=True)
    city = models.CharField(max_length=150, null=True)
    location = models.ForeignKey(
        SetupLocation, on_delete=models.CASCADE, null=True)
    date_linked = models.DateField(null=True)
    is_void = models.BooleanField(default=False)

    class Meta:
        """Override table details."""

        db_table = 'reg_person_other_geo'
        verbose_name = 'Person Geo area (Country, City, Location)'
        verbose_name_plural = 'Person Geo areas (Country, City, Location)'


@receiver(pre_save, sender=RegOrgUnit)
def check_malice(sender, instance, **kwargs):
    """Method to check malicious edits."""
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass
    else:
        oname = obj.org_unit_name.upper()
        aname = instance.org_unit_name.upper()
        sm = SequenceMatcher(None, oname, aname)
        sm_ratio = round(sm.ratio(), 2) * 100
        if sm_ratio < 70:
            raise Exception('Complete change of Org Unit name is NOT allowed.')


def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.user.id, instance.questid.id, ext)
    return os.path.join('uploads', filename)


class Photo(models.Model):
    person = models.ForeignKey(RegPerson, on_delete=models.CASCADE)
    photo_passport = models.FileField(upload_to='photos/')
    photo_fullsize = models.FileField(upload_to='photos/', null=True)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)

    def add(request):
        tr_uuid = uuid.uuid4()
        file = request.POST['file']
        file._name = request.user.id + tr_uuid + "." + file._name.split('.')[1]

    class Meta:
        """Override table details."""

        db_table = 'reg_person_photo'
        verbose_name = 'Person Photo'
        verbose_name_plural = 'Person Photos'

