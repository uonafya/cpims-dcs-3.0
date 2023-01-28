# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_forms', '0001_initial'),
        ('cpovc_ctip', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ctipmain',
            name='case',
            field=models.ForeignKey(on_delete=models.CASCADE, to='cpovc_forms.OVCCaseRecord'),
        ),
    ]
