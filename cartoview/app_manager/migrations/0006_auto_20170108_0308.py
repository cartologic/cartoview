# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_manager', '0005_appstore_is_default'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='app',
            name='admin_only',
        ),
        migrations.RemoveField(
            model_name='app',
            name='in_menu',
        ),
        migrations.AddField(
            model_name='app',
            name='version',
            field=models.CharField(default='0.0', max_length=10),
            preserve_default=False,
        ),
    ]
