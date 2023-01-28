# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AFCEvents',
            fields=[
                ('event_id', models.UUIDField(default=uuid.uuid1, serialize=False, editable=False, primary_key=True)),
                ('event_count', models.IntegerField(default=1)),
                ('event_date', models.DateField()),
                ('form_id', models.CharField(max_length=3, blank=True)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('timestamp_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'ovc_afc_event',
                'verbose_name': 'AFC Event',
                'verbose_name_plural': 'AFC Events',
            },
        ),
        migrations.CreateModel(
            name='AFCForms',
            fields=[
                ('form_id', models.UUIDField(default=uuid.uuid1, serialize=False, editable=False, primary_key=True)),
                ('question_id', models.CharField(max_length=12)),
                ('item_value', models.CharField(max_length=5)),
                ('item_detail', models.TextField(null=True, blank=True)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('timestamp_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'ovc_afc_form',
                'verbose_name': 'AFC Form data',
                'verbose_name_plural': 'AFC Forms data',
            },
        ),
        migrations.CreateModel(
            name='AFCInfo',
            fields=[
                ('info_id', models.UUIDField(default=uuid.uuid1, serialize=False, editable=False, primary_key=True)),
                ('item_id', models.CharField(max_length=12)),
                ('item_value', models.CharField(max_length=5)),
                ('item_detail', models.TextField(null=True, blank=True)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('timestamp_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'ovc_afc_info',
                'verbose_name': 'AFC Form Info',
                'verbose_name_plural': 'AFC Forms Infos',
            },
        ),
        migrations.CreateModel(
            name='AFCMain',
            fields=[
                ('care_id', models.UUIDField(default=uuid.uuid1, serialize=False, editable=False, primary_key=True)),
                ('case_number', models.CharField(max_length=12, blank=True)),
                ('care_type', models.CharField(max_length=5, null=True, blank=True)),
                ('school_level', models.CharField(max_length=4, null=True)),
                ('immunization_status', models.CharField(max_length=4, null=True)),
                ('case_status', models.BooleanField(default=None, null=True)),
                ('case_stage', models.IntegerField(default=0)),
                ('case_date', models.DateField()),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('timestamp_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'ovc_afc_main',
                'verbose_name': 'Alternative Care',
                'verbose_name_plural': 'Alternative Cares',
            },
        ),
        migrations.CreateModel(
            name='AFCQuestions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_text', models.TextField(null=True, blank=True)),
                ('question_code', models.CharField(max_length=50)),
                ('form_id', models.CharField(max_length=4, null=True, blank=True)),
                ('answer_type_id', models.CharField(max_length=4, null=True, blank=True)),
                ('answer_set_id', models.IntegerField(null=True, db_index=True)),
                ('the_order', models.IntegerField(null=True, db_index=True)),
                ('timestamp_created', models.DateTimeField(auto_now=True, null=True)),
                ('timestamp_updated', models.DateTimeField(auto_now=True, null=True)),
                ('is_void', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'ovc_afc_questions',
                'verbose_name': 'AFC Question',
                'verbose_name_plural': 'AFC Questions',
            },
        ),
    ]
