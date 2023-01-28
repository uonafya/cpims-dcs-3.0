# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_registry', '0001_initial'),
        ('cpovc_afc', '0002_auto_20221108_0852'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cpovc_forms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='afcmain',
            name='org_unit',
            field=models.ForeignKey(on_delete=models.CASCADE, to='cpovc_registry.RegOrgUnit'),
        ),
        migrations.AddField(
            model_name='afcmain',
            name='person',
            field=models.ForeignKey(on_delete=models.CASCADE, to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='afcinfo',
            name='care',
            field=models.ForeignKey(on_delete=models.CASCADE, to='cpovc_afc.AFCMain'),
        ),
        migrations.AddField(
            model_name='afcinfo',
            name='person',
            field=models.ForeignKey(on_delete=models.CASCADE, to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='afcforms',
            name='event',
            field=models.ForeignKey(on_delete=models.CASCADE, to='cpovc_afc.AFCEvents'),
        ),
        migrations.AddField(
            model_name='afcevents',
            name='care',
            field=models.ForeignKey(on_delete=models.CASCADE, to='cpovc_afc.AFCMain'),
        ),
        migrations.AddField(
            model_name='afcevents',
            name='case',
            field=models.ForeignKey(on_delete=models.CASCADE, to='cpovc_forms.OVCCaseRecord'),
        ),
        migrations.AddField(
            model_name='afcevents',
            name='created_by',
            field=models.ForeignKey(on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='afcevents',
            name='person',
            field=models.ForeignKey(on_delete=models.CASCADE, to='cpovc_registry.RegPerson'),
        ),
    ]
