# Generated by Django 4.1.7 on 2023-08-14 09:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cpovc_forms', '0002_initial'),
        ('cpovc_registry', '0004_photo_has_consent'),
        ('cpovc_stat_inst', '0004_alter_si_admission_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='SIMain',
            fields=[
                ('si_id', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('case_status', models.BooleanField(default=None, null=True)),
                ('case_stage', models.IntegerField(default=0)),
                ('case_date', models.DateField()),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('timestamp_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_forms.ovccaserecord')),
                ('created_by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('org_unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regorgunit')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_registry.regperson')),
            ],
            options={
                'verbose_name': 'Statutory Institutions Care',
                'verbose_name_plural': 'Statutory Institutions Cares',
                'db_table': 'ovc_si_registration',
            },
        ),
    ]
