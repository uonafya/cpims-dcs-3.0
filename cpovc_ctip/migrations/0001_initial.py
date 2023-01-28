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
            name='CTIPEvents',
            fields=[
                ('event_id', models.UUIDField(default=uuid.uuid1, serialize=False, editable=False, primary_key=True)),
                ('event_count', models.IntegerField(default=1)),
                ('event_date', models.DateField()),
                ('form_id', models.CharField(max_length=1, blank=True)),
                ('interviewer', models.CharField(max_length=100, blank=True)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'ovc_ctip_event',
                'verbose_name': 'Trafficking Event',
                'verbose_name_plural': 'Trafficking Events',
            },
        ),
        migrations.CreateModel(
            name='CTIPForms',
            fields=[
                ('form_id', models.UUIDField(default=uuid.uuid1, serialize=False, editable=False, primary_key=True)),
                ('question_id', models.CharField(max_length=12)),
                ('item_value', models.CharField(max_length=5)),
                ('item_detail', models.TextField(null=True, blank=True)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'ovc_ctip_form',
                'verbose_name': 'Trafficking Form data',
                'verbose_name_plural': 'Trafficking Forms data',
            },
        ),
        migrations.CreateModel(
            name='CTIPMain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('case_number', models.CharField(max_length=12, blank=True)),
                ('case_date', models.DateField()),
                ('country', models.CharField(max_length=2, blank=True)),
                ('case_status', models.BooleanField(default=None, null=True)),
                ('case_stage', models.IntegerField(default=0)),
                ('has_consent', models.BooleanField(default=False)),
                ('consent_date', models.DateField(null=True, blank=True)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('timestamp_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'ovc_ctip_main',
                'verbose_name': 'Trafficked Person',
                'verbose_name_plural': 'Trafficked Persons',
            },
        ),
    ]
