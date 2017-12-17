# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


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
