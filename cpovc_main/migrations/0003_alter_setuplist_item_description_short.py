# Generated by Django 4.1.7 on 2023-06-26 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_main', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setuplist',
            name='item_description_short',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
