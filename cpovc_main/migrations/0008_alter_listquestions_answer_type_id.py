# Generated by Django 4.1.7 on 2023-08-15 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_main', '0007_listquestions_question_required'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listquestions',
            name='answer_type_id',
            field=models.CharField(blank=True, choices=[('FMSL', 'Select'), ('FMRD', 'Radio'), ('FMCB', 'Checkbox'), ('FMTF', 'TextField'), ('FMTA', 'TextArea')], max_length=4, null=True),
        ),
    ]