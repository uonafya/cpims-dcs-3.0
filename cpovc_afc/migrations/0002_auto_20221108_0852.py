# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cpovc_forms', '0001_initial'),
        ('cpovc_afc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='afcmain',
            name='case',
            field=models.ForeignKey(on_delete=models.CASCADE, to='cpovc_forms.OVCCaseRecord'),
        ),
        migrations.AddField(
            model_name='afcmain',
            name='created_by',
            field=models.ForeignKey(on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
