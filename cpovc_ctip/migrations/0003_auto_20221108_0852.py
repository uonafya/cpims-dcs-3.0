# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_registry', '0001_initial'),
        ('cpovc_forms', '0001_initial'),
        ('cpovc_ctip', '0002_ctipmain_case'),
    ]

    operations = [
        migrations.AddField(
            model_name='ctipmain',
            name='person',
            field=models.ForeignKey(on_delete=models.CASCADE, to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ctipforms',
            name='event',
            field=models.ForeignKey(on_delete=models.CASCADE, to='cpovc_ctip.CTIPEvents'),
        ),
        migrations.AddField(
            model_name='ctipevents',
            name='case',
            field=models.ForeignKey(on_delete=models.CASCADE, to='cpovc_forms.OVCCaseRecord'),
        ),
        migrations.AddField(
            model_name='ctipevents',
            name='person',
            field=models.ForeignKey(on_delete=models.CASCADE, to='cpovc_registry.RegPerson'),
        ),
    ]
