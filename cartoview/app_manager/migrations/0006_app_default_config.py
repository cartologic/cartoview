# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import jsonfield.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('app_manager', '0005_delete_apptag'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='default_config',
            field=jsonfield.fields.JSONField(default={}),
        ),
    ]
