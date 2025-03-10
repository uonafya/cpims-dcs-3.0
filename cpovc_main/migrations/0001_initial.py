# Generated by Django 4.2.16 on 2024-10-10 08:19

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminCaptureSites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_unit_id', models.IntegerField(null=True)),
                ('capture_site_name', models.CharField(blank=True, max_length=255, null=True)),
                ('date_installed', models.DateField(blank=True, null=True)),
                ('approved', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'admin_capture_sites',
            },
        ),
        migrations.CreateModel(
            name='AdminDownload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capture_site_id', models.IntegerField(blank=True, null=True)),
                ('section_id', models.CharField(max_length=4, null=True)),
                ('timestamp_started', models.DateTimeField(null=True)),
                ('timestamp_completed', models.DateTimeField(null=True)),
                ('number_records', models.IntegerField(null=True)),
                ('request_id', models.CharField(max_length=64, null=True)),
                ('success', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'admin_download',
            },
        ),
        migrations.CreateModel(
            name='AdminPreferences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preference_id', models.CharField(max_length=4)),
            ],
            options={
                'db_table': 'admin_preferences',
            },
        ),
        migrations.CreateModel(
            name='AdminUploadForms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp_uploaded', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'admin_upload_forms',
            },
        ),
        migrations.CreateModel(
            name='CaptureTaskTracker',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('task_id', models.CharField(max_length=64, null=True)),
                ('operation', models.CharField(max_length=8, null=True)),
                ('timestamp_started', models.DateTimeField(default=django.utils.timezone.now)),
                ('timestamp_completed', models.DateTimeField(null=True)),
                ('completed', models.BooleanField(default=False)),
                ('cancelled', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'admin_task_tracker',
            },
        ),
        migrations.CreateModel(
            name='CoreAdverseConditions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adverse_condition_id', models.CharField(max_length=4)),
                ('is_void', models.BooleanField(default=False)),
                ('sms_id', models.IntegerField(null=True)),
                ('form_id', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'core_adverse_conditions',
            },
        ),
        migrations.CreateModel(
            name='CoreEncounters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('encounter_date', models.DateField()),
                ('org_unit_id', models.IntegerField()),
                ('area_id', models.IntegerField()),
                ('encounter_type_id', models.CharField(max_length=4)),
                ('sms_id', models.IntegerField(null=True)),
                ('form_id', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'core_encounters',
            },
        ),
        migrations.CreateModel(
            name='CoreEncountersNotes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_id', models.IntegerField()),
                ('encounter_date', models.DateField()),
                ('note_type_id', models.CharField(max_length=4)),
                ('note', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'form_encounters_notes',
            },
        ),
        migrations.CreateModel(
            name='CoreServices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('encounter_date', models.DateField()),
                ('core_item_id', models.CharField(max_length=4)),
                ('sms_id', models.IntegerField(null=True)),
                ('form_id', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'core_services',
            },
        ),
        migrations.CreateModel(
            name='FacilityList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facility_code', models.IntegerField()),
                ('facility_name', models.CharField(max_length=255)),
                ('county_id', models.IntegerField()),
                ('county_name', models.CharField(max_length=255)),
                ('subcounty_id', models.IntegerField()),
                ('subcounty_name', models.CharField(max_length=255)),
                ('latitude', models.DecimalField(decimal_places=5, max_digits=10)),
                ('longitude', models.DecimalField(decimal_places=5, max_digits=10)),
                ('is_void', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'facility_list',
            },
        ),
        migrations.CreateModel(
            name='Forms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_guid', models.CharField(max_length=64)),
                ('form_title', models.CharField(max_length=255, null=True)),
                ('form_type_id', models.CharField(max_length=4, null=True)),
                ('form_subject_id', models.IntegerField(null=True)),
                ('form_area_id', models.IntegerField(null=True)),
                ('date_began', models.DateField(null=True)),
                ('date_ended', models.DateField(null=True)),
                ('date_filled_paper', models.DateField(null=True)),
                ('person_id_filled_paper', models.IntegerField(null=True)),
                ('org_unit_id_filled_paper', models.IntegerField(null=True)),
                ('capture_site_id', models.IntegerField(blank=True, null=True)),
                ('timestamp_created', models.DateTimeField(null=True)),
                ('user_id_created', models.CharField(max_length=9, null=True)),
                ('timestamp_updated', models.DateTimeField(null=True)),
                ('user_id_updated', models.CharField(max_length=9, null=True)),
                ('is_void', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Generic Form',
                'verbose_name_plural': 'Generic Forms',
                'db_table': 'forms',
            },
        ),
        migrations.CreateModel(
            name='ListAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_set_id', models.IntegerField(db_index=True, null=True)),
                ('answer_code', models.CharField(blank=True, db_index=True, max_length=8, null=True)),
                ('answer', models.CharField(blank=True, max_length=255, null=True)),
                ('the_order', models.IntegerField(db_index=True, null=True)),
                ('timestamp_updated', models.DateTimeField(auto_now=True, null=True)),
                ('is_void', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'list_answers',
            },
        ),
        migrations.CreateModel(
            name='ListReports',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_code', models.CharField(blank=True, max_length=100, null=True)),
                ('report_title_short', models.CharField(max_length=255, null=True)),
                ('report_title_long', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'list_reports',
            },
        ),
        migrations.CreateModel(
            name='RegTemp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('page_id', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField()),
                ('_data', models.TextField(blank=True, db_column='page_data')),
            ],
            options={
                'db_table': 'reg_temp_data',
            },
        ),
        migrations.CreateModel(
            name='ReportsSets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('set_name', models.CharField(max_length=70)),
                ('set_type_id', models.CharField(default='SORG', max_length=4)),
                ('user_id_created', models.IntegerField()),
            ],
            options={
                'db_table': 'reports_sets',
            },
        ),
        migrations.CreateModel(
            name='SetupGeography',
            fields=[
                ('area_id', models.IntegerField(primary_key=True, serialize=False)),
                ('area_type_id', models.CharField(max_length=50)),
                ('area_name', models.CharField(max_length=100)),
                ('area_code', models.CharField(max_length=10, null=True)),
                ('parent_area_id', models.IntegerField(null=True)),
                ('area_name_abbr', models.CharField(max_length=5, null=True)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('timestamp_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Setup Geography',
                'verbose_name_plural': 'Setup Geographies',
                'db_table': 'list_geo',
            },
        ),
        migrations.CreateModel(
            name='SetupList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.CharField(max_length=4)),
                ('item_description', models.CharField(max_length=255)),
                ('item_description_short', models.CharField(max_length=26, null=True)),
                ('item_category', models.CharField(blank=True, max_length=255, null=True)),
                ('item_sub_category', models.CharField(blank=True, max_length=255, null=True)),
                ('the_order', models.IntegerField(null=True)),
                ('user_configurable', models.BooleanField(default=False)),
                ('sms_keyword', models.BooleanField(default=False)),
                ('is_void', models.BooleanField(default=False)),
                ('field_name', models.CharField(blank=True, max_length=200, null=True)),
                ('timestamp_updated', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'list_general',
            },
        ),
        migrations.CreateModel(
            name='SetupLocation',
            fields=[
                ('area_id', models.IntegerField(primary_key=True, serialize=False)),
                ('area_name', models.CharField(max_length=100)),
                ('area_type_id', models.CharField(max_length=50)),
                ('area_code', models.CharField(max_length=10, null=True)),
                ('parent_area_id', models.IntegerField(null=True)),
                ('is_void', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'list_location',
            },
        ),
        migrations.CreateModel(
            name='SchoolList',
            fields=[
                ('school_id', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('school_name', models.CharField(max_length=255)),
                ('type_of_school', models.CharField(max_length=26, null=True)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('created_by', models.IntegerField(default=404, null=True)),
                ('school_subcounty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='school_subcounty_fk', to='cpovc_main.setupgeography')),
                ('school_ward', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='school_ward_fk', to='cpovc_main.setupgeography')),
            ],
            options={
                'db_table': 'school_list',
            },
        ),
        migrations.CreateModel(
            name='ReportsSetsOrgUnits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_unit_id', models.IntegerField()),
                ('set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_main.reportssets')),
            ],
            options={
                'db_table': 'reports_sets_org_unit',
            },
        ),
        migrations.CreateModel(
            name='ListReportsParameters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parameter', models.CharField(blank=True, max_length=50, null=True)),
                ('filter', models.CharField(blank=True, max_length=50, null=True)),
                ('initially_visible', models.BooleanField(default=False)),
                ('label', models.CharField(blank=True, max_length=100, null=True)),
                ('tip', models.CharField(blank=True, max_length=255, null=True)),
                ('required', models.BooleanField(default=False)),
                ('report', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cpovc_main.listreports')),
            ],
            options={
                'db_table': 'list_reports_parameter',
            },
        ),
        migrations.CreateModel(
            name='ListQuestions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(blank=True, max_length=255, null=True)),
                ('question_code', models.CharField(max_length=50)),
                ('form_type_id', models.CharField(blank=True, max_length=4, null=True)),
                ('answer_type_id', models.CharField(blank=True, choices=[('FMSL', 'Select'), ('FMRD', 'Radio'), ('FMCB', 'Checkbox'), ('FMTF', 'TextField'), ('FMTA', 'TextArea'), ('FMRO', 'Read Only'), ('FMFL', 'File')], max_length=4, null=True)),
                ('answer_field_id', models.CharField(blank=True, max_length=60, null=True)),
                ('answer_set_id', models.IntegerField(choices=[(1, 'Text'), (2, 'Number'), (3, 'Date')], db_index=True, null=True)),
                ('question_required', models.BooleanField(default=True)),
                ('the_order', models.IntegerField(db_index=True, null=True)),
                ('timestamp_created', models.DateTimeField(auto_now=True, null=True)),
                ('timestamp_updated', models.DateTimeField(auto_now=True, null=True)),
                ('is_void', models.BooleanField(default=False)),
                ('db_field_name', models.CharField(blank=True, max_length=60, null=True)),
                ('question_number', models.CharField(blank=True, max_length=10, null=True)),
                ('form', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cpovc_main.forms')),
            ],
            options={
                'verbose_name': 'Generic Question',
                'verbose_name_plural': 'Generic Questions',
                'db_table': 'list_questions',
            },
        ),
        migrations.CreateModel(
            name='FormResWorkforce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workforce_id', models.IntegerField(blank=True, null=True)),
                ('institution_id', models.IntegerField(blank=True, null=True)),
                ('position_id', models.CharField(blank=True, max_length=4, null=True)),
                ('full_part_time_id', models.CharField(blank=True, max_length=4, null=True)),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_main.forms')),
            ],
            options={
                'db_table': 'form_res_workforce',
            },
        ),
        migrations.CreateModel(
            name='FormResChildren',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child_person_id', models.IntegerField(blank=True, null=True)),
                ('institution_id', models.IntegerField(blank=True, null=True)),
                ('residential_status_id', models.CharField(blank=True, max_length=4, null=True)),
                ('court_committal_id', models.CharField(blank=True, max_length=4, null=True)),
                ('family_status_id', models.CharField(blank=True, max_length=4, null=True)),
                ('date_admitted', models.DateField(blank=True, null=True)),
                ('date_left', models.DateField(blank=True, null=True)),
                ('sms_id', models.IntegerField(blank=True, null=True)),
                ('form', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cpovc_main.forms')),
            ],
            options={
                'db_table': 'form_res_children',
            },
        ),
        migrations.CreateModel(
            name='FormPersonParticipation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workforce_or_beneficiary_id', models.CharField(max_length=15)),
                ('participation_level_id', models.CharField(blank=True, max_length=4, null=True)),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_main.forms')),
            ],
            options={
                'db_table': 'form_person_participation',
            },
        ),
        migrations.CreateModel(
            name='FormOrgUnitContributions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_unit_id', models.CharField(max_length=7)),
                ('contribution_id', models.CharField(max_length=4)),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_main.forms')),
            ],
            options={
                'db_table': 'form_org_unit_contribution',
            },
        ),
        migrations.CreateModel(
            name='FormGenText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.CharField(blank=True, max_length=255, null=True)),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_main.forms')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_main.listquestions')),
            ],
            options={
                'db_table': 'form_gen_text',
            },
        ),
        migrations.CreateModel(
            name='FormGenNumeric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_main.forms')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_main.listquestions')),
            ],
            options={
                'db_table': 'form_gen_numeric',
            },
        ),
        migrations.CreateModel(
            name='FormGenDates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_date', models.DateField()),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_main.forms')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_main.listquestions')),
            ],
            options={
                'db_table': 'form_gen_dates',
            },
        ),
        migrations.CreateModel(
            name='FormGenAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cpovc_main.listanswers')),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_main.forms')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpovc_main.listquestions')),
            ],
            options={
                'db_table': 'form_gen_answers',
            },
        ),
    ]
