# Generated by Django 4.1.7 on 2023-08-15 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_main', '0008_alter_listquestions_answer_type_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listquestions',
            name='answer_set_id',
            field=models.IntegerField(choices=[(1, 'Text'), (2, 'Number'), (3, 'Date')], db_index=True, null=True),
        ),
    ]
