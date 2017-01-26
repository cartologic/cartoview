# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_manager', '0004_auto_20170104_0854'),
    ]

    operations = [
        migrations.AddField(
            model_name='appstore',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
    ]
