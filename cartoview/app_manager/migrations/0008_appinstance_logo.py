# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

import cartoview.app_manager.models


class Migration(migrations.Migration):
    dependencies = [
        ('app_manager', '0007_auto_20180128_0116'),
    ]

    operations = [
        migrations.AddField(
            model_name='appinstance',
            name='logo',
            field=models.ImageField(
                null=True,
                upload_to=cartoview.app_manager.models.get_app_logo_path,
                blank=True),
        ),
    ]
