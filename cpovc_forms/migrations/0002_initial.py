# Generated by Django 4.2.16 on 2024-10-10 08:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cpovc_forms', '0001_initial'),
        ('cpovc_registry', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cpovc_ovc', '0001_initial'),
        ('cpovc_main', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ovcsubpopulation',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovcreminders',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovcreferrals',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccareevents'),
        ),
        migrations.AddField(
            model_name='ovcreferrals',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovcreferral',
            name='case_category',
            field=models.ForeignKey(default=uuid.uuid1, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccasecategory'),
        ),
        migrations.AddField(
            model_name='ovcreferral',
            name='case_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccaserecord'),
        ),
        migrations.AddField(
            model_name='ovcreferral',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovcprogramregistration',
            name='child_cbo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prog_cbo', to='cpovc_registry.regorgunit'),
        ),
        migrations.AddField(
            model_name='ovcprogramregistration',
            name='child_chv',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prog_chv', to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovcprogramregistration',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ovcprogramregistration',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovcplacementfollowup',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovcplacementfollowup',
            name='placement_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovcplacement'),
        ),
        migrations.AddField(
            model_name='ovcplacement',
            name='case_record',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccaserecord'),
        ),
        migrations.AddField(
            model_name='ovcplacement',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovcplacement',
            name='residential_institution',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regorgunit'),
        ),
        migrations.AddField(
            model_name='ovcplacement',
            name='transfer_from_institution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ou_from', to='cpovc_registry.regorgunit'),
        ),
        migrations.AddField(
            model_name='ovcplacement',
            name='transfer_to_institution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ou', to='cpovc_registry.regorgunit'),
        ),
        migrations.AddField(
            model_name='ovcneeds',
            name='case_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccaserecord'),
        ),
        migrations.AddField(
            model_name='ovcneeds',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovcmonitoring',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccareevents'),
        ),
        migrations.AddField(
            model_name='ovcmonitoring',
            name='household',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_ovc.ovchousehold'),
        ),
        migrations.AddField(
            model_name='ovcmedicalsubconditions',
            name='medical_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovcmedical'),
        ),
        migrations.AddField(
            model_name='ovcmedicalsubconditions',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovcmedical',
            name='case_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccaserecord'),
        ),
        migrations.AddField(
            model_name='ovcmedical',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovchouseholddemographics',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccareevents'),
        ),
        migrations.AddField(
            model_name='ovchouseholddemographics',
            name='household',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_ovc.ovchousehold'),
        ),
        migrations.AddField(
            model_name='ovchobbies',
            name='case_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccaserecord'),
        ),
        migrations.AddField(
            model_name='ovchobbies',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovchivstatus',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccareevents'),
        ),
        migrations.AddField(
            model_name='ovchivstatus',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovchivriskscreening',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccareevents'),
        ),
        migrations.AddField(
            model_name='ovchivriskscreening',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovchivmanagement',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccareevents'),
        ),
        migrations.AddField(
            model_name='ovchivmanagement',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovcgokbursary',
            name='app_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ovcgokbursary',
            name='constituency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child_constituency', to='cpovc_main.setupgeography'),
        ),
        migrations.AddField(
            model_name='ovcgokbursary',
            name='county',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child_county', to='cpovc_main.setupgeography'),
        ),
        migrations.AddField(
            model_name='ovcgokbursary',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovcgokbursary',
            name='school_bank',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.listbanks'),
        ),
        migrations.AddField(
            model_name='ovcgokbursary',
            name='school_constituency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='school_constituency', to='cpovc_main.setupgeography'),
        ),
        migrations.AddField(
            model_name='ovcgokbursary',
            name='school_county',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='school_county', to='cpovc_main.setupgeography'),
        ),
        migrations.AddField(
            model_name='ovcgoals',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccareevents'),
        ),
        migrations.AddField(
            model_name='ovcgoals',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovcfriends',
            name='case_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccaserecord'),
        ),
        migrations.AddField(
            model_name='ovcfriends',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovcfmpevaluation',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccareevents'),
        ),
        migrations.AddField(
            model_name='ovcfmpevaluation',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovcfamilystatus',
            name='case_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccaserecord'),
        ),
        migrations.AddField(
            model_name='ovcfamilystatus',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovcfamilycare',
            name='adoption_subcounty',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='adoption_subcounty_fk', to='cpovc_main.setupgeography'),
        ),
        migrations.AddField(
            model_name='ovcfamilycare',
            name='children_office',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children_office_fk', to='cpovc_registry.regorgunit'),
        ),
        migrations.AddField(
            model_name='ovcfamilycare',
            name='fostered_from',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fostered_from_fk', to='cpovc_registry.regorgunit'),
        ),
        migrations.AddField(
            model_name='ovcfamilycare',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovcfamilycare',
            name='residential_institution_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='residential_institution_name_fk', to='cpovc_registry.regorgunit'),
        ),
        migrations.AddField(
            model_name='ovcexplanations',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccareevents'),
        ),
        migrations.AddField(
            model_name='ovcexplanations',
            name='form',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccareforms'),
        ),
        migrations.AddField(
            model_name='ovcexplanations',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccarequestions'),
        ),
        migrations.AddField(
            model_name='ovceducationlevelfollowup',
            name='education_followup_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovceducationfollowup'),
        ),
        migrations.AddField(
            model_name='ovceducationfollowup',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovceducationfollowup',
            name='placement_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovcplacement'),
        ),
        migrations.AddField(
            model_name='ovceducationfollowup',
            name='school_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cpovc_main.schoollist'),
        ),
        migrations.AddField(
            model_name='ovceconomicstatus',
            name='case_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccaserecord'),
        ),
        migrations.AddField(
            model_name='ovceconomicstatus',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovcdreams',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccareevents'),
        ),
        migrations.AddField(
            model_name='ovcdreams',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovcdocuments',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovcdischargefollowup',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovcdischargefollowup',
            name='placement_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovcplacement'),
        ),
        migrations.AddField(
            model_name='ovccasesubcategory',
            name='case_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccasecategory'),
        ),
        migrations.AddField(
            model_name='ovccasesubcategory',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovccaserecord',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovccasepersons',
            name='case',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccaserecord'),
        ),
        migrations.AddField(
            model_name='ovccasepersons',
            name='person',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovccaselocation',
            name='case',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccaserecord'),
        ),
        migrations.AddField(
            model_name='ovccaselocation',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovccaselocation',
            name='report_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='location', to='cpovc_main.setuplocation'),
        ),
        migrations.AddField(
            model_name='ovccaselocation',
            name='report_sublocation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_location', to='cpovc_main.setuplocation'),
        ),
        migrations.AddField(
            model_name='ovccaseinformation',
            name='case',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccaserecord'),
        ),
        migrations.AddField(
            model_name='ovccaseinformation',
            name='person',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovccasegeo',
            name='case_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccaserecord'),
        ),
        migrations.AddField(
            model_name='ovccasegeo',
            name='occurence_county',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='occurence_county_fk', to='cpovc_main.setupgeography'),
        ),
        migrations.AddField(
            model_name='ovccasegeo',
            name='occurence_subcounty',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='occurence_subcounty_fk', to='cpovc_main.setupgeography'),
        ),
        migrations.AddField(
            model_name='ovccasegeo',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovccasegeo',
            name='report_orgunit',
            field=models.ForeignKey(max_length=10, null=True, on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regorgunit'),
        ),
        migrations.AddField(
            model_name='ovccasegeo',
            name='report_subcounty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_subcounty_fk', to='cpovc_main.setupgeography'),
        ),
        migrations.AddField(
            model_name='ovccaseeventsummon',
            name='case_category',
            field=models.ForeignKey(default=uuid.uuid1, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccasecategory'),
        ),
        migrations.AddField(
            model_name='ovccaseeventsummon',
            name='case_event_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccaseevents'),
        ),
        migrations.AddField(
            model_name='ovccaseeventservices',
            name='case_category',
            field=models.ForeignKey(blank=True, default=uuid.uuid1, editable=False, on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccasecategory'),
        ),
        migrations.AddField(
            model_name='ovccaseeventservices',
            name='case_event_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccaseevents'),
        ),
        migrations.AddField(
            model_name='ovccaseevents',
            name='app_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ovccaseevents',
            name='case_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccaserecord'),
        ),
        migrations.AddField(
            model_name='ovccaseevents',
            name='placement_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovcplacement'),
        ),
        migrations.AddField(
            model_name='ovccaseeventcourt',
            name='case_category',
            field=models.ForeignKey(blank=True, default=uuid.uuid1, editable=False, on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccasecategory'),
        ),
        migrations.AddField(
            model_name='ovccaseeventcourt',
            name='case_event_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccaseevents'),
        ),
        migrations.AddField(
            model_name='ovccaseeventclosure',
            name='case_event_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccaseevents'),
        ),
        migrations.AddField(
            model_name='ovccaseeventclosure',
            name='transfer_to',
            field=models.ForeignKey(max_length=10, null=True, on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regorgunit'),
        ),
        migrations.AddField(
            model_name='ovccasecategory',
            name='case_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccaserecord'),
        ),
        migrations.AddField(
            model_name='ovccasecategory',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovccarewellbeing',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccareevents'),
        ),
        migrations.AddField(
            model_name='ovccarewellbeing',
            name='household',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_ovc.ovchousehold'),
        ),
        migrations.AddField(
            model_name='ovccarewellbeing',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovccarewellbeing',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccarequestions'),
        ),
        migrations.AddField(
            model_name='ovccaretransfer',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccareevents'),
        ),
        migrations.AddField(
            model_name='ovccaretransfer',
            name='household',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_ovc.ovchousehold'),
        ),
        migrations.AddField(
            model_name='ovccaretransfer',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovccaretransfer',
            name='rec_organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regorgunit'),
        ),
        migrations.AddField(
            model_name='ovccareservices',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccareevents'),
        ),
        migrations.AddField(
            model_name='ovccarequestions',
            name='form',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccareforms'),
        ),
        migrations.AddField(
            model_name='ovccarepriority',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccareevents'),
        ),
        migrations.AddField(
            model_name='ovccareindividaulcpara',
            name='caregiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='icpara_caregiver', to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovccareindividaulcpara',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccareevents'),
        ),
        migrations.AddField(
            model_name='ovccareindividaulcpara',
            name='household',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_ovc.ovchousehold'),
        ),
        migrations.AddField(
            model_name='ovccareindividaulcpara',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cpara_person', to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovccareindividaulcpara',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccarequestions'),
        ),
        migrations.AddField(
            model_name='ovccaref1b',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccareevents'),
        ),
        migrations.AddField(
            model_name='ovccareevents',
            name='house_hold',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cpovc_ovc.ovchousehold'),
        ),
        migrations.AddField(
            model_name='ovccareevents',
            name='person',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovccareeav',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccareevents'),
        ),
        migrations.AddField(
            model_name='ovccarecpara',
            name='caregiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cpara_caregiver', to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovccarecpara',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccareevents'),
        ),
        migrations.AddField(
            model_name='ovccarecpara',
            name='household',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_ovc.ovchousehold'),
        ),
        migrations.AddField(
            model_name='ovccarecpara',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovccarecpara',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccarequestions'),
        ),
        migrations.AddField(
            model_name='ovccarecaseplan',
            name='caregiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='caseplan_caregiver', to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovccarecaseplan',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccareevents'),
        ),
        migrations.AddField(
            model_name='ovccarecaseplan',
            name='form',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccareforms'),
        ),
        migrations.AddField(
            model_name='ovccarecaseplan',
            name='household',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_ovc.ovchousehold'),
        ),
        migrations.AddField(
            model_name='ovccarecaseplan',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovccarecaseexit',
            name='caregiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exit_caregiver', to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovccarecaseexit',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccareevents'),
        ),
        migrations.AddField(
            model_name='ovccarecaseexit',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regorgunit'),
        ),
        migrations.AddField(
            model_name='ovccarecaseexit',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='caseclouse_child', to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovccarebenchmarkscore',
            name='care_giver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovccarebenchmarkscore',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccareevents'),
        ),
        migrations.AddField(
            model_name='ovccarebenchmarkscore',
            name='household',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cpovc_ovc.ovchousehold'),
        ),
        migrations.AddField(
            model_name='ovccareassessment',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccareevents'),
        ),
        migrations.AddField(
            model_name='ovcbursary',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovcbenchmarkmonitoring',
            name='caregiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='care_giver', to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovcbenchmarkmonitoring',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccareevents'),
        ),
        migrations.AddField(
            model_name='ovcbenchmarkmonitoring',
            name='household',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_ovc.ovchousehold'),
        ),
        migrations.AddField(
            model_name='ovcbasicperson',
            name='case',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovcbasiccrs'),
        ),
        migrations.AddField(
            model_name='ovcbasiccrs',
            name='account',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ovcbasiccrs',
            name='case_org_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regorgunit'),
        ),
        migrations.AddField(
            model_name='ovcbasiccrs',
            name='case_record',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccaserecord'),
        ),
        migrations.AddField(
            model_name='ovcbasiccategory',
            name='case',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovcbasiccrs'),
        ),
        migrations.AddField(
            model_name='ovcadverseeventsotherfollowup',
            name='adverse_condition_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovcadverseeventsfollowup'),
        ),
        migrations.AddField(
            model_name='ovcadverseeventsfollowup',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='ovcadverseeventsfollowup',
            name='placement_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovcplacement'),
        ),
        migrations.AddField(
            model_name='formslog',
            name='person',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson'),
        ),
        migrations.AddField(
            model_name='formsaudittrail',
            name='app_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
